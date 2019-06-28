
__all__ = [
    'BaseError',
    'NoMarketDataException',
    'UninitializedImageError',
    'UniqueOrderIdValidation',
    'InvalidBrokerMarketImage',
    'SystemThrottleError'
]

# -----------------------------------------------------------------------------


class BaseError(Exception):
    """Base class for all exceptions"""
    pass


class NoMarketDataException(BaseError):
    """"Raised when the system couldn't fetch any market data"""
    pass


class UninitializedImageError(BaseError):
    """"Raised when the system couldn't initialize the image"""
    pass


class UniqueOrderIdValidation(BaseError):
    """"Raised when an order_id on active_db or execution_db is duplicated"""
    pass


class InvalidBrokerMarketImage(BaseError):
    """"Raised when a broker couldn't initialize the market image"""
    pass


class SystemThrottleError(BaseError):
    """"Raised when the throttle error is detected"""
    pass

# =============================================================================
