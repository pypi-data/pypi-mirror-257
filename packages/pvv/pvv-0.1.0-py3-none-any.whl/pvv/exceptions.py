class PvvException(BaseException):
    """pvv base exception"""

    pass


class ValidatorError(PvvException):
    """ValidatorError

    Raised when input parameters to a validator are incorrect
    """

    pass
