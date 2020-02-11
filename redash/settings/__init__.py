#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import importlib
import ssl
from funcy import distinct, remove
from flask_talisman import talisman

from .helpers import fix_assets_path, array_from_string, parse_boolean, int_or_none, set_from_string
from .organization import DATE_FORMAT, TIME_FORMAT  # noqa

# ==========Redis配置==========start
# Redis访问地址
REDIS_URL = os.environ.get('REDASH_REDIS_URL', os.environ.get('REDIS_URL', "redis://127.0.0.1:6379/0"))
# 代理服务器数
PROXIES_COUNT = int(os.environ.get('REDASH_PROXIES_COUNT', "1"))
# ==========Redis配置==========end

# ==========StatsD配置==========start
# StatsD的地址
STATSD_HOST = os.environ.get('REDASH_STATSD_HOST', "127.0.0.1")
# StatsD端口号
STATSD_PORT = int(os.environ.get('REDASH_STATSD_PORT', "8125"))
# StatsD前缀
STATSD_PREFIX = os.environ.get('REDASH_STATSD_PREFIX', "redash")
# 是否将标记与StatsD指标一起使用
STATSD_USE_TAGS = parse_boolean(os.environ.get('REDASH_STATSD_USE_TAGS', "false"))
# ==========StatsD配置==========end

# ==========数据库配置==========start
# 用于连接数据的数据库
# SQLALCHEMY_DATABASE_URI = os.environ.get("REDASH_DATABASE_URL", os.environ.get('DATABASE_URL', "postgresql:///postgres"))
SQLALCHEMY_DATABASE_URI = os.environ.get("REDASH_DATABASE_URL", os.environ.get('DATABASE_URL', "postgresql://postgres:Beidas0ft@localhost:5432/postgres"))
# 控制在连接池达到最大值后可以创建的连接数。当这些额外的 连接回收到连接池后将会被断开和抛弃。
SQLALCHEMY_MAX_OVERFLOW = int_or_none(os.environ.get("SQLALCHEMY_MAX_OVERFLOW"))
# 数据库连接池的大小。默认是数据库引擎的默认值 （通常是 5）。
SQLALCHEMY_POOL_SIZE = int_or_none(os.environ.get("SQLALCHEMY_POOL_SIZE"))
SQLALCHEMY_DISABLE_POOL = parse_boolean(os.environ.get("SQLALCHEMY_DISABLE_POOL", "false"))
# 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 如果设置成 True，SQLAlchemy 将会记录所有 发到标准输出(stderr)的语句，这对调试很有帮助。
SQLALCHEMY_ECHO = False
# ==========数据库配置==========end

# ==========Celery配置==========start
# Celery的Broker，默认值是REDIS_URL的值
CELERY_BROKER = os.environ.get("REDASH_CELERY_BROKER", REDIS_URL)
CELERY_RESULT_BACKEND = os.environ.get("REDASH_CELERY_RESULT_BACKEND", os.environ.get("REDASH_CELERY_BACKEND", CELERY_BROKER))
CELERY_RESULT_EXPIRES = int(os.environ.get("REDASH_CELERY_RESULT_EXPIRES", os.environ.get("REDASH_CELERY_TASK_RESULT_EXPIRES", 3600 * 4)))
CELERY_INIT_TIMEOUT = int(os.environ.get("REDASH_CELERY_INIT_TIMEOUT", 10))
CELERY_BROKER_USE_SSL = CELERY_BROKER.startswith('rediss')
CELERY_SSL_CONFIG = {
    'ssl_cert_reqs': int(os.environ.get("REDASH_CELERY_BROKER_SSL_CERT_REQS",  ssl.CERT_OPTIONAL)),
    'ssl_ca_certs': os.environ.get("REDASH_CELERY_BROKER_SSL_CA_CERTS"),
    'ssl_certfile': os.environ.get("REDASH_CELERY_BROKER_SSL_CERTFILE"),
    'ssl_keyfile': os.environ.get("REDASH_CELERY_BROKER_SSL_KEYFILE"),
} if CELERY_BROKER_USE_SSL else None

