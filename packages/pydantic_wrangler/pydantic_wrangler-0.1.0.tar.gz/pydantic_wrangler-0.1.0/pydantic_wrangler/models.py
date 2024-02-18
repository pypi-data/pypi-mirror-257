import re
from functools import total_ordering
from typing import Any, Dict, List, Optional, Tuple, Union, ClassVar

from jinja2 import Environment, FileSystemLoader, Template
from jinja2.exceptions import TemplateNotFound
from pydantic import BaseModel, ConfigDict

from pydantic_wrangler.config import get_config
from pydantic_wrangler.datastore import (
    PydanticWranglerSortedSet,
    ModelsGlobalStore,
    get_shared_data_store,
)
from pydantic_wrangler.exceptions import (
    PydanticWranglerTypeError,
    ModelInitializationError,
    RenderableTemplateError,
)
from pydantic_wrangler.utils import convert_nested_dict_to_hashabledict

GLOBAL_CONFIGS = get_config()


@total_ordering
class PydanticWranglerBaseModel(BaseModel):
    """A pydantic BaseModel class that provides the basic
    functionality for all pydantic_wrangler Models classes.

    Any PydanticWranglerBaseModel child class SHOULD be instantiated from
    .create_from_loaded_data() or .create() class methods provided.
    Instantiation by using __init__() directly is discouraged.

    This class implements functools.total_ordering to allow its instances
    to be sorted accordingly inside a pydantic_wrangler.datastore.PydanticWranglerSortedSet.

    Because pydantic_wrangler.datastore.PydanticWranglerSortedSet is a python Set, all
    pydantic_wrangler models MUST be hashable. This has a twofold consequence:
        - Model classes must implement the __hash__() method;
        - all attributes of any pydantic_wrangler model class must be hashable;
    """

    # this class attribute is used as a registry for all subclasses
    # of this one. This is useful to allow transparent discovery of
    # such classes, which in turn allows for easy mapping of directives
    # to model classes.
    _subclasses: ClassVar = []

    # class attribute to store a reference to the global data structure
    # where all model instances are stored.
    _data_store: ClassVar = get_shared_data_store()

    # this is required to allow fields of non-native python types
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # represents the key-word in the format-specific file used to
    # trigger the instantiation of this model class
    _directive: str = None

    # a tuple of strings with each representing the name of an attribute of
    # the model class. This tuple will be used to create a unique identifier
    # that will ID this model object in the store.This will also be used as
    # a sort key in the data store. Child classes MUST override this attribute.
    _key: Tuple = tuple()

    # the global data store doesn't allow for duplication, as it
    # implements a set. However, pydantic_wrangler doesn't necessarily care if a
    # duplication happens.This attribute indicates if an exception should
    # be raised in case an attempted duplication is detected.
    _err_on_duplicate: bool = False

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._subclasses.append(cls)

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    def __lt__(self, other):
        return self.key <= other.key

    def __eq__(self, other):
        return str(self) == str(other)

    @property
    def directive(self) -> str:
        return self._directive

    @property
    def key(self) -> Tuple:
        """Returns a tuple containing the values associate with the fields (attributes)
        named in the `_key` attribute."""
        return tuple([getattr(self, attr) for attr in self._key])

    @classmethod
    def create_from_loaded_data(
        cls, data: Union[Dict[str, Any], List[Dict[str, Any]]]
    ) -> None:
        """Factory class method used to instantiate a model with data
        previously loaded and parsed from a file.

        Args:
            data (Union[Dict[str, Any], List[Dict[str, Any]]]): Data loaded
            from a file of supported format and parsed into a Dictionary or List.

        Raises:
            PydanticWranglerTypeError: If `data` is not a dict nor a list.
        """
        if not isinstance(data, dict) and not isinstance(data, list):
            raise PydanticWranglerTypeError(
                f"Data passed to {cls.__name__} must be of type 'dict' or 'list', but was {type(data)}"
            )

        if isinstance(data, list):
            for _dict in data:
                cls.create(dict_args=_dict)
            return

        cls.create(dict_args=data)

    @classmethod
    def create(
        cls, dict_args: Dict[Any, Any], *args, **kwargs
    ) -> "PydanticWranglerBaseModel":
        if cls == PydanticWranglerBaseModel:
            raise ModelInitializationError(
                "Cannot instantiate PydanticWranglerBaseModel directly."
            )

        convert_nested_dict_to_hashabledict(dict_args)
        new_obj_model = cls.model_validate(dict_args, strict=True, *args, **kwargs)
        new_obj_model.ds().save(new_obj_model)
        return new_obj_model

    @classmethod
    def ds(cls) -> ModelsGlobalStore:
        """Returns the global data store where all models are stored."""
        return cls._data_store

    @classmethod
    def filter(cls, search_params: Dict[Any, Any]) -> PydanticWranglerSortedSet:
        return cls.ds().filter(cls, search_params)

    @classmethod
    def get(cls, search_params: Dict[Any, Any]) -> "PydanticWranglerBaseModel":
        return cls.ds().get(cls, search_params)

    @classmethod
    def get_all(cls) -> PydanticWranglerSortedSet:
        return cls.ds().get_all_by_class(cls)

    @classmethod
    def get_subclasses(cls):
        return cls._subclasses

    @classmethod
    def get_subclasses_with_directive(cls):
        """Returns a list of all subclasses that have a `_directive`
        attribute set. The .get_default() method is used here since
        sub_cls._directive is inherently a pydantic ModelPrivateAttr."""
        return [
            sub_cls
            for sub_cls in cls.get_subclasses()
            if sub_cls._directive.get_default()
        ]


