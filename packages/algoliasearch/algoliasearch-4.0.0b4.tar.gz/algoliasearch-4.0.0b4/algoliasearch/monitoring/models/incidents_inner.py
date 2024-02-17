# coding: utf-8

"""
Code generated by OpenAPI Generator (https://openapi-generator.tech), manual changes will be lost - read more on https://github.com/algolia/api-clients-automation. DO NOT EDIT.
"""
from __future__ import annotations

from json import loads
from typing import Any, Dict, Optional, Self

from pydantic import BaseModel, Field, StrictInt

from algoliasearch.monitoring.models.incident import Incident


class IncidentsInner(BaseModel):
    """
    IncidentsInner
    """

    t: Optional[StrictInt] = Field(
        default=None,
        description="Timestamp in [Unix epoch time](https://wikipedia.org/wiki/Unix_time) in milliseconds.",
    )
    v: Optional[Incident] = None

    model_config = {"populate_by_name": True, "validate_assignment": True}

    def to_json(self) -> str:
        return self.model_dump_json(by_alias=True, exclude_unset=True)

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of IncidentsInner from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of v
        if self.v:
            _dict["v"] = self.v.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of IncidentsInner from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "t": obj.get("t"),
                "v": Incident.from_dict(obj.get("v"))
                if obj.get("v") is not None
                else None,
            }
        )
        return _obj