CELERY_WORKER_PREFETCH_MULTIPLIER = int(os.environ.get("REDASH_CELERY_WORKER_PREFETCH_MULTIPLIER", 1))
CELERY_ACCEPT_CONTENT = os.environ.get("REDASH_CELERY_ACCEPT_CONTENT", "json").split(",")
CELERY_TASK_SERIALIZER = os.environ.get("REDASH_CELERY_TASK_SERIALIZER", "json")
CELERY_RESULT_SERIALIZER = os.environ.get("REDASH_CELERY_RESULT_SERIALIZER", "json")
# ==========Celery配置==========end

# 通过以下操作，可以定期（每5分钟）删除未使用的查询结果。
# 删除超过QUERY_RESULTS_CLEANUP_MAX_AGE设置天数的查询
QUERY_RESULTS_CLEANUP_ENABLED = parse_boolean(os.environ.get("REDASH_QUERY_RESULTS_CLEANUP_ENABLED", "true"))
# 删除超过QUERY_RESULTS_CLEANUP_MAX_AGE设置天数的查询时的最大删除次数
QUERY_RESULTS_CLEANUP_COUNT = int(os.environ.get("REDASH_QUERY_RESULTS_CLEANUP_COUNT", "100"))
# 删除超过指定值的查询结果，默认值：（ 7单位：天）
QUERY_RESULTS_CLEANUP_MAX_AGE = int(os.environ.get("REDASH_QUERY_RESULTS_CLEANUP_MAX_AGE", "7"))

# 数据源模式检索间隔
SCHEMAS_REFRESH_SCHEDULE = int(os.environ.get("REDASH_SCHEMAS_REFRESH_SCHEDULE", 30))
SCHEMAS_REFRESH_QUEUE = os.environ.get("REDASH_SCHEMAS_REFRESH_QUEUE", "celery")

#  API的认证方法api_key，hmac，password的一个
AUTH_TYPE = os.environ.get("REDASH_AUTH_TYPE", "api_key")
# 新用户邀请令牌的到期时间
INVITATION_TOKEN_MAX_AGE = int(os.environ.get("REDASH_INVITATION_TOKEN_MAX_AGE", 60 * 60 * 24 * 7))

# 在Flask应用中用于各种加密功能的秘密密钥
SECRET_KEY = os.environ.get("REDASH_COOKIE_SECRET", "c292a0a3aa32397cdb050e233733900f")
# 加密数据源选项时使用的密钥
DATASOURCE_SECRET_KEY = os.environ.get('REDASH_SECRET_KEY', SECRET_KEY)

# 是否将非HTTP请求重定向到HTTPS。 默认禁用。
ENFORCE_HTTPS = parse_boolean(os.environ.get("REDASH_ENFORCE_HTTPS", "false"))
ENFORCE_HTTPS_PERMANENT = parse_boolean(os.environ.get("REDASH_ENFORCE_HTTPS_PERMANENT", "false"))
# 是否强制执行文件下载
ENFORCE_FILE_SAVE = parse_boolean(os.environ.get("REDASH_ENFORCE_FILE_SAVE", "true"))

# 默认情况下是否使用安全cookie。
COOKIES_SECURE = parse_boolean(os.environ.get("REDASH_COOKIES_SECURE", str(ENFORCE_HTTPS)))
# 会话cookie是否设置为安全。
SESSION_COOKIE_SECURE = parse_boolean(os.environ.get("REDASH_SESSION_COOKIE_SECURE") or str(COOKIES_SECURE))
# 会话cookie是否设置为HttpOnly
SESSION_COOKIE_HTTPONLY = parse_boolean(os.environ.get("REDASH_SESSION_COOKIE_HTTPONLY", "true"))
# 会话cookie是否设置为安全。
REMEMBER_COOKIE_SECURE = parse_boolean(os.environ.get("REDASH_REMEMBER_COOKIE_SECURE") or str(COOKIES_SECURE))
# 是否记住cookie设置为HttpOnly
REMEMBER_COOKIE_HTTPONLY = parse_boolean(os.environ.get("REDASH_REMEMBER_COOKIE_HTTPONLY", "true"))

