# Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021

import numpy as np
import json
from .source_adapter import SourceAdapter
from .compressors import DEFAULT_COMPRESSORS, BaseCompressor
from ipywidgets import widget_serialization, Widget


def array_to_json(value):
    """
    numpy to JSON serializer.
    """
    assert isinstance(value, np.ndarray)
        
    if value.dtype.name == "int64":
        value = value.astype("int32", order="C")
    elif value.dtype.name == "uint64":
        value = value.astype("uint32", order="C")
    elif not value.flags["C_CONTIGUOUS"] and (
        np.issubdtype(value.dtype, np.integer)
        or np.issubdtype(value.dtype, np.floating)
    ):
        value = np.ascontiguousarray(value)
    elif np.issubdtype(value.dtype, str):
        value = value.tolist()
    elif np.issubdtype(value.dtype, object):
        value = list(map(str, value))
    if isinstance(value, list):
        return {"shape": (len(value),), "dtype": "str", "buffer": value}
    return {
        "shape": value.shape,
        "dtype": str(value.dtype),
        "buffer": memoryview(value),
    }


def col_to_json(value, compression):
    assert isinstance(value, np.ndarray)
    json_ = array_to_json(value)
    if compression is None:
        return json_
    arr = json_.get("buffer")
    if (value.dtype == object
       or value.dtype == str
       or value.dtype.name.startswith('str')):
        arr = json.dumps(arr).encode()
    json_["buffer"] = compression.compress(arr)
    json_["compression"] = compression.name
    return json_


def _expand_compressors(compr_dict):
    res = {}
    for k, v in compr_dict.items():
        if isinstance(v, str):
            assert v in DEFAULT_COMPRESSORS
            res[k] = DEFAULT_COMPRESSORS[v]
        else:
            assert v is None or isinstance(v, BaseCompressor)
            res[k] = v
    return res


def table_to_json(value, widget):
    if value is None:
        return None
    if isinstance(value, Widget):
        return widget_serialization['to_json'](value, widget)
    assert isinstance(value, SourceAdapter)
    compression = value._compression or widget.compression
    if isinstance(compression, dict):  # column specific compressors
        compression = _expand_compressors(compression)
        data = {cn: col_to_json(value.to_array(cn),
                                compression.get(cn, None))
                for cn in value.columns}
    else:
        # unique compression for all columns
        if isinstance(compression, str):
            assert compression in DEFAULT_COMPRESSORS
            compression = DEFAULT_COMPRESSORS[compression]
        else:
            assert compression is None or isinstance(compression,
                                                     BaseCompressor)
        data = {
            cn: col_to_json(value.to_array(cn), compression)
            for cn in value.columns
        }
    return dict(columns=list(value.columns), data=data)


def table_from_json(value, widget):
    return {}  # not yet implemented


serialization = dict(to_json=table_to_json, from_json=table_from_json)
