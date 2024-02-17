# coding: utf-8

"""
Code generated by OpenAPI Generator (https://openapi-generator.tech), manual changes will be lost - read more on https://github.com/algolia/api-clients-automation. DO NOT EDIT.
"""
from __future__ import annotations

from enum import Enum
from json import loads
from typing import Self


class Action(str, Enum):
    """
    Type of batch operation.
    """

    """
    allowed enum values
    """
    ADDOBJECT = "addObject"
    UPDATEOBJECT = "updateObject"
    PARTIALUPDATEOBJECT = "partialUpdateObject"
    PARTIALUPDATEOBJECTNOCREATE = "partialUpdateObjectNoCreate"
    DELETEOBJECT = "deleteObject"
    DELETE = "delete"
    CLEAR = "clear"

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of Action from a JSON string"""
        return cls(loads(json_str))
