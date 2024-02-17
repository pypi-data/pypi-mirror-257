# coding: utf-8

"""
    Platform API

    _OpenAPI specification for the **Platform API** of **Empire**, the allocation and nomination platform of BritNed_  ---  Additional documentation available in the API's [GitHub repository](https://github.com/britned/empire-platform-api) 

    The version of the OpenAPI document: 3.0.0
    Contact: britned.info@britned.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest
import datetime

from empire_platform_api_public_client.models.long_term_auction_bid_result import LongTermAuctionBidResult  # noqa: E501

class TestLongTermAuctionBidResult(unittest.TestCase):
    """LongTermAuctionBidResult unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> LongTermAuctionBidResult:
        """Test LongTermAuctionBidResult
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `LongTermAuctionBidResult`
        """
        model = LongTermAuctionBidResult()  # noqa: E501
        if include_optional:
            return LongTermAuctionBidResult(
                id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09',
                participant = empire_platform_api_public_client.models.auction_bid_participant.AuctionBidParticipant(
                    id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                    name = '', ),
                value = empire_platform_api_public_client.models.bid_value.BidValue(
                    price = 1.337, 
                    capacity = 56, ),
                updated_at = '2022-01-04T00:00Z',
                status = 'NOT_CLEARED_YET'
            )
        else:
            return LongTermAuctionBidResult(
                value = empire_platform_api_public_client.models.bid_value.BidValue(
                    price = 1.337, 
                    capacity = 56, ),
                status = 'NOT_CLEARED_YET',
        )
        """

    def testLongTermAuctionBidResult(self):
        """Test LongTermAuctionBidResult"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
