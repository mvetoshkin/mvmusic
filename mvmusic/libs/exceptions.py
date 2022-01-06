class AppException(Exception):
    pass


class NoSettingsModuleSpecified(Exception):
    pass


class NoBlueprintException(Exception):
    pass


class NoConverterException(Exception):
    pass


class NoExtensionException(Exception):
    pass


###

class AppValueError(AppException):
    pass


class ModelKeyError(AppException):
    pass


###

class AccessDeniedError(AppException):
    pass


class BadRequestError(AppException):
    pass


class NotAllowedError(AppException):
    pass


class NotFoundError(AppException):
    pass


class UnauthorizedError(AppException):
    pass
