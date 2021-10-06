from warnings import warn

from .source_adapter import SourceAdapter
from .pandas_adapter import PandasAdapter
from .numpy_adapter import NumpyAdapter
from .widgets import TableWidget, EchoTableWidget
from .traitlets import TableType
from .serializers import table_to_json, table_from_json, serialization
from .compressors import ZLibCompressor, LZ4Compressor, DEFAULT_COMPRESSORS
from ._version import __version__
from ._frontend import npm_module_name, npm_package_version

def _jupyter_nbextension_paths():
    """Return metadata for the ipytablewidgets nbextension."""
    return [dict(
        section="notebook",
        # the path is relative to the inner `ipytablewidgets` directory
        src="static",
        # directory in the `nbextension/` namespace
        dest=npm_module_name,
        # _also_ in the `nbextension/` namespace
        require=f"{npm_module_name}/extension")]


def _jupyter_labextension_paths():
    return [{
        "section": "notebook",
        "src": "labextension",
        "dest": npm_module_name,
        "require": f"{npm_module_name}/extension"
    }]


def find_static_assets():
    warn("""To use the ipytablewidgets nbextension, you'll need to update
    the Jupyter notebook to version 4.2 or later.""")
    return []
