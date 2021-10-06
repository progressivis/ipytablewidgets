# Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021

import numpy as np
import pandas as pd
from ..pandas_adapter import PandasAdapter
from ..numpy_adapter import NumpyAdapter
from ..widgets import TableWidget


def test_table_type_touch_mode():
    list_ = list('ipytablewidgets')
    arr_s = np.array(list_, dtype=str)
    arr_n = np.arange(len(list_), dtype='float32')
    pd_data = PandasAdapter(pd.DataFrame({'s': arr_s, 'n': arr_n}),
                            touch_mode=True)
    tw = TableWidget(pd_data)
    assert not pd_data.is_touched
    pd_data.touch()
    assert pd_data.is_touched
    tw._table = pd_data
    assert not pd_data.is_touched


def test_table_type_no_touch_mode():
    list_ = list('ipytablewidgets')
    arr_s = np.array(list_, dtype=str)
    arr_n = np.arange(len(list_), dtype='float32')
    pd_data = PandasAdapter(pd.DataFrame({'s': arr_s, 'n': arr_n}))
    tw = TableWidget(pd_data)
    np_data = NumpyAdapter({'s': arr_s, 'n': arr_n})
    tw._table = np_data
