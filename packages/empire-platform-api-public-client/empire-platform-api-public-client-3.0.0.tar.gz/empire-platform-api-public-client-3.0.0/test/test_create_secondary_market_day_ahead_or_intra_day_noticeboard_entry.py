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

from empire_platform_api_public_client.models.create_secondary_market_day_ahead_or_intra_day_noticeboard_entry import CreateSecondaryMarketDayAheadOrIntraDayNoticeboardEntry  # noqa: E501

class TestCreateSecondaryMarketDayAheadOrIntraDayNoticeboardEntry(unittest.TestCase):
    """CreateSecondaryMarketDayAheadOrIntraDayNoticeboardEntry unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CreateSecondaryMarketDayAheadOrIntraDayNoticeboardEntry:
        """Test CreateSecondaryMarketDayAheadOrIntraDayNoticeboardEntry
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CreateSecondaryMarketDayAheadOrIntraDayNoticeboardEntry`
        """
        model = CreateSecondaryMarketDayAheadOrIntraDayNoticeboardEntry()  # noqa: E501
        if include_optional:
            return CreateSecondaryMarketDayAheadOrIntraDayNoticeboardEntry(
                type = 'BUY',
                timescale = 'LONG_TERM',
                delivery_day = 'Tue Jan 04 00:00:00 UTC 2022',
                direction = 'GB_NL',
                mtus = [
                    empire_platform_api_public_client.models.secondary_market_capacity_price_mtu.SecondaryMarketCapacityPriceMtu(
                        mtu = '2022-01-04T10:00Z', 
                        capacity = 56, 
                        price = 1.337, )
                    ]
            )
        else:
            return CreateSecondaryMarketDayAheadOrIntraDayNoticeboardEntry(
                type = 'BUY',
                timescale = 'LONG_TERM',
                delivery_day = 'Tue Jan 04 00:00:00 UTC 2022',
                direction = 'GB_NL',
                mtus = [
                    empire_platform_api_public_client.models.secondary_market_capacity_price_mtu.SecondaryMarketCapacityPriceMtu(
                        mtu = '2022-01-04T10:00Z', 
                        capacity = 56, 
                        price = 1.337, )
                    ],
        )
        """

    def testCreateSecondaryMarketDayAheadOrIntraDayNoticeboardEntry(self):
        """Test CreateSecondaryMarketDayAheadOrIntraDayNoticeboardEntry"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
