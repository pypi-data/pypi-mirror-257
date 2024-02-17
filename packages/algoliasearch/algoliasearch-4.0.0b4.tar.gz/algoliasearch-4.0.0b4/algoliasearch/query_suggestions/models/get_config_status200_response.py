# coding: utf-8

"""
Code generated by OpenAPI Generator (https://openapi-generator.tech), manual changes will be lost - read more on https://github.com/algolia/api-clients-automation. DO NOT EDIT.
"""
from __future__ import annotations

from json import loads
from typing import Any, Dict, Optional, Self

from pydantic import BaseModel, Field, StrictBool, StrictStr


class GetConfigStatus200Response(BaseModel):
    """
    GetConfigStatus200Response
    """

    index_name: Optional[StrictStr] = Field(
        default=None, description="Query Suggestions index name.", alias="indexName"
    )
    is_running: Optional[StrictBool] = Field(
        default=None,
        description="Indicates whether the creation or update of the Query Suggestions is in progress.",
        alias="isRunning",
    )
    last_built_at: Optional[StrictStr] = Field(
        default=None,
        description="Timestamp in [ISO-8601](https://wikipedia.org/wiki/ISO_8601) format when the Query Suggestions index was last built.",
        alias="lastBuiltAt",
    )
    last_successful_built_at: Optional[StrictStr] = Field(
        default=None,
        description="Timestamp in [ISO-8601](https://wikipedia.org/wiki/ISO_8601) format when the Query Suggestions index was last updated successfully.",
        alias="lastSuccessfulBuiltAt",
    )
    last_successful_build_duration: Optional[StrictStr] = Field(
        default=None,
        description="Duration of the last successful build in seconds.",
        alias="lastSuccessfulBuildDuration",
    )

    model_config = {"populate_by_name": True, "validate_assignment": True}

    def to_json(self) -> str:
        return self.model_dump_json(by_alias=True, exclude_unset=True)

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of GetConfigStatus200Response from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of GetConfigStatus200Response from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "indexName": obj.get("indexName"),
                "isRunning": obj.get("isRunning"),
                "lastBuiltAt": obj.get("lastBuiltAt"),
                "lastSuccessfulBuiltAt": obj.get("lastSuccessfulBuiltAt"),
                "lastSuccessfulBuildDuration": obj.get("lastSuccessfulBuildDuration"),
            }
        )
        return _obj
