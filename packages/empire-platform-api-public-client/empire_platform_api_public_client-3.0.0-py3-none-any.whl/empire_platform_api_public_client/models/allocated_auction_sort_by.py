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





class AllocatedAuctionSortBy(str, Enum):
    """
    AllocatedAuctionSortBy
    """

    """
    allowed enum values
    """
    AUCTION_TYPE_ASC = 'AUCTION_TYPE_ASC'
    AUCTION_TYPE_DESC = 'AUCTION_TYPE_DESC'
    DELIVERY_PERIOD_START_ASC = 'DELIVERY_PERIOD_START_ASC'
    DELIVERY_PERIOD_START_DESC = 'DELIVERY_PERIOD_START_DESC'
    DELIVERY_PERIOD_END_ASC = 'DELIVERY_PERIOD_END_ASC'
    DELIVERY_PERIOD_END_DESC = 'DELIVERY_PERIOD_END_DESC'
    BORDER_DIRECTION_ASC = 'BORDER_DIRECTION_ASC'
    BORDER_DIRECTION_DESC = 'BORDER_DIRECTION_DESC'
    MARGINAL_CLEARING_PRICE_ASC = 'MARGINAL_CLEARING_PRICE_ASC'
    MARGINAL_CLEARING_PRICE_DESC = 'MARGINAL_CLEARING_PRICE_DESC'

    @classmethod
    def from_json(cls, json_str: str) -> AllocatedAuctionSortBy:
        """Create an instance of AllocatedAuctionSortBy from a JSON string"""
        return AllocatedAuctionSortBy(json.loads(json_str))


