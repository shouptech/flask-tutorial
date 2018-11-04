class Error(Exception):
    """Base class for exceptions"""
    pass

class ConfigError(Error):
    """Raised when a needed configuration is missing"""
    pass
