# Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021

import pytest

import numpy as np
from ..serializers import table_to_json, table_from_json
from ..numpy_adapter import NumpyAdapter
from ..pandas_adapter import PandasAdapter
from ..compressors import LZ4Compressor
import pandas as pd


class FakeWidget:
    def __init__(self, compression=None):
        self.compression = compression


def test_table_to_json_none():
    assert table_to_json(None, None) is None


def test_table_unsupported():
    # See https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html
    arrays = [
        ["bar", "bar", "baz", "baz", "foo", "foo", "qux", "qux"],
        ["one", "two", "one", "two", "one", "two", "one", "two"],
    ]
    tuples = list(zip(*arrays))
    index = pd.MultiIndex.from_tuples(tuples, names=["first", "second"])
    df = pd.DataFrame(np.random.randn(3, 8),
                      index=["A", "B", "C"],
                      columns=index)
    with pytest.raises(ValueError) as excinfo:
        PandasAdapter(df.T)
    assert "Hierarchical indices" in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        PandasAdapter(df)
    assert "Hierarchical columns" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        s = pd.Series(pd.date_range("2012-1-1", periods=3, freq="D"))
        td = pd.Series([pd.Timedelta(days=i) for i in range(3)])
        df = pd.DataFrame({"A": s, "B": td})
        PandasAdapter(df)
    assert "not supported" in str(excinfo.value)


def test_table_range_index():
    df = pd.DataFrame([[1, 2, 3], [4, 5, 6]])
    assert isinstance(df.columns, pd.RangeIndex)
    pd_data = PandasAdapter(df)
    assert isinstance(pd_data.columns, list)


def test_table_non_str_column():
    df = pd.DataFrame([[1, 2, 3], [4, 5, 6]])
    assert isinstance(df.columns, pd.RangeIndex)
    with pytest.raises(ValueError):
        PandasAdapter(df, columns=['0', 1])
    PandasAdapter(df, columns=['0', '1'])


def test_table_translate():
    # TODO add NaN values
    list_ = list('ipytablewidgets')
    arr_s = np.array(list_, dtype=str)
    arr_n = np.arange(len(list_), dtype='float32')
    # Convert categories into objects (str or None)
    arr_c = pd.Series(list_, dtype="category")
    # Convert strings into objects (str or None)
    arr_S = pd.Series(list_, dtype="string")
    arr_S[2] = pd.NA  # Add NA at index 2
    # Convert boolean into objects (bool or None)
    data = np.random.choice(a=[False, True], size=len(list_))
    arr_B = pd.Series(data, dtype="boolean")
    arr_B[3] = pd.NA  # Add NA at index 3
    # Convert datetime[...] into objects (str or None)
    data = pd.date_range("2018-01-01", periods=len(list_), freq="H")
    arr_D = pd.Series(data)
    arr_D[4] = pd.NA  # Add NA at index 4
    # Convert nullable integer datatypes
    data = np.arange(len(list_), dtype='int32')
    arr_I = pd.Series(data, dtype="UInt16")
    arr_I[5] = pd.NA
    # Convert object array with sub arrays in it (edge case)
    data = list('ipytablewidgets')
    arr_O = np.array(data, dtype=object)
    arr_O[6] = np.arange(10)
    pd_data = PandasAdapter(pd.DataFrame({'s': arr_s,
                                          'n': arr_n,
                                          'c': arr_c,
                                          'S': arr_S,
                                          'B': arr_B,
                                          'D': arr_D,
                                          'I': arr_I,
                                          'O': arr_O}))
    cat = pd_data.to_array('c')
    assert (isinstance(cat, np.ndarray)
            and cat.dtype == object)
    S = pd_data.to_array('S')
    assert (isinstance(S, np.ndarray)
            and S.dtype == object
            and S[2] is None)
    B = pd_data.to_array('B')
    assert (isinstance(B, np.ndarray)
            and B.dtype == object
            and B[3] is None)
    D = pd_data.to_array('D')
    assert (isinstance(D, np.ndarray)
            and D.dtype == object
            and D[4] == "")
    I = pd_data.to_array('I')
    assert (isinstance(I, np.ndarray)
            and I.dtype == object
            and I[5] is None)
    O = pd_data.to_array('O')
    assert (isinstance(O, np.ndarray)
            and O.dtype == object
            and isinstance(O[6], list))
    return pd_data


def _table_to_json(widget):
    list_ = list('ipytablewidgets')
    arr_s = np.array(list_, dtype=str)
    arr_n = np.arange(len(list_), dtype='float32')
    np_data = NumpyAdapter({'s': arr_s, 'n': arr_n})
    np_json = table_to_json(np_data, widget)
    pd_data = PandasAdapter(pd.DataFrame({'s': arr_s,
                                          'n': arr_n}))
    assert pd_data.columns == np_data.columns
    assert np.array_equal(pd_data.to_array('s'), np_data.to_array('s'))
    pd_json = table_to_json(np_data, widget)
    assert np_json == pd_json
    assert np_data.equals(pd_data)
    assert pd_data.equals(np_data)
    assert pd_data.equals(pd.DataFrame(np_data._source))
    pd_json = table_to_json(test_table_translate(), widget)


def test_table_to_json():
    widget = FakeWidget()
    _table_to_json(widget)


def test_table_to_json_zlib():
    widget = FakeWidget("zlib")
    _table_to_json(widget)


def test_table_to_json_lz4():
    widget = FakeWidget(LZ4Compressor(level=4))
    _table_to_json(widget)


def test_table_to_json_csp():  # with column specific compressors
    widget = FakeWidget({'n': 'zlib', 's': LZ4Compressor(level=4)})
    _table_to_json(widget)


def test_table_from_json():
    assert table_from_json(None, None) == {}  # not implemented
