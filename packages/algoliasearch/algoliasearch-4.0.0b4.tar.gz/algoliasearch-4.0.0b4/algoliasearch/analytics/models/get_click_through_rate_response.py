# coding: utf-8

"""
Code generated by OpenAPI Generator (https://openapi-generator.tech), manual changes will be lost - read more on https://github.com/algolia/api-clients-automation. DO NOT EDIT.
"""
from __future__ import annotations

from json import loads
from typing import Annotated, Any, Dict, List, Optional, Self, Union

from pydantic import BaseModel, Field, StrictInt

from algoliasearch.analytics.models.click_through_rate_event import (
    ClickThroughRateEvent,
)


class GetClickThroughRateResponse(BaseModel):
    """
    GetClickThroughRateResponse
    """

    rate: Union[
        Annotated[float, Field(le=1, strict=True, ge=0)],
        Annotated[int, Field(le=1, strict=True, ge=0)],
    ] = Field(
        description="[Click-through rate (CTR)](https://www.algolia.com/doc/guides/search-analytics/concepts/metrics/#click-through-rate). "
    )
    click_count: StrictInt = Field(
        description="Number of click events.", alias="clickCount"
    )
    tracked_search_count: Optional[StrictInt] = Field(
        description="Number of tracked searches. This is the number of search requests where the `clickAnalytics` parameter is `true`.",
        alias="trackedSearchCount",
    )
    dates: List[ClickThroughRateEvent] = Field(description="Click-through rate events.")

    model_config = {"populate_by_name": True, "validate_assignment": True}

    def to_json(self) -> str:
        return self.model_dump_json(by_alias=True, exclude_unset=True)

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of GetClickThroughRateResponse from a JSON string"""
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
        # each item in dates (list)
        _items = []
        if self.dates:
            for _item in self.dates:
                if _item:
                    _items.append(_item.to_dict())
            _dict["dates"] = _items
        # set to None if tracked_search_count (nullable) is None
        # and model_fields_set contains the field
        if (
            self.tracked_search_count is None
            and "tracked_search_count" in self.model_fields_set
        ):
            _dict["trackedSearchCount"] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of GetClickThroughRateResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "rate": obj.get("rate"),
                "clickCount": obj.get("clickCount"),
                "trackedSearchCount": obj.get("trackedSearchCount"),
                "dates": [
                    ClickThroughRateEvent.from_dict(_item) for _item in obj.get("dates")
                ]
                if obj.get("dates") is not None
                else None,
            }
        )
        return _obj
