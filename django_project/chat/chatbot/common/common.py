import os

class UserInfo:
    user = None

def set_env_if_not_exists(key, value):
    """Sets an environment variable if it doesn't already exist."""
    if key not in os.environ:
        os.environ[key] = value