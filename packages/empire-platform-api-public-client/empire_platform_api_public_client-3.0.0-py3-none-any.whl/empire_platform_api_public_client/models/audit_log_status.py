# coding: utf-8

"""
    Platform API

    _OpenAPI specification for the **Platform API** of **Empire**, the allocation and nomination platform of BritNed_  ---  Additional documentation available in the API's [GitHub repository](https://github.com/britned/empire-platform-api) 

    The version of the OpenAPI document: 3.0.0
    Contact: britned.info@britned.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import json
import pprint
import re  # noqa: F401
from aenum import Enum, no_arg





class AuditLogStatus(str, Enum):
    """
    AuditLogStatus
    """

    """
    allowed enum values
    """
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'

    @classmethod
    def from_json(cls, json_str: str) -> AuditLogStatus:
        """Create an instance of AuditLogStatus from a JSON string"""
        return AuditLogStatus(json.loads(json_str))


