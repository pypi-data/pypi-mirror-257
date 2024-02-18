import importlib
from pathlib import Path
from typing import TYPE_CHECKING, Dict, Optional, Type, TypeVar, Union

# this module is where the 'HashableDict' will be used the most.
# Hence, we import it here and in pydantic_wrangler.__init__.py we import
# it from here. Other modules, including client code, should always do
# 'from pydantic_wrangler import HashableDict'.
from pydantic_wrangler.config import get_config
from pydantic_wrangler.exceptions import (
    PydanticWranglerImportError,
    PydanticWranglerTypeError,
    UnsupportedFileFormatError,
)

GLOBAL_CONFIGS = get_config()
_module, _, _cls = GLOBAL_CONFIGS.hashable_dict_cls.rpartition(".")
try:
    hashable_dict_module = importlib.import_module(_module)
    HashableDict = getattr(hashable_dict_module, _cls)
except AttributeError:
    raise PydanticWranglerImportError(
        f"Could not import class {_cls} from module {_module}"
    )

# Creating a generic type variable to be used in type hints for the HashableDict
# class. This is necessary because the class actually assigned to HashableDict is
# not known in advance, as it can be dynamically defined by the user.
HashableDictType = TypeVar("HashableDictType", bound=HashableDict)

if TYPE_CHECKING:
    from pydantic_wrangler.models import PydanticWranglerBaseModel


def check_support_by_extension(file_path: Path) -> bool:
    """Checks if the file represented by `file_path` is of a
    supported format.

    Here we take a rather naive approach and only check the file
    extension.

    Args:
        file_path (Path): the path to the file to be checked.

    Returns:
        bool: True if the file is of a supported format, False otherwise.
    """
    return file_path.suffix.lstrip(".") in GLOBAL_CONFIGS.supported_formats


