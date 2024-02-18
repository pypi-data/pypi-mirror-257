import importlib
import inspect
import os
from types import ModuleType
from typing import List

from pydantic_wrangler.exceptions import PydanticWranglerImportError

# Below, we define the default values for the environment variables that
# will be used to configure the package. If the user wants to override these
# values, they can do so by setting the environment variables with the same
# names as the ones defined below.

# Directory where templates are stored by default
TEMPLATES_DIR = "templates"

# The python dotted path to the class used for creating hashable dictionaries
HASHABLE_DICT_CLS = "pydantic_wrangler.custom_collections.HashableDict"

# The python dotted path to the module the provides loader functions
LOADERS_MODULE = "pydantic_wrangler.loaders"

# The python dotted path to the module the provides dumper functions
DUMPERS_MODULE = "pydantic_wrangler.dumpers"


class PydanticWranglerConfig:
    """
    This class is used to hold the configuration of the package, which is
    determined by the environment variables.
    """

    @property
    def templates_dir(self) -> str:
        return os.environ.get("TEMPLATES_DIR", TEMPLATES_DIR)

    @property
    def hashable_dict_cls(self) -> str:
        return os.environ.get("HASHABLE_DICT_CLS", HASHABLE_DICT_CLS)

    @property
    def loaders_module_path(self) -> str:
        return os.environ.get("LOADERS_MODULE", LOADERS_MODULE)

    @property
    def loaders_module(self) -> ModuleType:
        try:
            loaders_module = importlib.import_module(self.loaders_module_path)
        except ImportError as err:
            raise PydanticWranglerImportError(err)

        return loaders_module

    @property
    def dumpers_module_path(self) -> str:
        return os.environ.get("DUMPERS_MODULE", DUMPERS_MODULE)

    @property
    def dumpers_module(self) -> ModuleType:
        try:
            dumpers_module = importlib.import_module(self.dumpers_module_path)
        except ImportError as err:
            raise PydanticWranglerImportError(err)

        return dumpers_module

    @property
    def supported_formats(self) -> List[str]:
        """
        For simplicity, we only take loaders as the basis to determine the supported formats.

        In this package, it's guaranteed to always exist a matching dumper for each loader.
        If you are using a custom loader module, you should also strive for the same.
        """
        supported_formats = [
            name.partition("_")[0]
            for name, obj in inspect.getmembers(self.loaders_module)
            if inspect.isfunction(obj) and "_loader" in name
        ]

        return supported_formats


GLOBAL_CONFIGS = None


def get_config():
    global GLOBAL_CONFIGS

    if GLOBAL_CONFIGS is None:
        GLOBAL_CONFIGS = PydanticWranglerConfig()

    return GLOBAL_CONFIGS
