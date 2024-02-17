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

from empire_platform_api_public_client.models.default_bid_options import DefaultBidOptions  # noqa: E501

class TestDefaultBidOptions(unittest.TestCase):
    """DefaultBidOptions unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DefaultBidOptions:
        """Test DefaultBidOptions
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DefaultBidOptions`
        """
        model = DefaultBidOptions()  # noqa: E501
        if include_optional:
            return DefaultBidOptions(
                mtu_sizes = [
                    empire_platform_api_public_client.models.mtu_size_per_auction_product_type.MtuSizePerAuctionProductType(
                        auction_product_type = 'LT_EXPLICIT_MULTI_ANNUAL', 
                        mtu_size = 'MTU_15_MINS', )
                    ]
            )
        else:
            return DefaultBidOptions(
                mtu_sizes = [
                    empire_platform_api_public_client.models.mtu_size_per_auction_product_type.MtuSizePerAuctionProductType(
                        auction_product_type = 'LT_EXPLICIT_MULTI_ANNUAL', 
                        mtu_size = 'MTU_15_MINS', )
                    ],
        )
        """

    def testDefaultBidOptions(self):
        """Test DefaultBidOptions"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
