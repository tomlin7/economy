"""
errors are handled here.
"""


class Error(Exception):
    """Base class for other exceptions"""
    pass


class HasJobError(Error):
    pass


class UserNotFound(Error):
    pass
