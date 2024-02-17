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





class MessageType(str, Enum):
    """
    MessageType
    """

    """
    allowed enum values
    """
    AUCTION = 'AUCTION'
    BPP = 'BPP'
    BUY_NOW_AUCTION = 'BUY_NOW_AUCTION'
    FINANCE = 'FINANCE'
    MANUAL_MESSAGE = 'MANUAL_MESSAGE'
    NOMINATION = 'NOMINATION'
    OPERATIONAL_DATAFLOW = 'OPERATIONAL_DATAFLOW'
    OPERATIONAL_PROCESS = 'OPERATIONAL_PROCESS'
    PARTICIPANT_CONFIGURATION = 'PARTICIPANT_CONFIGURATION'
    PARTICIPANT_PROCESS = 'PARTICIPANT_PROCESS'
    PLANNED_OUTAGE = 'PLANNED_OUTAGE'
    PROCESS = 'PROCESS'
    SECONDARY_MARKET = 'SECONDARY_MARKET'
    TRANSPARENCY_DATAFLOW = 'TRANSPARENCY_DATAFLOW'
    UNPLANNED_OUTAGE = 'UNPLANNED_OUTAGE'

    @classmethod
    def from_json(cls, json_str: str) -> MessageType:
        """Create an instance of MessageType from a JSON string"""
        return MessageType(json.loads(json_str))


