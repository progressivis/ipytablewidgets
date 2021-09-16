# Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021

import numpy as np
from ..serializers import table_to_json, table_from_json
from ..numpy_adapter import NumpyAdapter
from ..pandas_adapter import PandasAdapter
from ..compressors import DEFAULT_COMPRESSORS, ZLibCompressor, LZ4Compressor
import pandas as pd
import lz4.frame
import zlib
import json

class FakeWidget:
    def __init__(self, compression=None):
        self.compression = compression

def test_table_to_json_none():
    assert table_to_json(None, None) is None

def _table_to_json(widget):
    list_ = list('ipytablewidgets')
    arr_s = np.array(list_, dtype=str)
    arr_n = np.arange(len(list_), dtype='float32')
    np_data = NumpyAdapter({'s': arr_s, 'n': arr_n})
    np_json = table_to_json(np_data, widget)
    pd_data = PandasAdapter(pd.DataFrame({'s': arr_s, 'n': arr_n}))
    #import pdb;pdb.set_trace()
    assert pd_data.columns == np_data.columns
    assert np.array_equal(pd_data.to_array('s'), np_data.to_array('s'))
    pd_json = table_to_json(np_data, widget)
    assert np_json == pd_json
    assert np_data.equals(pd_data)
    assert pd_data.equals(np_data)
    assert pd_data.equals(pd.DataFrame(np_data._source))

def test_table_to_json():
    widget = FakeWidget()
    _table_to_json(widget)

def test_table_to_json_zlib():
    widget = FakeWidget("zlib")
    _table_to_json(widget)

def test_table_to_json_lz4():
    widget = FakeWidget(LZ4Compressor(level=4))
    _table_to_json(widget)

def test_table_to_json_csp(): # with column specific compressors
    widget = FakeWidget({'n': 'zlib', 's': LZ4Compressor(level=4)})
    _table_to_json(widget)

def test_table_from_json():
    assert table_from_json(None, None) == {} # not implemented
