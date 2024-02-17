# coding: utf-8

"""
Code generated by OpenAPI Generator (https://openapi-generator.tech), manual changes will be lost - read more on https://github.com/algolia/api-clients-automation. DO NOT EDIT.
"""
from __future__ import annotations

from json import loads
from typing import Any, Dict, Optional, Self

from pydantic import BaseModel, Field, StrictStr

from algoliasearch.ingestion.models.big_query_data_type import BigQueryDataType


class SourceBigQuery(BaseModel):
    """
    SourceBigQuery
    """

    project_id: StrictStr = Field(
        description="Project ID of the BigQuery Source.", alias="projectID"
    )
    dataset_id: StrictStr = Field(
        description="Dataset ID of the BigQuery Source.", alias="datasetID"
    )
    data_type: Optional[BigQueryDataType] = Field(default=None, alias="dataType")
    table: Optional[StrictStr] = Field(
        default=None, description="Table name (for default BQ)."
    )
    table_prefix: Optional[StrictStr] = Field(
        default=None,
        description="Table prefix (for Google Analytics).",
        alias="tablePrefix",
    )
    custom_sql_request: Optional[StrictStr] = Field(
        default=None,
        description="Custom SQL request to extract data from the BigQuery table.",
        alias="customSQLRequest",
    )
    unique_id_column: Optional[StrictStr] = Field(
        default=None,
        description="The name of the column that contains the unique ID, used as `objectID` in Algolia.",
        alias="uniqueIDColumn",
    )

    model_config = {"populate_by_name": True, "validate_assignment": True}

    def to_json(self) -> str:
        return self.model_dump_json(by_alias=True, exclude_unset=True)

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of SourceBigQuery from a JSON string"""
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
        """Create an instance of SourceBigQuery from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "projectID": obj.get("projectID"),
                "datasetID": obj.get("datasetID"),
                "dataType": obj.get("dataType"),
                "table": obj.get("table"),
                "tablePrefix": obj.get("tablePrefix"),
                "customSQLRequest": obj.get("customSQLRequest"),
                "uniqueIDColumn": obj.get("uniqueIDColumn"),
            }
        )
        return _obj
