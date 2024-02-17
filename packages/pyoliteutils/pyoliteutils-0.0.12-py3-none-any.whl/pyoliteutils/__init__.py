from .pyoliteutils import load_file_into_in_mem_filesystem, get_file_from_url
from .mermaid import mm
from .kroki import kroki, plantuml, ditaa, graphviz, mermaid
from .lessonsurvey import lessonsurvey
from .wordcloud import wordcloud

from . import _version
__version__ = _version.get_versions()['version']
