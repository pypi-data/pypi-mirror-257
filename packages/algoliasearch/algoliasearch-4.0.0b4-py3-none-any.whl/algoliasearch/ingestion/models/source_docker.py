# coding: utf-8

"""
Code generated by OpenAPI Generator (https://openapi-generator.tech), manual changes will be lost - read more on https://github.com/algolia/api-clients-automation. DO NOT EDIT.
"""
from __future__ import annotations

from json import loads
from typing import Any, Dict, Optional, Self

from pydantic import BaseModel, Field, StrictStr

from algoliasearch.ingestion.models.docker_image_type import DockerImageType
from algoliasearch.ingestion.models.docker_registry import DockerRegistry


class SourceDocker(BaseModel):
    """
    SourceDocker
    """

    image_type: DockerImageType = Field(alias="imageType")
    registry: DockerRegistry
    image: StrictStr = Field(description="The name of the image to pull.")
    version: Optional[StrictStr] = Field(
        default=None, description="The version of the image, defaults to `latest`."
    )
    configuration: Dict[str, Any] = Field(description="The configuration of the spec.")

    model_config = {"populate_by_name": True, "validate_assignment": True}

    def to_json(self) -> str:
        return self.model_dump_json(by_alias=True, exclude_unset=True)

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of SourceDocker from a JSON string"""
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
        """Create an instance of SourceDocker from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "imageType": obj.get("imageType"),
                "registry": obj.get("registry"),
                "image": obj.get("image"),
                "version": obj.get("version"),
                "configuration": obj.get("configuration"),
            }
        )
        return _obj
