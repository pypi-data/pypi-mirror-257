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
from typing import Optional
from pydantic import BaseModel, Field
from empire_platform_api_public_client.models.day_ahead_or_intra_day_auction_participant_results_mtus_value import DayAheadOrIntraDayAuctionParticipantResultsMtusValue

class DayAheadOrIntraDayAuctionParticipantResultsMtus(BaseModel):
    """
    DayAheadOrIntraDayAuctionParticipantResultsMtus
    """
    mtu: datetime = Field(..., description="The first moment (inclusive) of an MTU period  - theoretically can be sent and received with any zone offset (until it marks the desired **absolute MTU start point** on the timeline) - in practice it is advised to transfer it in UTC timezone (with Z offset, \"Zulu time\") - ISO 8601 compliant string in `yyyy-mm-ddThh:mm:ss.SSSZ` format - only with `XX:00:00`, `XX:15:00`, `XX:30:00` and `XX:45:00` time parts are valid values (depending on MTU size) ")
    value: Optional[DayAheadOrIntraDayAuctionParticipantResultsMtusValue] = None
    __properties = ["mtu", "value"]

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
    def from_json(cls, json_str: str) -> DayAheadOrIntraDayAuctionParticipantResultsMtus:
        """Create an instance of DayAheadOrIntraDayAuctionParticipantResultsMtus from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of value
        if self.value:
            _dict['value'] = self.value.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DayAheadOrIntraDayAuctionParticipantResultsMtus:
        """Create an instance of DayAheadOrIntraDayAuctionParticipantResultsMtus from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DayAheadOrIntraDayAuctionParticipantResultsMtus.parse_obj(obj)

        _obj = DayAheadOrIntraDayAuctionParticipantResultsMtus.parse_obj({
            "mtu": obj.get("mtu"),
            "value": DayAheadOrIntraDayAuctionParticipantResultsMtusValue.from_dict(obj.get("value")) if obj.get("value") is not None else None
        })
        return _obj


