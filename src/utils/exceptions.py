class BankingError(Exception):
    """Base exception for Montcrest Bank."""
    pass


class InvalidAmountError(BankingError):
    """Raised when an amount is invalid."""
    pass


class InsufficientBalanceError(BankingError):
    """Raised when an account has insufficient funds."""
    pass


class AccountInactiveError(BankingError):
    """Raised when an operation is attempted on an inactive account."""
    pass