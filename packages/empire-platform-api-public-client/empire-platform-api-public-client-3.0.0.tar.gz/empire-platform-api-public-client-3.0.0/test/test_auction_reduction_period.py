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

from empire_platform_api_public_client.models.auction_reduction_period import AuctionReductionPeriod  # noqa: E501

class TestAuctionReductionPeriod(unittest.TestCase):
    """AuctionReductionPeriod unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AuctionReductionPeriod:
        """Test AuctionReductionPeriod
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AuctionReductionPeriod`
        """
        model = AuctionReductionPeriod()  # noqa: E501
        if include_optional:
            return AuctionReductionPeriod(
                period = empire_platform_api_public_client.models.date_time_period.DateTimePeriod(
                    start = '2022-01-04T00:00Z', 
                    end = '2022-01-04T00:00Z', ),
                atc_reduction = 56,
                available_atc = 56
            )
        else:
            return AuctionReductionPeriod(
                period = empire_platform_api_public_client.models.date_time_period.DateTimePeriod(
                    start = '2022-01-04T00:00Z', 
                    end = '2022-01-04T00:00Z', ),
                atc_reduction = 56,
                available_atc = 56,
        )
        """

    def testAuctionReductionPeriod(self):
        """Test AuctionReductionPeriod"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
