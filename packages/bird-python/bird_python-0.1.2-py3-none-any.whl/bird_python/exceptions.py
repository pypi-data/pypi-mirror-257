class BaseError(Exception):
    pass


class UnauthorizedError(BaseError):
    pass


class WrongFormatInputError(BaseError):
    pass


class ErrorException(Exception):
    def __init__(self, errors):
        self.errors = errors
        message = " ".join([str(e) for e in self.errors])
        super(ErrorException, self).__init__(message)
