import os

# placeholder for a required APP_CONF value that has no default
UNSET_REQUIRED_VALUE='NOT-SET'

# Default env var
DEFAULT_ENV = {
    'DEBUG': "false",
    'DB_HOST': UNSET_REQUIRED_VALUE,
    'DB_USER': UNSET_REQUIRED_VALUE,
    'DB_PASS': UNSET_REQUIRED_VALUE,
    'DB_PORT': 27017,
    'DB_NAME': UNSET_REQUIRED_VALUE,
    'HOST_IP': '0.0.0.0',
    'PORT': 3000
}

APP_CONF = {}

# loads env var, raises exception if any
# required values are not defined
for key, default in DEFAULT_ENV.items():
    value = os.getenv(key, default)
    if value == UNSET_REQUIRED_VALUE:
        raise Exception(f"{key} is required to be set")
    APP_CONF[key] = value
