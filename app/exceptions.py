class ValidationError(ValueError):
    """Base class for invalid user input"""


class FileFormatError(ValidationError): ...


class InvalidJSONError(ValidationError): ...


class InvalidKeywordError(ValidationError): ...