class PydanticWranglerRenderableModel(PydanticWranglerBaseModel):
    """A Renderable model allows for its instances to render a string
    according to a Jinja2 template. This enables various automation
    use-cases.

    The expected template file name is derived in either of two ways:
        - a statically defined `_template_name` attribute in the child class.
        - the class name split on the capital letters, removing
        the word 'Model' (if present), and then joined by underscores ('_'):
            - MyClass -> my_class
            - OtherClassModel -> other_class
            - ModelYetAnotherClass -> yet_another_class

    NOTE: Support for additional templating languages are not planned, but also
    not excluded.
    """

    @classmethod
    def create(
        cls, dict_args: Dict[Any, Any], *args, **kwargs
    ) -> "PydanticWranglerRenderableModel":
        if cls == PydanticWranglerRenderableModel:
            raise ModelInitializationError(
                "Cannot instantiate RenderablePydanticWranglerModel directly."
            )

        cls._set_template(**dict_args)
        return super().create(dict_args, *args, **kwargs)

    @classmethod
    def _set_template(cls, **kwargs):
        """Guarantees the instance will have a _template_name attribute already set.
        If the child class doesn't define it already, one will be created."""
        try:
            getattr(cls, "_template_name")
        except AttributeError:
            informed_template_name = kwargs.get("template_name")

            if informed_template_name:
                cls._template_name = informed_template_name

            else:
                split_cls_name = re.findall("[A-Z][^A-Z]*", cls.__name__)

                if "Model" in split_cls_name:
                    split_cls_name.remove("Model")

                cls._template_name = "_".join(split_cls_name).lower()

    @property
    def template_name(self) -> str:
        """A property to access the _template_name attribute."""
        return self._template_name

    def get_rendered_str(self, extra_vars_dict: Optional[Dict[str, Any]] = None) -> str:
        """Renders this RenderablePydanticWranglerModel into a string according to the Jinja2
        template indicated by _template_name attribute.

        A dictionary representation of this instance will be passed to the render method.
        However, if the template requires additional variables that wouldn't match any of
        the attributes of this instance, the caller can pass them through `extra_vars_dict`
        argument.

        Args:
            extra_vars_dict (Optional[Dict[str, Any]], optional): A dictionary containing
            extra vars that the template may require. Defaults to None.

        Returns:
            str: the rendered string produced by the .render() method of the Template
            object.
        """
        if extra_vars_dict:
            _dict_to_render = dict(self)
            _dict_to_render.update(extra_vars_dict)
            return self._get_template().render(_dict_to_render)

        return self._get_template().render(dict(self))

    def _get_template(self) -> Template:
        """Retrieves the template file to be used to render this RenderablePydanticWranglerModel.
        Currently, only Jinja2 templates are supported. Hence, the file is expected to
        have a '.j2' extension.

        Raises:
            RenderableTemplateError: if a template file with expected name does not exist.

        Returns:
            Template: The template file as a jinja2.Template object.
        """
        env = Environment(loader=FileSystemLoader(GLOBAL_CONFIGS.templates_dir))
        try:
            return env.get_template(f"{self.template_name}.j2")
        except TemplateNotFound as err:
            raise RenderableTemplateError(err.message)
