from collections import defaultdict
from functools import cache
from typing import TYPE_CHECKING, Any, DefaultDict, Dict, Optional, Type

from pydantic_wrangler.custom_collections import PydanticWranglerSortedSet
from pydantic_wrangler.exceptions import (
    DataStoreDirectAssignmentError,
    ModelAlreadyExistsError,
    ModelDoesNotExistError,
)

if TYPE_CHECKING:
    from pydantic_wrangler.models import PydanticWranglerBaseModel


class ModelsGlobalStore:
    """Implements a global store for all the models in the application.

    Models are stored in a defaultdict, where the keys are the model
    classes and the values are PydanticWranglerSortedSet objects.

    IMPORTANT: the keys of the defaultdict are model classes, not model
    classes' names.

    The PydanticWranglerSortedSet is a custom collection that stores the
    models in a sorted order, based on the `key` attribute of the model.

    An example of how the structure looks like:
    {
        Model1: PydanticWranglerSortedSet([Model1_instance1, Model1_instance2, ...]),
        Model2: PydanticWranglerSortedSet([Model2_instance1, Model2_instance2, ...]),
        ...
    }

    Only one instance of this class is created and it's shared across the
    entire application. This is done to ensure that all the models are stored
    in the same place and that they can be accessed from anywhere in the
    application. See the `get_shared_data_store` function for more details.
    """

    _records = defaultdict(PydanticWranglerSortedSet)

    @property
    def records(
        self,
    ) -> DefaultDict[Type["PydanticWranglerBaseModel"], PydanticWranglerSortedSet]:
        return self._records

    @records.setter
    def records(self, _):
        raise DataStoreDirectAssignmentError(
            "Cannot directly assign to attribute 'records' of a ModelsGlobalStore object."
        )

    def as_dict(self) -> Dict[str, Any]:
        """Returns regular python dict version of the records attribute.
        This makes it more human-friendly, as well easier to serialize the
        records attribute to a file by using any of the dumper functions in
        the dumpers module.
        """

        dump = {}

        for key, value in self.records.items():
            dump[key.__name__] = [record.model_dump() for record in value]

        return dump

    def save(self, obj: "PydanticWranglerBaseModel") -> None:
        """Saves a model instance to the global store.

        If a key with name obj.__class__ is not in self.records, it will
        be added to the store and the model instance will be added to the
        PydanticWranglerSortedSet associated with that key.Otherwise, the model
        instance will be added to the existing obj.__class__ key.

        Args:
            obj (PydanticWranglerBaseModel): the PydanticWranglerBaseModel instance to be saved.

        Raises:
            ModelAlreadyExists: if the model instance is already in the store
            and the `_err_on_duplicate` attribute is set to True.
        """
        if obj in self.records[obj.__class__] and obj._err_on_duplicate:
            raise ModelAlreadyExistsError(
                f"{obj.__class__.__name__}: duplicates not allowed. Make sure there's no other "
                f"{obj.__class__.__name__} with fields {obj._key} associated with values {obj.key}, respectively."
            )
        self.records[obj.__class__].add(obj)

    def _search(
        self,
        model_class: Type["PydanticWranglerBaseModel"],
        search_params: Optional[Dict[Any, Any]] = None,
    ) -> PydanticWranglerSortedSet:
        """Searches the records of a given model class based on the search_params.
        Currently, only one k:v pair is supported in the search_params.

        Args:
            model_class (Type["PydanticWranglerBaseModel"]): the class of the model to
            be searched. This should map to a key in the self.records defaultdict.
            Otherwise, returns an empty PydanticWranglerSortedSet.
            search_params (Optional[Dict[Any, Any]], optional): a single k:v pair
            dictionary with the key being the attribute of the model and the value
            being the value to be searched for. If None, returns the entire
            PydanticWranglerSortedSet associated with model_class key. Defaults to None.

        Returns:
            PydanticWranglerSortedSet: the PydanticWranglerSortedSet containing the records
            that match the search_params.
        """
        if search_params:
            # we only take the first k,v pair from search_params
            search_k, value = list(search_params.items())[0]
            return PydanticWranglerSortedSet(
                [x for x in self.records[model_class] if getattr(x, search_k) == value]
            )

        return self.records[model_class]

    def filter(
        self,
        model_class: Type["PydanticWranglerBaseModel"],
        search_params: Dict[Any, Any],
    ) -> PydanticWranglerSortedSet:
        """
        Avails of self._search() to filter the records of a given model class
        based on the search_params.

        Currently, only one k:v pair is supported in the search_params.


        Args:
            model_class (Type["PydanticWranglerBaseModel"]): the class of the model
            to be filtered.
            search_params (Dict[Any, Any]): the search parameters to be used
            to filter the records.

        Returns:
            PydanticWranglerSortedSet: the PydanticWranglerSortedSet containing the records
            that match the search_params."""
        return self._search(model_class, search_params)

    def get(
        self,
        model_class: Type["PydanticWranglerBaseModel"],
        search_params: Dict[Any, Any],
    ) -> "PydanticWranglerBaseModel":
        """Avails of self.filter() method to get single model instance from
        the global store based on the search_params.

        Currently, only one k:v pair is supported in the search_params.

        Args:
            model_class (Type["PydanticWranglerBaseModel"]): the class of the model
            to be filtered.
            search_params (Dict[Any, Any]): the search parameters to be used
            to filter the records.

        Raises:
            ModelDoesNotExist: if a PydanticWranglerBaseModel does not exist in
            the datastore matching the search_params.
            ModelAlreadyExists: if more than one PydanticWranglerBaseModel exists
            in the datastore matching the search_params.

        Returns:
            PydanticWranglerBaseModel: a single PydanticWranglerBaseModel instance.
        """
        search = self.filter(model_class, search_params)

        if not search:
            raise ModelDoesNotExistError(
                f"A {model_class.__name__} object was not found matching params: {search_params}"
            )

        if len(search) > 1:
            raise ModelAlreadyExistsError("More than one element found")

        return search[0]

    def get_all_by_class(
        self, model_class: Type["PydanticWranglerBaseModel"]
    ) -> PydanticWranglerSortedSet:
        """Avails of self._search() method to get all the records of a given
        model class from the global store.

        Args:
            model_class (Type["PydanticWranglerBaseModel"]): the class of the model

        Returns:
            PydanticWranglerSortedSet: the PydanticWranglerSortedSet containing all the
            records of the given model class.
        """
        return self._search(model_class)


SHARED_DATA_STORE = None


@cache
def get_shared_data_store():
    """Returns the shared instance of the ModelsGlobalStore. It's a cached function,
    meaning that it will only be executed once and the result will be stored in memory.
    This is done to ensure that the same instance of the class is returned every time
    the function is called."""

    global SHARED_DATA_STORE

    if SHARED_DATA_STORE is None:
        SHARED_DATA_STORE = ModelsGlobalStore()

    return SHARED_DATA_STORE
