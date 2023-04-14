import os
from urllib.parse import quote_plus as urlquote

from .base import *

elastic_search_url = 'https://{user_name}:{password}@{host_ip}:{host_port}'.format(
    user_name=os.environ.get('ELASTICSEARCH_USERNAME'),
    password=urlquote(os.environ.get('ELASTICSEARCH_PASSWORD')),
    host_ip=os.environ.get('ELASTICSEARCH_HOST_IP'),
    host_port=int(os.environ.get('ELASTICSEARCH_HOST_PORT'))
)

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': [elastic_search_url],
        'ca_certs': os.environ.get('CERTI_PATH'),
    },
}

# Name of the Elasticsearch index
ELASTICSEARCH_INDEX_NAMES = {
    'search_indexes.documents.book': 'book',
    'search_indexes.documents.publisher': 'publisher',
}

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'debug_toolbar_force.middleware.ForceDebugToolbarMiddleware',
)

INSTALLED_APPS += (
    'debug_toolbar',
    'elastic_panel',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

DEBUG_TOOLBAR_PANELS = (
    # Defaults
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    # Additional
    'elastic_panel.panel.ElasticDebugPanel',
)
