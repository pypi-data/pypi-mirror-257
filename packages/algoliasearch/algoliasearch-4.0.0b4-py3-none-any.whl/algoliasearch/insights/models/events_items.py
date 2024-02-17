# coding: utf-8

"""
Code generated by OpenAPI Generator (https://openapi-generator.tech), manual changes will be lost - read more on https://github.com/algolia/api-clients-automation. DO NOT EDIT.
"""
from __future__ import annotations

from json import dumps
from typing import Dict, Optional, Self, Union

from pydantic import BaseModel, ValidationError, model_serializer

from algoliasearch.insights.models.added_to_cart_object_ids import AddedToCartObjectIDs
from algoliasearch.insights.models.added_to_cart_object_ids_after_search import (
    AddedToCartObjectIDsAfterSearch,
)
from algoliasearch.insights.models.clicked_filters import ClickedFilters
from algoliasearch.insights.models.clicked_object_ids import ClickedObjectIDs
from algoliasearch.insights.models.clicked_object_ids_after_search import (
    ClickedObjectIDsAfterSearch,
)
from algoliasearch.insights.models.converted_filters import ConvertedFilters
from algoliasearch.insights.models.converted_object_ids import ConvertedObjectIDs
from algoliasearch.insights.models.converted_object_ids_after_search import (
    ConvertedObjectIDsAfterSearch,
)
from algoliasearch.insights.models.purchased_object_ids import PurchasedObjectIDs
from algoliasearch.insights.models.purchased_object_ids_after_search import (
    PurchasedObjectIDsAfterSearch,
)
from algoliasearch.insights.models.viewed_filters import ViewedFilters
from algoliasearch.insights.models.viewed_object_ids import ViewedObjectIDs


class EventsItems(BaseModel):
    """
    EventsItems
    """

    oneof_schema_1_validator: Optional[ClickedObjectIDsAfterSearch] = None
    oneof_schema_2_validator: Optional[AddedToCartObjectIDsAfterSearch] = None
    oneof_schema_3_validator: Optional[PurchasedObjectIDsAfterSearch] = None
    oneof_schema_4_validator: Optional[ConvertedObjectIDsAfterSearch] = None
    oneof_schema_5_validator: Optional[ClickedObjectIDs] = None
    oneof_schema_6_validator: Optional[PurchasedObjectIDs] = None
    oneof_schema_7_validator: Optional[AddedToCartObjectIDs] = None
    oneof_schema_8_validator: Optional[ConvertedObjectIDs] = None
    oneof_schema_9_validator: Optional[ClickedFilters] = None
    oneof_schema_10_validator: Optional[ConvertedFilters] = None
    oneof_schema_11_validator: Optional[ViewedObjectIDs] = None
    oneof_schema_12_validator: Optional[ViewedFilters] = None
    actual_instance: Optional[
        Union[
            AddedToCartObjectIDs,
            AddedToCartObjectIDsAfterSearch,
            ClickedFilters,
            ClickedObjectIDs,
            ClickedObjectIDsAfterSearch,
            ConvertedFilters,
            ConvertedObjectIDs,
            ConvertedObjectIDsAfterSearch,
            PurchasedObjectIDs,
            PurchasedObjectIDsAfterSearch,
            ViewedFilters,
            ViewedObjectIDs,
        ]
    ] = None

    model_config = {"validate_assignment": True}

    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError(
                    "If a position argument is used, only 1 is allowed to set `actual_instance`"
                )
            if kwargs:
                raise ValueError(
                    "If a position argument is used, keyword arguments cannot be used."
                )
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @model_serializer
    def unwrap_actual_instance(
        self,
    ) -> Optional[
        Union[
            AddedToCartObjectIDs,
            AddedToCartObjectIDsAfterSearch,
            ClickedFilters,
            ClickedObjectIDs,
            ClickedObjectIDsAfterSearch,
            ConvertedFilters,
            ConvertedObjectIDs,
            ConvertedObjectIDsAfterSearch,
            PurchasedObjectIDs,
            PurchasedObjectIDsAfterSearch,
            ViewedFilters,
            ViewedObjectIDs,
        ]
    ]:
        """
        Unwraps the `actual_instance` when calling the `to_json` method.
        """
        return self.actual_instance

    @classmethod
    def from_dict(cls, obj: dict) -> Self:
        return cls.from_json(dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Returns the object represented by the json string"""
        instance = cls.model_construct()
        error_messages = []

        try:
            instance.actual_instance = ClickedObjectIDsAfterSearch.from_json(json_str)

            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        try:
            instance.actual_instance = AddedToCartObjectIDsAfterSearch.from_json(
                json_str
            )

            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        try:
            instance.actual_instance = PurchasedObjectIDsAfterSearch.from_json(json_str)

            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        try:
            instance.actual_instance = ConvertedObjectIDsAfterSearch.from_json(json_str)

            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        try:
            instance.actual_instance = ClickedObjectIDs.from_json(json_str)

            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        try:
            instance.actual_instance = PurchasedObjectIDs.from_json(json_str)

            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        try:
            instance.actual_instance = AddedToCartObjectIDs.from_json(json_str)

            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        try:
            instance.actual_instance = ConvertedObjectIDs.from_json(json_str)

            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        try:
            instance.actual_instance = ClickedFilters.from_json(json_str)

            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        try:
            instance.actual_instance = ConvertedFilters.from_json(json_str)

            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        try:
            instance.actual_instance = ViewedObjectIDs.from_json(json_str)

            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        try:
            instance.actual_instance = ViewedFilters.from_json(json_str)

            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        raise ValueError(
            "No match found when deserializing the JSON string into EventsItems with oneOf schemas: AddedToCartObjectIDs, AddedToCartObjectIDsAfterSearch, ClickedFilters, ClickedObjectIDs, ClickedObjectIDsAfterSearch, ConvertedFilters, ConvertedObjectIDs, ConvertedObjectIDsAfterSearch, PurchasedObjectIDs, PurchasedObjectIDsAfterSearch, ViewedFilters, ViewedObjectIDs. Details: "
            + ", ".join(error_messages)
        )

    def to_json(self) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        to_json = getattr(self.actual_instance, "to_json", None)
        if callable(to_json):
            return self.actual_instance.to_json()
        else:
            return dumps(self.actual_instance)

    def to_dict(self) -> Dict:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        to_dict = getattr(self.actual_instance, "to_dict", None)
        if callable(to_dict):
            return self.actual_instance.to_dict()
        else:
            return self.actual_instance
