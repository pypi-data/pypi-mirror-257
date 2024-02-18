class PydanticWranglerBaseException(Exception):
    """Parent class for all pydantic_wrangler exceptions."""


class ModelInitializationError(PydanticWranglerBaseException):
    """Model instantiation not possible."""


class PydanticWranglerTypeError(PydanticWranglerBaseException):
    """Data received is of the wrong type"""


class RenderableTemplateError(PydanticWranglerBaseException):
    """An error occurred while trying to render a RenderablePydanticWranglerModel"""


class ModelDoesNotExistError(PydanticWranglerBaseException):
    """Model does not exist in the datastore."""


class ModelAlreadyExistsError(PydanticWranglerBaseException):
    """Model already exists in the datastore."""


class DataStoreDirectAssignmentError(PydanticWranglerBaseException):
    """Cannot directly assign to attribute 'records' of a ModelsGlobalStore object."""


class UnsupportedFileFormatError(PydanticWranglerBaseException):
    """Unsupported file format"""


class PydanticWranglerImportError(PydanticWranglerBaseException):
    """Error importing a module or class"""


class PydanticWranglerDumperError(PydanticWranglerBaseException):
    """Error dumping data"""
