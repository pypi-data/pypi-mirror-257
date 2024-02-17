from . import _version
import pyolite
import pyodide

__version__ = _version.get_versions()['version']

def pyoliteutilsinfo():
    print("pyoliteutils=", __version__, "pyodide=", pyodide.__version__, "pyolite=", pyolite.__version__)