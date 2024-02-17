# coding: utf-8

"""
Code generated by OpenAPI Generator (https://openapi-generator.tech), manual changes will be lost - read more on https://github.com/algolia/api-clients-automation. DO NOT EDIT.
"""
from __future__ import annotations

from json import loads
from re import match
from typing import Annotated, Any, Dict, List, Optional, Self

from pydantic import BaseModel, Field, StrictInt, StrictStr, field_validator

from algoliasearch.insights.models.conversion_event import ConversionEvent
from algoliasearch.insights.models.object_data_after_search import ObjectDataAfterSearch
from algoliasearch.insights.models.purchase_event import PurchaseEvent
from algoliasearch.insights.models.value import Value


class PurchasedObjectIDsAfterSearch(BaseModel):
    """
    Use this event to track when users make a purchase after a previous Algolia request. If you're building your category pages with Algolia, you'll also use this event.
    """

    event_name: Annotated[str, Field(min_length=1, strict=True, max_length=64)] = Field(
        description="The name of the event, up to 64 ASCII characters.  Consider naming events consistently—for example, by adopting Segment's [object-action](https://segment.com/academy/collecting-data/naming-conventions-for-clean-data/#the-object-action-framework) framework. ",
        alias="eventName",
    )
    event_type: ConversionEvent = Field(alias="eventType")
    event_subtype: PurchaseEvent = Field(alias="eventSubtype")
    index: StrictStr = Field(description="The name of an Algolia index.")
    object_ids: Annotated[List[StrictStr], Field(min_length=1, max_length=20)] = Field(
        description="The object IDs of the records that are part of the event.",
        alias="objectIDs",
    )
    user_token: Annotated[
        str, Field(min_length=1, strict=True, max_length=129)
    ] = Field(
        description="An anonymous or pseudonymous user identifier.  > **Note**: Never include personally identifiable information in user tokens. ",
        alias="userToken",
    )
    authenticated_user_token: Optional[
        Annotated[str, Field(min_length=1, strict=True, max_length=129)]
    ] = Field(
        default=None,
        description="An identifier for authenticated users.  > **Note**: Never include personally identifiable information in user tokens. ",
        alias="authenticatedUserToken",
    )
    currency: Optional[StrictStr] = Field(
        default=None,
        description="Three-letter [currency code](https://www.iso.org/iso-4217-currency-codes.html).",
    )
    object_data: Optional[
        Annotated[List[ObjectDataAfterSearch], Field(min_length=1, max_length=20)]
    ] = Field(
        default=None,
        description="Extra information about the records involved in a purchase or add-to-cart events.  If provided, it must be the same length as `objectIDs`. ",
        alias="objectData",
    )
    timestamp: Optional[StrictInt] = Field(
        default=None,
        description="The timestamp of the event in milliseconds in [Unix epoch time](https://wikipedia.org/wiki/Unix_time). By default, the Insights API uses the time it receives an event as its timestamp. ",
    )
    value: Optional[Value] = None

    @field_validator("event_name")
    def event_name_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not match(r"[\x20-\x7E]{1,64}", value):
            raise ValueError(
                r"must validate the regular expression /[\x20-\x7E]{1,64}/"
            )
        return value

    @field_validator("user_token")
    def user_token_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not match(r"[a-zA-Z0-9_=\/+-]{1,129}", value):
            raise ValueError(
                r"must validate the regular expression /[a-zA-Z0-9_=\/+-]{1,129}/"
            )
        return value

    @field_validator("authenticated_user_token")
    def authenticated_user_token_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not match(r"[a-zA-Z0-9_=\/+-]{1,129}", value):
            raise ValueError(
                r"must validate the regular expression /[a-zA-Z0-9_=\/+-]{1,129}/"
            )
        return value

    model_config = {"populate_by_name": True, "validate_assignment": True}

    def to_json(self) -> str:
        return self.model_dump_json(by_alias=True, exclude_unset=True)

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of PurchasedObjectIDsAfterSearch from a JSON string"""
        return cls.from_dict(loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={},
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of
        # each item in object_data (list)
        _items = []
        if self.object_data:
            for _item in self.object_data:
                if _item:
                    _items.append(_item.to_dict())
            _dict["objectData"] = _items
        # override the default output from pydantic by calling `to_dict()` of
        # value
        if self.value:
            _dict["value"] = self.value.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of PurchasedObjectIDsAfterSearch from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "eventName": obj.get("eventName"),
                "eventType": obj.get("eventType"),
                "eventSubtype": obj.get("eventSubtype"),
                "index": obj.get("index"),
                "objectIDs": obj.get("objectIDs"),
                "userToken": obj.get("userToken"),
                "authenticatedUserToken": obj.get("authenticatedUserToken"),
                "currency": obj.get("currency"),
                "objectData": [
                    ObjectDataAfterSearch.from_dict(_item)
                    for _item in obj.get("objectData")
                ]
                if obj.get("objectData") is not None
                else None,
                "timestamp": obj.get("timestamp"),
                "value": Value.from_dict(obj.get("value"))
                if obj.get("value") is not None
                else None,
            }
        )
        return _obj
