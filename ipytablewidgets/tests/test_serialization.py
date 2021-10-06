# Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021

import numpy as np
from ..serializers import array_to_json


def _array_to_json_dtype(dtype, dtypeout, size):
    data = np.arange(size, dtype=dtype)
    json_data = array_to_json(data)
    assert json_data == {
        'buffer': memoryview(data),
        'dtype': dtypeout,
        'shape': (size,),
    }


def test_array_to_json_float32():
    _array_to_json_dtype('float32', 'float32', 16)


def test_array_to_json_int32():
    _array_to_json_dtype('int32', 'int32', 16)


def test_array_to_json_uint32():
    _array_to_json_dtype('uint32', 'uint32', 16)


def test_array_to_json_int64():
    _array_to_json_dtype('int64', 'int32', 16)


def test_array_to_json_uint64():
    _array_to_json_dtype('uint64', 'uint32', 16)


def test_array_to_json_2d():
    dtype, dtypeout, size = 'int32', 'int32', 16
    data = np.arange(size*2, dtype=dtype).reshape(size, -1)
    json_data = array_to_json(data)
    assert json_data == {
        'buffer': memoryview(data),
        'dtype': dtypeout,
        'shape': data.shape,
    }


def test_array_to_json_2d_f():
    dtype, dtypeout, size = 'int32', 'int32', 16
    data = np.arange(size*2, dtype=dtype).reshape(size, -1, order='F')
    json_data = array_to_json(data)
    assert json_data == {
        'buffer': memoryview(data),
        'dtype': dtypeout,
        'shape': data.shape,
    }


def _array_to_json_other(dtype):
    list_ = list('ipytablewidgets')
    data = np.array(list_, dtype=dtype)
    json_data = array_to_json(data)
    assert json_data == {
        'buffer': data.tolist(),
        'dtype': "str",
        'shape': data.shape,
    }


def test_array_to_json_str():
    _array_to_json_other('str')


def test_array_to_json_object():
    _array_to_json_other('object')