def load_file_to_dict(file_path: Union[str, Path]) -> dict:
    """Finds the appropriate loader for the file format and uses it to load the file.

    Args:
        file_path (str, Path): the path to the file to be loaded. If it's a
        string, it will be converted to a Path object.

    Raises:
        PydanticWranglerImportError: If the supplied module with loader
        functions can't be imported.
        UnsupportedFileFormatError: If the file format is not supported.

    Returns:
        dict: the loaded file as a dictionary.
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)

    if not check_support_by_extension(file_path):
        raise UnsupportedFileFormatError(
            f"File extension {file_path.suffix.lstrip('.')} not supported. "
            f"Supported formats are {GLOBAL_CONFIGS.supported_formats}"
        )

    try:
        loader_function = getattr(
            GLOBAL_CONFIGS.loaders_module, f"{file_path.suffix.lstrip('.')}_loader"
        )
    except AttributeError:
        raise PydanticWranglerImportError(
            f"Could not find a loader function with name {file_path.suffix.lstrip('.')}_loader"
        )
    return loader_function(file_path)


def convert_src_file_to(
    src_file: Union[str, Path],
    dst_format: str,
    dst_file: Optional[Union[str, Path]] = None,
    *args,
    **kwargs,
) -> None:
    """Converts a serialized file to another format.

    Args:
        src_file (str, Path): the path to the file to be converted. Can be either
        a string or a Path object.
        dst_format (str): the format to which the file will be converted.
        dst_file (Optional[Path], optional): the path to the output file. If not
        provided, the output will be written to a file with the same name as the input
        file, but with the new extension. Defaults to None.

        additional arguments and keyword arguments will be passed to the dumper
        function.

    Raises:
        UnsupportedFileFormatError: If the src_file format is not supported.
        PydanticWranglerImportError: If either a loader of dumper function
        can't be found for the src_file format or dst_format respectively.
    """
    if isinstance(src_file, str):
        src_file = Path(src_file)

    if isinstance(dst_file, str):
        dst_file = Path(dst_file)

    loaded_dict = load_file_to_dict(src_file)

    try:
        dumper_function = getattr(GLOBAL_CONFIGS.dumpers_module, f"{dst_format}_dumper")
    except AttributeError:
        raise PydanticWranglerImportError(
            f"Could not find a dumper function with name {dst_format}_dumper"
        )

    dst_file = dst_file or src_file.with_suffix(f".{dst_format}")

    dumper_function(loaded_dict, dst_file, *args, **kwargs)


def convert_flat_dict_to_hashabledict(dict_obj: dict) -> Type[HashableDictType]:
    """Converts a flat dictionary to a HashableDict.

    Args:
        dict_obj (dict): the dictionary to be converted.

    Returns:
        Type[HashableDictType]: the converted dictionary as a HashableDict.
    """
    if not dict_obj:
        return HashableDict()

    if not isinstance(dict_obj, HashableDict):
        dict_obj = HashableDict(dict_obj)

    return dict_obj


def convert_nested_dict_to_hashabledict(dict_obj: dict) -> Type[HashableDictType]:
    """Converts a nested dictionary to a HashableDict.

    Args:
        dict_obj (dict): the dictionary to be converted.

    Returns:
        Type[HashableDictType]: the converted dictionary as a HashableDict.
    """
    for k in dict_obj:
        if isinstance(dict_obj[k], dict):
            convert_nested_dict_to_hashabledict(dict_obj[k])
            dict_obj[k] = convert_flat_dict_to_hashabledict(dict_obj[k])

    return convert_flat_dict_to_hashabledict(dict_obj)


def get_directive_to_model_mapping() -> dict:
    """
    Creates a mapping between any PydanticWranglerBaseModel's child class '_directive'
    attribute and the class itself. This allows for easy correlation between 'keys'
    in serialized file and actual PydanticWrangler models.

    Returns:
        A dictionary in which each key is a directive key-word and the value is the
    corresponding PydanticWranglerBaseModel class.

    """
    mapping = {}

    # this import happens here to avoid circular ImportError
    from pydantic_wrangler.models import PydanticWranglerBaseModel

    for cls in PydanticWranglerBaseModel.get_subclasses_with_directive():
        mapping[cls._directive.get_default()] = cls

    return mapping


def create_all_models_from_dict(
    loaded_dict: dict,
    key_to_model_mapping: Dict[str, Type["PydanticWranglerBaseModel"]],
) -> None:
    """Creates all PydanticWrangler models from a dictionary.

    Args:
        loaded_dict (dict): the dictionary to be used to create the models.
        key_to_model_mapping (Dict[str, Type["PydanticWranglerBaseModel"]]): a dictionary
        mapping each key to the corresponding PydanticWrangler model.

    Raises:
        DataTypeError: If `loaded_dict` is not a dict.

    """
    for key in loaded_dict:
        model_cls = key_to_model_mapping.get(key)
        if model_cls:
            if isinstance(loaded_dict[key], list):
                for dict_element in loaded_dict[key]:
                    create_all_models_from_dict(dict_element, key_to_model_mapping)

            model_cls.create_from_loaded_data(loaded_dict[key])


def create_all_models_from_file(file_path: Path) -> None:
    """A very straightforward function to instantiate all models from a file.

    This will only work if there's no need of any kind of pre-processing of the
    data before creating the models.

    If there's a need for pre-processing, then a better approach would be to:
        1 - load the data as a dict by using `load_file_to_dict`
        2 - do the required processing of the loaded data
        3 - create the models from the processed data using `create_all_models_from_dict`

    Args:
        file_path (Path): The path to the file containing serialized data to be
        loaded and parsed into a Dictionary.

    Raises:
        DataTypeError: If `file_path` does not represent a path object.
    """
    if not isinstance(file_path, Path):
        raise PydanticWranglerTypeError(
            f"file_path argument must be of type 'Path', but was {type(file_path)}"
        )

    loaded_data = load_file_to_dict(file_path)
    key_to_model_mapping = get_directive_to_model_mapping()
    create_all_models_from_dict(
        loaded_dict=loaded_data, key_to_model_mapping=key_to_model_mapping
    )
