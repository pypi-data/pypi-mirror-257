# coding: utf-8

"""
    Platform API

    _OpenAPI specification for the **Platform API** of **Empire**, the allocation and nomination platform of BritNed_  ---  Additional documentation available in the API's [GitHub repository](https://github.com/britned/empire-platform-api) 

    The version of the OpenAPI document: 3.0.0
    Contact: britned.info@britned.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import List, Optional
from pydantic import BaseModel, Field, StrictInt, conlist
from empire_platform_api_public_client.models.border_direction import BorderDirection
from empire_platform_api_public_client.models.transmission_rights_overview_mtus_values_timescales import TransmissionRightsOverviewMtusValuesTimescales

class TransmissionRightsOverviewMtusValues(BaseModel):
    """
    TransmissionRightsOverviewMtusValues
    """
    direction: BorderDirection = Field(...)
    timescales: conlist(TransmissionRightsOverviewMtusValuesTimescales) = Field(...)
    total: Optional[StrictInt] = Field(None, description="Capacity value in kilowatts (kW) - the required system precision allows for handling capacity values as integers")
    curtailed: Optional[StrictInt] = Field(None, description="Capacity value in kilowatts (kW) - the required system precision allows for handling capacity values as integers")
    remaining: Optional[StrictInt] = Field(None, description="Capacity value in kilowatts (kW) - the required system precision allows for handling capacity values as integers")
    __properties = ["direction", "timescales", "total", "curtailed", "remaining"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TransmissionRightsOverviewMtusValues:
        """Create an instance of TransmissionRightsOverviewMtusValues from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in timescales (list)
        _items = []
        if self.timescales:
            for _item in self.timescales:
                if _item:
                    _items.append(_item.to_dict())
            _dict['timescales'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TransmissionRightsOverviewMtusValues:
        """Create an instance of TransmissionRightsOverviewMtusValues from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TransmissionRightsOverviewMtusValues.parse_obj(obj)

        _obj = TransmissionRightsOverviewMtusValues.parse_obj({
            "direction": obj.get("direction"),
            "timescales": [TransmissionRightsOverviewMtusValuesTimescales.from_dict(_item) for _item in obj.get("timescales")] if obj.get("timescales") is not None else None,
            "total": obj.get("total"),
            "curtailed": obj.get("curtailed"),
            "remaining": obj.get("remaining")
        })
        return _obj


