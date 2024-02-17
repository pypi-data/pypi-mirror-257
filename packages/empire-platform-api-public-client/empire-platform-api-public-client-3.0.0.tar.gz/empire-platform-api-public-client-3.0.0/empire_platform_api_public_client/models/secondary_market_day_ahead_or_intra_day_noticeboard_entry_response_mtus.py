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

from datetime import datetime
from typing import Union
from pydantic import BaseModel, Field, StrictInt, confloat, conint

class SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponseMtus(BaseModel):
    """
    SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponseMtus
    """
    mtu: datetime = Field(..., description="The first moment (inclusive) of an MTU period  - theoretically can be sent and received with any zone offset (until it marks the desired **absolute MTU start point** on the timeline) - in practice it is advised to transfer it in UTC timezone (with Z offset, \"Zulu time\") - ISO 8601 compliant string in `yyyy-mm-ddThh:mm:ss.SSSZ` format - only with `XX:00:00`, `XX:15:00`, `XX:30:00` and `XX:45:00` time parts are valid values (depending on MTU size) ")
    response_capacity: StrictInt = Field(..., alias="responseCapacity", description="Capacity value in kilowatts (kW) - the required system precision allows for handling capacity values as integers")
    response_price: Union[confloat(multiple_of=0.01, strict=True), conint(strict=True)] = Field(..., alias="responsePrice", description="Currency value in Euros (€), accepted with a precision of maximum 2 decimal places")
    __properties = ["mtu", "responseCapacity", "responsePrice"]

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
    def from_json(cls, json_str: str) -> SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponseMtus:
        """Create an instance of SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponseMtus from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponseMtus:
        """Create an instance of SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponseMtus from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponseMtus.parse_obj(obj)

        _obj = SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponseMtus.parse_obj({
            "mtu": obj.get("mtu"),
            "response_capacity": obj.get("responseCapacity"),
            "response_price": obj.get("responsePrice")
        })
        return _obj


