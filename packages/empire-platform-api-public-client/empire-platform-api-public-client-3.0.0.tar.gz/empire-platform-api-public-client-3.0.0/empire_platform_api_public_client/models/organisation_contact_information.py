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



from pydantic import BaseModel, Field, constr, validator
from empire_platform_api_public_client.models.organisation_contact import OrganisationContact

class OrganisationContactInformation(BaseModel):
    """
    OrganisationContactInformation
    """
    primary_contact: OrganisationContact = Field(..., alias="primaryContact")
    operational_emergency_contact: OrganisationContact = Field(..., alias="operationalEmergencyContact")
    helpdesk_pin: constr(strict=True) = Field(..., alias="helpdeskPin")
    __properties = ["primaryContact", "operationalEmergencyContact", "helpdeskPin"]

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
    def from_json(cls, json_str: str) -> OrganisationContactInformation:
        """Create an instance of OrganisationContactInformation from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of primary_contact
        if self.primary_contact:
            _dict['primaryContact'] = self.primary_contact.to_dict()
        # override the default output from pydantic by calling `to_dict()` of operational_emergency_contact
        if self.operational_emergency_contact:
            _dict['operationalEmergencyContact'] = self.operational_emergency_contact.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> OrganisationContactInformation:
        """Create an instance of OrganisationContactInformation from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return OrganisationContactInformation.parse_obj(obj)

        _obj = OrganisationContactInformation.parse_obj({
            "primary_contact": OrganisationContact.from_dict(obj.get("primaryContact")) if obj.get("primaryContact") is not None else None,
            "operational_emergency_contact": OrganisationContact.from_dict(obj.get("operationalEmergencyContact")) if obj.get("operationalEmergencyContact") is not None else None,
            "helpdesk_pin": obj.get("helpdeskPin")
        })
        return _obj