# 默认情况下不设置X-Frame-Options，因为它高度依赖于特定的部署。
# 参考 https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
FRAME_OPTIONS = os.environ.get("REDASH_FRAME_OPTIONS", "deny")
FRAME_OPTIONS_ALLOW_FROM = os.environ.get("REDASH_FRAME_OPTIONS_ALLOW_FROM", "")

# 是否以及如何发送Strict-Transport-Security响应标头。
# See https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security
HSTS_ENABLED = parse_boolean(os.environ.get("REDASH_HSTS_ENABLED") or str(ENFORCE_HTTPS))
HSTS_PRELOAD = parse_boolean(os.environ.get("REDASH_HSTS_PRELOAD", "false"))
HSTS_MAX_AGE = int(os.environ.get("REDASH_HSTS_MAX_AGE", talisman.ONE_YEAR_IN_SECS))
HSTS_INCLUDE_SUBDOMAINS = parse_boolean(os.environ.get("REDASH_HSTS_INCLUDE_SUBDOMAINS", "false"))

# Whether and how to send Content-Security-Policy response headers.
# See https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy
# for more information.
# Overriding this value via an environment variables requires setting it
# as a string in the general CSP format of a semicolon separated list of
# individual CSP directives, see https://github.com/GoogleCloudPlatform/flask-talisman#example-7
# for more information. E.g.:
CONTENT_SECURITY_POLICY = os.environ.get(
    "REDASH_CONTENT_SECURITY_POLICY",
    "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-eval'; font-src 'self' data:; img-src 'self' http: https: data:; object-src 'none'; frame-ancestors 'none'; frame-src redash.io;"
)
CONTENT_SECURITY_POLICY_REPORT_URI = os.environ.get("REDASH_CONTENT_SECURITY_POLICY_REPORT_URI", "")
CONTENT_SECURITY_POLICY_REPORT_ONLY = parse_boolean(os.environ.get("REDASH_CONTENT_SECURITY_POLICY_REPORT_ONLY", "false"))
CONTENT_SECURITY_POLICY_NONCE_IN = array_from_string(os.environ.get("REDASH_CONTENT_SECURITY_POLICY_NONCE_IN", ""))

# Whether and how to send Referrer-Policy response headers. Defaults to
# 'strict-origin-when-cross-origin'.
# See https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy
# for more information.
REFERRER_POLICY = os.environ.get("REDASH_REFERRER_POLICY", "strict-origin-when-cross-origin")
# Whether and how to send Feature-Policy response headers. Defaults to
# an empty value.
# See https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Feature-Policy
# for more information.
FEATURE_POLICY = os.environ.get("REDASH_REFERRER_POLICY", "")

MULTI_ORG = parse_boolean(os.environ.get("REDASH_MULTI_ORG", "false"))

