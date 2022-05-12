from functools import wraps
from flask import Flask


def ensure_sync_wrapper(app: Flask):
    def dec(func):
        def wrapper(*args, **kwargs):
            return app.async_to_sync(func)(*args, **kwargs)
        return wrapper
    return dec
