import os

class UserInfo:
    """Class to asynchronously obtain the current user's details from channels."""
    user = None

class ChatInfo:
    """Class to asynchronously obtain the current user's chat thread from channels."""
    chat_thread_id = None

def set_env_if_not_exists(key, value):
    """Sets an environment variable if it doesn't already exist."""
    if key not in os.environ:
        os.environ[key] = value