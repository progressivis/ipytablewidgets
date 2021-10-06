# Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021

import numpy as np
from ..serializers import col_to_json
from ..compressors import DEFAULT_COMPRESSORS, BaseCompressor
import lz4.frame
import zlib
import json
import pytest

DECOMPRESS = {'lz4': lz4.frame.decompress, 'zlib': zlib.decompress}


def _col_to_json_none(dtype, dtypeout, size):  # no compression
    data = np.arange(size, dtype=dtype)
    json_data = col_to_json(data, None)
    assert json_data == {
        'buffer': memoryview(data),
        'dtype': dtypeout,
        'shape': data.shape,
    }
    assert 'compression' not in json_data


def test_col_to_json_none_float32():
    _col_to_json_none('float32', 'float32', 16)


# method => compression
def _col_to_json_compression(dtype, dtypeout, size, method):
    data = np.arange(size, dtype=dtype)
    compressor = DEFAULT_COMPRESSORS[method]
    json_data = col_to_json(data, compressor).copy()
    json_data['buffer'] = DECOMPRESS[method](json_data['buffer'])
    assert json_data == {
        'buffer': memoryview(data).tobytes(),
        'dtype': dtypeout,
        'shape': data.shape,
        'compression': method
    }


# method => compression
def _col_to_json_compression_str(method):
    raw_data = list('ipytablewidgets')
    data = np.array(raw_data, dtype="str")
    compressor = DEFAULT_COMPRESSORS[method]
    json_data = col_to_json(data, compressor).copy()
    json_data['buffer'] = json.loads(DECOMPRESS[method](json_data['buffer']))
    assert json_data == {
        'buffer': raw_data,
        'dtype': 'str',
        'shape': data.shape,
        'compression': method
    }


def test_col_to_json_lz4_float32():
    _col_to_json_compression('float32', 'float32', 16, 'lz4')


def test_col_to_json_lz4_str():
    _col_to_json_compression_str('lz4')


def test_col_to_json_zlib_float32():
    _col_to_json_compression('float32', 'float32', 16, 'zlib')


def test_col_to_json_zlib_str():
    _col_to_json_compression_str('zlib')


class FakeCompressor(BaseCompressor):
    def compress(self, data):
        ...
    ...


def test_fake_compressor_name():
    fc = FakeCompressor()
    fc.compress(None)
    with pytest.raises(NotImplementedError):
        fc.name
