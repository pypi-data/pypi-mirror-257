# coding: utf-8

"""
Code generated by OpenAPI Generator (https://openapi-generator.tech), manual changes will be lost - read more on https://github.com/algolia/api-clients-automation. DO NOT EDIT.
"""
from __future__ import annotations

from enum import Enum
from json import loads
from typing import Self


class RecommendationModels(str, Enum):
    """
    Recommendation model.
    """

    """
    allowed enum values
    """
    RELATED_MINUS_PRODUCTS = "related-products"
    BOUGHT_MINUS_TOGETHER = "bought-together"

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of RecommendationModels from a JSON string"""
        return cls(loads(json_str))
