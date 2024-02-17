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





class AggregatedNominationType(str, Enum):
    """
    AggregatedNominationType
    """

    """
    allowed enum values
    """
    TIMESCALE = 'TIMESCALE'
    TIMESCALE_AND_BPP = 'TIMESCALE_AND_BPP'
    BPP = 'BPP'
    SOSO = 'SOSO'
    OPERATIONAL_FLOW = 'OPERATIONAL_FLOW'

    @classmethod
    def from_json(cls, json_str: str) -> AggregatedNominationType:
        """Create an instance of AggregatedNominationType from a JSON string"""
        return AggregatedNominationType(json.loads(json_str))


