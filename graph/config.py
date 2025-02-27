import os
from pyhocon import ConfigFactory

conf = None


def get(key, default=None):
    try:
        global conf
        return conf.get(key, default)
    except AttributeError as aex:
        return default


mandatory_confs = [
    "elasticsearch.hostname",
    "data.filedir",
    "data.version",
]

conf_dir = os.path.abspath(os.path.dirname(__file__))
conf_path = os.path.join(conf_dir, 'config.json')
conf = ConfigFactory.parse_file(conf_path)
conf.put('elasticsearch.hostname', os.getenv('ELASTICSEARCH_URL', conf.get('elasticsearch.hostname')))
for key in mandatory_confs:
    assert key in conf, "Key %s down not exists" % key
