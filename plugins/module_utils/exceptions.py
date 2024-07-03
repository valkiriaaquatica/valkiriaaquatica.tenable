class TenableAPIError(Exception):
    def __init__(self, msg=None, status_code=None):
        super().__init__(msg)
        self.status_code = status_code


# error 401
class AuthenticationError(TenableAPIError):
    pass


# other errors
class UnexpectedAPIResponse(TenableAPIError):
    pass


# error 400
class BadRequestError(TenableAPIError):
    pass
