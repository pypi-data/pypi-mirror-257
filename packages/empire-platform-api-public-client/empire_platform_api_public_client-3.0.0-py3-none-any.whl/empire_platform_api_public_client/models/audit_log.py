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
from pydantic import BaseModel, Field, StrictStr
from empire_platform_api_public_client.models.audit_log_api_key import AuditLogApiKey
from empire_platform_api_public_client.models.audit_log_domain import AuditLogDomain
from empire_platform_api_public_client.models.audit_log_status import AuditLogStatus
from empire_platform_api_public_client.models.audit_log_type import AuditLogType
from empire_platform_api_public_client.models.audit_log_user import AuditLogUser

class AuditLog(BaseModel):
    """
    AuditLog
    """
    id: StrictStr = Field(..., description="Unique identifier for the record in UUID4 format")
    created_at: datetime = Field(..., alias="createdAt", description="Date and time with zone information, marks an **absolute point** on the timeline  - theoretically can be sent and received with any zone offset (until it marks the desired **absolute point** on the timeline) - in practice it is advised to transfer it in UTC timezone (with Z offset, \"Zulu time\") - ISO 8601 compliant string in `yyyy-mm-ddThh:mm:ss.SSSZ` format ")
    user: AuditLogUser = Field(...)
    domain: AuditLogDomain = Field(...)
    type: AuditLogType = Field(...)
    status: AuditLogStatus = Field(...)
    description: StrictStr = Field(...)
    impersonated_by_user: Optional[AuditLogUser] = Field(None, alias="impersonatedByUser")
    requested_with_api_key: Optional[AuditLogApiKey] = Field(None, alias="requestedWithApiKey")
    __properties = ["id", "createdAt", "user", "domain", "type", "status", "description", "impersonatedByUser", "requestedWithApiKey"]

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
    def from_json(cls, json_str: str) -> AuditLog:
        """Create an instance of AuditLog from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of user
        if self.user:
            _dict['user'] = self.user.to_dict()
        # override the default output from pydantic by calling `to_dict()` of impersonated_by_user
        if self.impersonated_by_user:
            _dict['impersonatedByUser'] = self.impersonated_by_user.to_dict()
        # override the default output from pydantic by calling `to_dict()` of requested_with_api_key
        if self.requested_with_api_key:
            _dict['requestedWithApiKey'] = self.requested_with_api_key.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AuditLog:
        """Create an instance of AuditLog from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AuditLog.parse_obj(obj)

        _obj = AuditLog.parse_obj({
            "id": obj.get("id"),
            "created_at": obj.get("createdAt"),
            "user": AuditLogUser.from_dict(obj.get("user")) if obj.get("user") is not None else None,
            "domain": obj.get("domain"),
            "type": obj.get("type"),
            "status": obj.get("status"),
            "description": obj.get("description"),
            "impersonated_by_user": AuditLogUser.from_dict(obj.get("impersonatedByUser")) if obj.get("impersonatedByUser") is not None else None,
            "requested_with_api_key": AuditLogApiKey.from_dict(obj.get("requestedWithApiKey")) if obj.get("requestedWithApiKey") is not None else None
        })
        return _obj


