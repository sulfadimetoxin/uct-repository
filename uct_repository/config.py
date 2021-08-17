import os

from flask_babelex import lazy_gettext as _
from datetime import timedelta

# Database
# ========
#: Database URI including user and password
# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://uct-repository:uct-repository@localhost/uct-repository'

PIDSTORE_RECID_FIELD = 'id'
JSONSCHEMAS_HOST = 'localhost'
SUPPORTED_LANGUAGES = ['cs', 'en', '_']

BABEL_DEFAULT_LOCALE = 'cs'
I18N_LANGUAGES = (('en', _('English')), ('cs', _('Czech')))
I18N_SESSION_KEY = 'language'
I18N_SET_LANGUAGE_URL = '/api/lang'

ELASTICSEARCH_DEFAULT_LANGUAGE_TEMPLATE = {
    "type": "text",
    "fields": {
        "raw": {
            "type": "keyword"
        }
    }
}

INDEXER_RECORD_TO_INDEX = 'uct_repository.indexer:record_to_index'

# hack to serve schemas both on jsonschemas host and server name (if they differ)
import jsonresolver


@jsonresolver.hookimpl
def jsonresolver_loader(url_map):
    """JSON resolver plugin that loads the schema endpoint.

    Injected into Invenio-Records JSON resolver.
    """
    from flask import current_app
    from invenio_jsonschemas import current_jsonschemas
    from werkzeug.routing import Rule
    url_map.add(Rule(
        "{0}/<path:path>".format(current_app.config['JSONSCHEMAS_ENDPOINT']),
        endpoint=current_jsonschemas.get_schema,
        host=current_app.config['SERVER_NAME']))


FILES_REST_STORAGE_FACTORY = 'oarepo_s3.storage.s3_storage_factory'
CELERY_BEAT_SCHEDULE = {
    'cleanup_expired_multipart_uploads': {
        'task': 'oarepo_s3.tasks.cleanup_expired_multipart_uploads',
        'schedule': timedelta(minutes=60 * 24),
    }
}

REST_CSRF_ENABLED = False
CSRF_HEADER = 'X-CSRFTOKEN'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_PATH = '/'

OAISERVER_ID_PREFIX = 'oai:localhost'
MAIL_SUPPRESS_SEND = os.environ.get('FLASK_DEBUG', False)

S3_TENANT='uct_repository_test$uct_repository_test'  # TODO: change me
S3_SIGNATURE_VERSION='s3'
S3_ENDPOINT_URL='https://cis-rgw.vscht.cz'  # TODO: change me
S3_ACCESS_KEY_ID='0YRJO96LSUYA79O8S4DO'  # TODO: change me
S3_SECRET_ACCESS_KEY='XWTsxLvpEfTCsiRRgT6V8ik2q3b08cjHHHa3co95'  # TODO: change me
