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
from pydantic import BaseModel, Field, conlist
from empire_platform_api_public_client.models.auction_result_congestion_rent import AuctionResultCongestionRent
from empire_platform_api_public_client.models.auction_result_participant import AuctionResultParticipant
from empire_platform_api_public_client.models.day_ahead_or_intra_day_auction_results_mtu import DayAheadOrIntraDayAuctionResultsMtu

class DayAheadOrIntraDayAuctionResults(BaseModel):
    """
    DayAheadOrIntraDayAuctionResults
    """
    congestion_rent: Optional[AuctionResultCongestionRent] = Field(None, alias="congestionRent")
    mtus: conlist(DayAheadOrIntraDayAuctionResultsMtu) = Field(...)
    successful_participants: conlist(AuctionResultParticipant) = Field(..., alias="successfulParticipants")
    __properties = ["congestionRent", "mtus", "successfulParticipants"]

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
    def from_json(cls, json_str: str) -> DayAheadOrIntraDayAuctionResults:
        """Create an instance of DayAheadOrIntraDayAuctionResults from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of congestion_rent
        if self.congestion_rent:
            _dict['congestionRent'] = self.congestion_rent.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in mtus (list)
        _items = []
        if self.mtus:
            for _item in self.mtus:
                if _item:
                    _items.append(_item.to_dict())
            _dict['mtus'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in successful_participants (list)
        _items = []
        if self.successful_participants:
            for _item in self.successful_participants:
                if _item:
                    _items.append(_item.to_dict())
            _dict['successfulParticipants'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DayAheadOrIntraDayAuctionResults:
        """Create an instance of DayAheadOrIntraDayAuctionResults from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DayAheadOrIntraDayAuctionResults.parse_obj(obj)

        _obj = DayAheadOrIntraDayAuctionResults.parse_obj({
            "congestion_rent": AuctionResultCongestionRent.from_dict(obj.get("congestionRent")) if obj.get("congestionRent") is not None else None,
            "mtus": [DayAheadOrIntraDayAuctionResultsMtu.from_dict(_item) for _item in obj.get("mtus")] if obj.get("mtus") is not None else None,
            "successful_participants": [AuctionResultParticipant.from_dict(_item) for _item in obj.get("successfulParticipants")] if obj.get("successfulParticipants") is not None else None
        })
        return _obj


