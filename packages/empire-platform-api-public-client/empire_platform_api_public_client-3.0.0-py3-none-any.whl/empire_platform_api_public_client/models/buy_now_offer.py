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
from typing import List, Optional, Union
from pydantic import BaseModel, Field, StrictInt, StrictStr, confloat, conint, conlist
from empire_platform_api_public_client.models.border_direction import BorderDirection
from empire_platform_api_public_client.models.buy_now_offer_mtus import BuyNowOfferMtus
from empire_platform_api_public_client.models.buy_now_offer_status import BuyNowOfferStatus
from empire_platform_api_public_client.models.date_time_period import DateTimePeriod
from empire_platform_api_public_client.models.mtu_size import MtuSize
from empire_platform_api_public_client.models.purchased_by_organisation import PurchasedByOrganisation

class BuyNowOffer(BaseModel):
    """
    BuyNowOffer
    """
    id: StrictStr = Field(..., description="Unique identifier for the record in UUID4 format")
    validity_period: DateTimePeriod = Field(..., alias="validityPeriod")
    current_price: Union[confloat(multiple_of=0.01, strict=True), conint(strict=True)] = Field(..., alias="currentPrice", description="Currency value in Euros (€), accepted with a precision of maximum 2 decimal places")
    next_price_change_at: datetime = Field(..., alias="nextPriceChangeAt", description="Date and time with zone information, marks an **absolute point** on the timeline  - theoretically can be sent and received with any zone offset (until it marks the desired **absolute point** on the timeline) - in practice it is advised to transfer it in UTC timezone (with Z offset, \"Zulu time\") - ISO 8601 compliant string in `yyyy-mm-ddThh:mm:ss.SSSZ` format ")
    direction: BorderDirection = Field(...)
    status: BuyNowOfferStatus = Field(...)
    total_trs: StrictInt = Field(..., alias="totalTrs", description="Capacity value in kilowatts (kW) - the required system precision allows for handling capacity values as integers")
    total_cost: Union[confloat(multiple_of=0.01, strict=True), conint(strict=True)] = Field(..., alias="totalCost", description="Currency value in Euros (€), accepted with a precision of maximum 2 decimal places")
    purchased_by: Optional[PurchasedByOrganisation] = Field(None, alias="purchasedBy")
    mtu_size: MtuSize = Field(..., alias="mtuSize")
    mtus: conlist(BuyNowOfferMtus) = Field(...)
    __properties = ["id", "validityPeriod", "currentPrice", "nextPriceChangeAt", "direction", "status", "totalTrs", "totalCost", "purchasedBy", "mtuSize", "mtus"]

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
    def from_json(cls, json_str: str) -> BuyNowOffer:
        """Create an instance of BuyNowOffer from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of validity_period
        if self.validity_period:
            _dict['validityPeriod'] = self.validity_period.to_dict()
        # override the default output from pydantic by calling `to_dict()` of purchased_by
        if self.purchased_by:
            _dict['purchasedBy'] = self.purchased_by.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in mtus (list)
        _items = []
        if self.mtus:
            for _item in self.mtus:
                if _item:
                    _items.append(_item.to_dict())
            _dict['mtus'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BuyNowOffer:
        """Create an instance of BuyNowOffer from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BuyNowOffer.parse_obj(obj)

        _obj = BuyNowOffer.parse_obj({
            "id": obj.get("id"),
            "validity_period": DateTimePeriod.from_dict(obj.get("validityPeriod")) if obj.get("validityPeriod") is not None else None,
            "current_price": obj.get("currentPrice"),
            "next_price_change_at": obj.get("nextPriceChangeAt"),
            "direction": obj.get("direction"),
            "status": obj.get("status"),
            "total_trs": obj.get("totalTrs"),
            "total_cost": obj.get("totalCost"),
            "purchased_by": PurchasedByOrganisation.from_dict(obj.get("purchasedBy")) if obj.get("purchasedBy") is not None else None,
            "mtu_size": obj.get("mtuSize"),
            "mtus": [BuyNowOfferMtus.from_dict(_item) for _item in obj.get("mtus")] if obj.get("mtus") is not None else None
        })
        return _obj


