from os.path import dirname, realpath, join, abspath
from enum import Enum
from data.source_FILE import FILE

APP_DIR = dirname(dirname(realpath(__file__)))
TEMPLATES_DIR = join(dirname(dirname(abspath(__file__))), 'view', 'templates')
STATIC_DIR = join(dirname(dirname(abspath(__file__))), 'view', 'static')
LOGFILE = APP_DIR + '/flask.log'
DEBUG = True


class VocabSource(Enum):
    FILE = 0
    SPARQL = 1
    RVA = 2
    VOCBENCH = 3
    # extend as needed

# Home title
TITLE = 'VocPrez'


#   Instance vocabularies
#
# Here you list the vocabularies that this instance of VocPrez knows about. Note that some vocab data sources, like
# VOCBENCH auto list vocabularies by implementing the list_vocabularies method and thus their vocabularies don't need to
# be listed here. FILE vocabularies too don't need to be listed here as they are automatically picked up by the system
# if the files are added to the data/ folder, as described in the DATA_SOURCES.md documentation file.
VOCABS = {
    'tenement_type': {
        'source': VocabSource.FILE,
        'title': 'ga_igsn-codelist'
    },
}


# extend this intsnace's list of vocabs by using the known sources
VOCABS = {**VOCABS, **FILE.list_vocabularies()}  # picks up all vocab RDF (turtle) files in data/
#VOCABS = {**VOCABS, **VOCBENCH.list_vocabularies()}  # picks up all vocabs at the relevant VocBench instance