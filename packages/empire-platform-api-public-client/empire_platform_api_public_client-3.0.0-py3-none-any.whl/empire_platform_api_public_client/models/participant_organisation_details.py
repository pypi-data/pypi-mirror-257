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



from pydantic import BaseModel, Field, StrictStr
from empire_platform_api_public_client.models.organisation_auth_method import OrganisationAuthMethod
from empire_platform_api_public_client.models.organisation_contact_information import OrganisationContactInformation
from empire_platform_api_public_client.models.organisation_file_settings import OrganisationFileSettings
from empire_platform_api_public_client.models.organisation_market_settings import OrganisationMarketSettings
from empire_platform_api_public_client.models.organisation_status import OrganisationStatus

class ParticipantOrganisationDetails(BaseModel):
    """
    ParticipantOrganisationDetails
    """
    id: StrictStr = Field(..., description="Unique identifier for the record in UUID4 format")
    status: OrganisationStatus = Field(...)
    name: StrictStr = Field(...)
    auth_method: OrganisationAuthMethod = Field(..., alias="authMethod")
    contact_information: OrganisationContactInformation = Field(..., alias="contactInformation")
    market_settings: OrganisationMarketSettings = Field(..., alias="marketSettings")
    file_settings: OrganisationFileSettings = Field(..., alias="fileSettings")
    __properties = ["id", "status", "name", "authMethod", "contactInformation", "marketSettings", "fileSettings"]

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
    def from_json(cls, json_str: str) -> ParticipantOrganisationDetails:
        """Create an instance of ParticipantOrganisationDetails from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of contact_information
        if self.contact_information:
            _dict['contactInformation'] = self.contact_information.to_dict()
        # override the default output from pydantic by calling `to_dict()` of market_settings
        if self.market_settings:
            _dict['marketSettings'] = self.market_settings.to_dict()
        # override the default output from pydantic by calling `to_dict()` of file_settings
        if self.file_settings:
            _dict['fileSettings'] = self.file_settings.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ParticipantOrganisationDetails:
        """Create an instance of ParticipantOrganisationDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ParticipantOrganisationDetails.parse_obj(obj)

        _obj = ParticipantOrganisationDetails.parse_obj({
            "id": obj.get("id"),
            "status": obj.get("status"),
            "name": obj.get("name"),
            "auth_method": obj.get("authMethod"),
            "contact_information": OrganisationContactInformation.from_dict(obj.get("contactInformation")) if obj.get("contactInformation") is not None else None,
            "market_settings": OrganisationMarketSettings.from_dict(obj.get("marketSettings")) if obj.get("marketSettings") is not None else None,
            "file_settings": OrganisationFileSettings.from_dict(obj.get("fileSettings")) if obj.get("fileSettings") is not None else None
        })
        return _obj


