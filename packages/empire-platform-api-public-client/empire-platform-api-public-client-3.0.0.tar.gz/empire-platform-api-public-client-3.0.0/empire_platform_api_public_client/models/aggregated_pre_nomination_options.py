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


from typing import List
from pydantic import BaseModel, Field, conlist
from empire_platform_api_public_client.models.aggregated_pre_nomination_options_timescale import AggregatedPreNominationOptionsTimescale

class AggregatedPreNominationOptions(BaseModel):
    """
    AggregatedPreNominationOptions
    """
    long_term: conlist(AggregatedPreNominationOptionsTimescale) = Field(..., alias="longTerm")
    day_ahead: conlist(AggregatedPreNominationOptionsTimescale) = Field(..., alias="dayAhead")
    intra_day: conlist(AggregatedPreNominationOptionsTimescale) = Field(..., alias="intraDay")
    __properties = ["longTerm", "dayAhead", "intraDay"]

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
    def from_json(cls, json_str: str) -> AggregatedPreNominationOptions:
        """Create an instance of AggregatedPreNominationOptions from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in long_term (list)
        _items = []
        if self.long_term:
            for _item in self.long_term:
                if _item:
                    _items.append(_item.to_dict())
            _dict['longTerm'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in day_ahead (list)
        _items = []
        if self.day_ahead:
            for _item in self.day_ahead:
                if _item:
                    _items.append(_item.to_dict())
            _dict['dayAhead'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in intra_day (list)
        _items = []
        if self.intra_day:
            for _item in self.intra_day:
                if _item:
                    _items.append(_item.to_dict())
            _dict['intraDay'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AggregatedPreNominationOptions:
        """Create an instance of AggregatedPreNominationOptions from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AggregatedPreNominationOptions.parse_obj(obj)

        _obj = AggregatedPreNominationOptions.parse_obj({
            "long_term": [AggregatedPreNominationOptionsTimescale.from_dict(_item) for _item in obj.get("longTerm")] if obj.get("longTerm") is not None else None,
            "day_ahead": [AggregatedPreNominationOptionsTimescale.from_dict(_item) for _item in obj.get("dayAhead")] if obj.get("dayAhead") is not None else None,
            "intra_day": [AggregatedPreNominationOptionsTimescale.from_dict(_item) for _item in obj.get("intraDay")] if obj.get("intraDay") is not None else None
        })
        return _obj


