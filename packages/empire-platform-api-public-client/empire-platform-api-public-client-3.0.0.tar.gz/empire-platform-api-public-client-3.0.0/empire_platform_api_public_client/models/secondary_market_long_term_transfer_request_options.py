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



from pydantic import BaseModel, Field, StrictInt

class SecondaryMarketLongTermTransferRequestOptions(BaseModel):
    """
    SecondaryMarketLongTermTransferRequestOptions
    """
    available_capacity: StrictInt = Field(..., alias="availableCapacity", description="Capacity value in kilowatts (kW) - the required system precision allows for handling capacity values as integers")
    __properties = ["availableCapacity"]

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
    def from_json(cls, json_str: str) -> SecondaryMarketLongTermTransferRequestOptions:
        """Create an instance of SecondaryMarketLongTermTransferRequestOptions from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SecondaryMarketLongTermTransferRequestOptions:
        """Create an instance of SecondaryMarketLongTermTransferRequestOptions from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SecondaryMarketLongTermTransferRequestOptions.parse_obj(obj)

        _obj = SecondaryMarketLongTermTransferRequestOptions.parse_obj({
            "available_capacity": obj.get("availableCapacity")
        })
        return _obj