GOOGLE_CLIENT_ID = os.environ.get("REDASH_GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("REDASH_GOOGLE_CLIENT_SECRET", "")
GOOGLE_OAUTH_ENABLED = bool(GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET)

# Enables the use of an externally-provided and trusted remote user via an HTTP
# header.  The "user" must be an email address.
#
# By default the trusted header is X-Forwarded-Remote-User.  You can change
# this by setting REDASH_REMOTE_USER_HEADER.
#
# Enabling this authentication method is *potentially dangerous*, and it is
# your responsibility to ensure that only a trusted frontend (usually on the
# same server) can talk to the redash backend server, otherwise people will be
# able to login as anyone they want by directly talking to the redash backend.
# You must *also* ensure that any special header in the original request is
# removed or always overwritten by your frontend, otherwise your frontend may
# pass it through to the backend unchanged.
#
# Note that redash will only check the remote user once, upon the first need
# for a login, and then set a cookie which keeps the user logged in.  Dropping
# the remote user header after subsequent requests won't automatically log the
# user out.  Doing so could be done with further work, but usually it's
# unnecessary.
#
# If you also set the organization setting auth_password_login_enabled to false,
# then your authentication will be seamless.  Otherwise a link will be presented
# on the login page to trigger remote user auth.
REMOTE_USER_LOGIN_ENABLED = parse_boolean(os.environ.get("REDASH_REMOTE_USER_LOGIN_ENABLED", "false"))
REMOTE_USER_HEADER = os.environ.get("REDASH_REMOTE_USER_HEADER", "X-Forwarded-Remote-User")

# If the organization setting auth_password_login_enabled is not false, then users will still be
# able to login through Redash instead of the LDAP server
LDAP_LOGIN_ENABLED = parse_boolean(os.environ.get('REDASH_LDAP_LOGIN_ENABLED', 'false'))
# Bind LDAP using SSL. Default is False
LDAP_SSL = parse_boolean(os.environ.get('REDASH_LDAP_USE_SSL', 'false'))
# Choose authentication method(SIMPLE, ANONYMOUS or NTLM). Default is SIMPLE
LDAP_AUTH_METHOD = os.environ.get('REDASH_LDAP_AUTH_METHOD', 'SIMPLE')
# The LDAP directory address (ex. ldap://10.0.10.1:389)
LDAP_HOST_URL = os.environ.get('REDASH_LDAP_URL', None)
# The DN & password used to connect to LDAP to determine the identity of the user being authenticated.
# For AD this should be "org\\user".
LDAP_BIND_DN = os.environ.get('REDASH_LDAP_BIND_DN', None)
LDAP_BIND_DN_PASSWORD = os.environ.get('REDASH_LDAP_BIND_DN_PASSWORD', '')
# AD/LDAP email and display name keys
LDAP_DISPLAY_NAME_KEY = os.environ.get('REDASH_LDAP_DISPLAY_NAME_KEY', 'displayName')
LDAP_EMAIL_KEY = os.environ.get('REDASH_LDAP_EMAIL_KEY', "mail")
# Prompt that should be shown above username/email field.
LDAP_CUSTOM_USERNAME_PROMPT = os.environ.get('REDASH_LDAP_CUSTOM_USERNAME_PROMPT', 'LDAP/AD/SSO username:')
# LDAP Search DN TEMPLATE (for AD this should be "(sAMAccountName=%(username)s)"")
LDAP_SEARCH_TEMPLATE = os.environ.get('REDASH_LDAP_SEARCH_TEMPLATE', '(cn=%(username)s)')
# The schema to bind to (ex. cn=users,dc=ORG,dc=local)
LDAP_SEARCH_DN = os.environ.get('REDASH_LDAP_SEARCH_DN', os.environ.get('REDASH_SEARCH_DN'))

STATIC_ASSETS_PATH = fix_assets_path(os.environ.get("REDASH_STATIC_ASSETS_PATH", "../client/dist/"))

# 最长的工作时间
JOB_EXPIRY_TIME = int(os.environ.get("REDASH_JOB_EXPIRY_TIME", 3600 * 12))

LOG_LEVEL = os.environ.get("REDASH_LOG_LEVEL", "INFO")
LOG_STDOUT = parse_boolean(os.environ.get('REDASH_LOG_STDOUT', 'false'))
LOG_PREFIX = os.environ.get('REDASH_LOG_PREFIX', '')
LOG_FORMAT = os.environ.get('REDASH_LOG_FORMAT', LOG_PREFIX + '[%(asctime)s][PID:%(process)d][%(levelname)s][%(name)s] %(message)s')
CELERYD_WORKER_LOG_FORMAT = os.environ.get(
    "REDASH_CELERYD_WORKER_LOG_FORMAT",
    os.environ.get('REDASH_CELERYD_LOG_FORMAT',
                   LOG_PREFIX + '[%(asctime)s][PID:%(process)d][%(levelname)s][%(processName)s] %(message)s'))
CELERYD_WORKER_TASK_LOG_FORMAT = os.environ.get(
    "REDASH_CELERYD_WORKER_TASK_LOG_FORMAT",
    os.environ.get('REDASH_CELERYD_TASK_LOG_FORMAT',
                   (LOG_PREFIX + '[%(asctime)s][PID:%(process)d][%(levelname)s][%(processName)s] '
                    'task_name=%(task_name)s '
                    'task_id=%(task_id)s %(message)s')))

# 邮件设置:
MAIL_SERVER = os.environ.get('REDASH_MAIL_SERVER', 'smtp.263.net')
MAIL_PORT = int(os.environ.get('REDASH_MAIL_PORT', 465))
MAIL_USE_TLS = parse_boolean(os.environ.get('REDASH_MAIL_USE_TLS', 'false'))
MAIL_USE_SSL = parse_boolean(os.environ.get('REDASH_MAIL_USE_SSL', 'true'))
MAIL_USERNAME = os.environ.get('REDASH_MAIL_USERNAME', 'hexm@beidasoft.com')
MAIL_PASSWORD = os.environ.get('REDASH_MAIL_PASSWORD', 'Bkagy0h0')
MAIL_DEFAULT_SENDER = os.environ.get('REDASH_MAIL_DEFAULT_SENDER', 'hexm@beidasoft.com')
MAIL_MAX_EMAILS = os.environ.get('REDASH_MAIL_MAX_EMAILS', None)
MAIL_ASCII_ATTACHMENTS = parse_boolean(os.environ.get('REDASH_MAIL_ASCII_ATTACHMENTS', 'false'))


def email_server_is_configured():
    return MAIL_DEFAULT_SENDER is not None


HOST = os.environ.get('REDASH_HOST', '')

SEND_FAILURE_EMAIL_INTERVAL = int(os.environ.get('REDASH_SEND_FAILURE_EMAIL_INTERVAL', 60))
MAX_FAILURE_REPORTS_PER_QUERY = int(os.environ.get('REDASH_MAX_FAILURE_REPORTS_PER_QUERY', 100))

ALERTS_DEFAULT_MAIL_SUBJECT_TEMPLATE = os.environ.get('REDASH_ALERTS_DEFAULT_MAIL_SUBJECT_TEMPLATE', "({state}) {alert_name}")

# How many requests are allowed per IP to the login page before
# being throttled?
# See https://flask-limiter.readthedocs.io/en/stable/#rate-limit-string-notation

RATELIMIT_ENABLED = parse_boolean(os.environ.get('REDASH_RATELIMIT_ENABLED', 'true'))
THROTTLE_LOGIN_PATTERN = os.environ.get('REDASH_THROTTLE_LOGIN_PATTERN', '50/hour')
LIMITER_STORAGE = os.environ.get("REDASH_LIMITER_STORAGE", REDIS_URL)

# CORS settings for the Query Result API (and possbily future external APIs).
# In most cases all you need to do is set REDASH_CORS_ACCESS_CONTROL_ALLOW_ORIGIN
# to the calling domain (or domains in a comma separated list).
ACCESS_CONTROL_ALLOW_ORIGIN = set_from_string(os.environ.get("REDASH_CORS_ACCESS_CONTROL_ALLOW_ORIGIN", ""))
ACCESS_CONTROL_ALLOW_CREDENTIALS = parse_boolean(os.environ.get("REDASH_CORS_ACCESS_CONTROL_ALLOW_CREDENTIALS", "false"))
ACCESS_CONTROL_REQUEST_METHOD = os.environ.get("REDASH_CORS_ACCESS_CONTROL_REQUEST_METHOD", "GET, POST, PUT")
ACCESS_CONTROL_ALLOW_HEADERS = os.environ.get("REDASH_CORS_ACCESS_CONTROL_ALLOW_HEADERS", "Content-Type")

# Query Runners
default_query_runners = [
    'redash.query_runner.athena',
    'redash.query_runner.big_query',
    'redash.query_runner.google_spreadsheets',
    'redash.query_runner.graphite',
    'redash.query_runner.mongodb',
    'redash.query_runner.couchbase',
    'redash.query_runner.mysql',
    'redash.query_runner.pg',
    'redash.query_runner.url',
    'redash.query_runner.influx_db',
    'redash.query_runner.elasticsearch',
    'redash.query_runner.amazon_elasticsearch',
    'redash.query_runner.presto',
    'redash.query_runner.databricks',
    'redash.query_runner.hive_ds',
    'redash.query_runner.impala_ds',
    'redash.query_runner.vertica',
    'redash.query_runner.clickhouse',
    'redash.query_runner.yandex_metrica',
    'redash.query_runner.rockset',
    'redash.query_runner.treasuredata',
    'redash.query_runner.sqlite',
    'redash.query_runner.dynamodb_sql',
    'redash.query_runner.mssql',
    'redash.query_runner.memsql_ds',
    'redash.query_runner.mapd',
    'redash.query_runner.jql',
    'redash.query_runner.google_analytics',
    'redash.query_runner.axibase_tsd',
    'redash.query_runner.salesforce',
    'redash.query_runner.query_results',
    'redash.query_runner.prometheus',
    'redash.query_runner.qubole',
    'redash.query_runner.db2',
    'redash.query_runner.druid',
    'redash.query_runner.kylin',
    'redash.query_runner.drill',
    'redash.query_runner.uptycs',
    'redash.query_runner.snowflake',
    'redash.query_runner.phoenix',
    'redash.query_runner.json_ds',
    'redash.query_runner.cass',
    'redash.query_runner.dgraph',
    'redash.query_runner.azure_kusto',
]

enabled_query_runners = array_from_string(os.environ.get("REDASH_ENABLED_QUERY_RUNNERS", ",".join(default_query_runners)))
additional_query_runners = array_from_string(os.environ.get("REDASH_ADDITIONAL_QUERY_RUNNERS", ""))
disabled_query_runners = array_from_string(os.environ.get("REDASH_DISABLED_QUERY_RUNNERS", ""))

QUERY_RUNNERS = remove(set(disabled_query_runners), distinct(enabled_query_runners + additional_query_runners))

dynamic_settings = importlib.import_module(os.environ.get('REDASH_DYNAMIC_SETTINGS_MODULE', 'redash.settings.dynamic_settings'))

# Destinations
default_destinations = [
    'redash.destinations.email',
    'redash.destinations.slack',
    'redash.destinations.webhook',
    'redash.destinations.hipchat',
    'redash.destinations.mattermost',
    'redash.destinations.chatwork',
    'redash.destinations.pagerduty',
    'redash.destinations.hangoutschat'
]

enabled_destinations = array_from_string(os.environ.get("REDASH_ENABLED_DESTINATIONS", ",".join(default_destinations)))
additional_destinations = array_from_string(os.environ.get("REDASH_ADDITIONAL_DESTINATIONS", ""))

DESTINATIONS = distinct(enabled_destinations + additional_destinations)

EVENT_REPORTING_WEBHOOKS = array_from_string(os.environ.get("REDASH_EVENT_REPORTING_WEBHOOKS", ""))

# Support for Sentry (https://getsentry.com/). Just set your Sentry DSN to enable it:
SENTRY_DSN = os.environ.get("REDASH_SENTRY_DSN", "")

# Client side toggles:
ALLOW_SCRIPTS_IN_USER_INPUT = parse_boolean(os.environ.get("REDASH_ALLOW_SCRIPTS_IN_USER_INPUT", "false"))
DASHBOARD_REFRESH_INTERVALS = map(int, array_from_string(os.environ.get("REDASH_DASHBOARD_REFRESH_INTERVALS", "60,300,600,1800,3600,43200,86400")))
QUERY_REFRESH_INTERVALS = map(int, array_from_string(os.environ.get("REDASH_QUERY_REFRESH_INTERVALS", "60, 300, 600, 900, 1800, 3600, 7200, 10800, 14400, 18000, 21600, 25200, 28800, 32400, 36000, 39600, 43200, 86400, 604800, 1209600, 2592000")))
PAGE_SIZE = int(os.environ.get('REDASH_PAGE_SIZE', 20))
PAGE_SIZE_OPTIONS = map(int, array_from_string(os.environ.get("REDASH_PAGE_SIZE_OPTIONS", "5,10,20,50,100")))
TABLE_CELL_MAX_JSON_SIZE = int(os.environ.get('REDASH_TABLE_CELL_MAX_JSON_SIZE', 50000))

# Features:
VERSION_CHECK = parse_boolean(os.environ.get("REDASH_VERSION_CHECK", "true"))
FEATURE_DISABLE_REFRESH_QUERIES = parse_boolean(os.environ.get("REDASH_FEATURE_DISABLE_REFRESH_QUERIES", "false"))
FEATURE_SHOW_QUERY_RESULTS_COUNT = parse_boolean(os.environ.get("REDASH_FEATURE_SHOW_QUERY_RESULTS_COUNT", "true"))
FEATURE_ALLOW_CUSTOM_JS_VISUALIZATIONS = parse_boolean(os.environ.get("REDASH_FEATURE_ALLOW_CUSTOM_JS_VISUALIZATIONS", "false"))
FEATURE_AUTO_PUBLISH_NAMED_QUERIES = parse_boolean(os.environ.get("REDASH_FEATURE_AUTO_PUBLISH_NAMED_QUERIES", "true"))
FEATURE_EXTENDED_ALERT_OPTIONS = parse_boolean(os.environ.get("REDASH_FEATURE_EXTENDED_ALERT_OPTIONS", "false"))

# BigQuery
BIGQUERY_HTTP_TIMEOUT = int(os.environ.get("REDASH_BIGQUERY_HTTP_TIMEOUT", "600"))

# Allow Parameters in Embeds
# WARNING: Deprecated!
# See https://discuss.redash.io/t/support-for-parameters-in-embedded-visualizations/3337 for more details.
ALLOW_PARAMETERS_IN_EMBEDS = parse_boolean(os.environ.get("REDASH_ALLOW_PARAMETERS_IN_EMBEDS", "false"))

# 增强架构获取
SCHEMA_RUN_TABLE_SIZE_CALCULATIONS = parse_boolean(os.environ.get("REDASH_SCHEMA_RUN_TABLE_SIZE_CALCULATIONS", "false"))

# kylin
KYLIN_OFFSET = int(os.environ.get('REDASH_KYLIN_OFFSET', 0))
KYLIN_LIMIT = int(os.environ.get('REDASH_KYLIN_LIMIT', 50000))
KYLIN_ACCEPT_PARTIAL = parse_boolean(os.environ.get("REDASH_KYLIN_ACCEPT_PARTIAL", "false"))

# sqlparse
SQLPARSE_FORMAT_OPTIONS = {
    'reindent': parse_boolean(os.environ.get('SQLPARSE_FORMAT_REINDENT', 'true')),
    'keyword_case': os.environ.get('SQLPARSE_FORMAT_KEYWORD_CASE', 'upper'),
}
