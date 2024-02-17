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





class AuctionFilterStatus(str, Enum):
    """
    AuctionFilterStatus
    """

    """
    allowed enum values
    """
    CREATED = 'CREATED'
    INITIALISED = 'INITIALISED'
    PRELIMINARY_SPEC_PUBLISHED = 'PRELIMINARY_SPEC_PUBLISHED'
    FINAL_SPEC_PUBLISHED = 'FINAL_SPEC_PUBLISHED'
    BIDDING_OPEN = 'BIDDING_OPEN'
    BIDDING_CLOSED = 'BIDDING_CLOSED'
    PROVISIONAL_RESULTS_PUBLISHED = 'PROVISIONAL_RESULTS_PUBLISHED'
    CANCELLED = 'CANCELLED'
    DELETED = 'DELETED'

    @classmethod
    def from_json(cls, json_str: str) -> AuctionFilterStatus:
        """Create an instance of AuctionFilterStatus from a JSON string"""
        return AuctionFilterStatus(json.loads(json_str))


