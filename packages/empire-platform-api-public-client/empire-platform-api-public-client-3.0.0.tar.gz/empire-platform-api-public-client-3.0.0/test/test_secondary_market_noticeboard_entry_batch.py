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

from empire_platform_api_public_client.models.secondary_market_noticeboard_entry_batch import SecondaryMarketNoticeboardEntryBatch  # noqa: E501

class TestSecondaryMarketNoticeboardEntryBatch(unittest.TestCase):
    """SecondaryMarketNoticeboardEntryBatch unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SecondaryMarketNoticeboardEntryBatch:
        """Test SecondaryMarketNoticeboardEntryBatch
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SecondaryMarketNoticeboardEntryBatch`
        """
        model = SecondaryMarketNoticeboardEntryBatch()  # noqa: E501
        if include_optional:
            return SecondaryMarketNoticeboardEntryBatch(
                entries = [
                    empire_platform_api_public_client.models.secondary_market_noticeboard_entry.SecondaryMarketNoticeboardEntry(
                        id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                        type = 'BUY', 
                        delivery_period = empire_platform_api_public_client.models.date_period.DatePeriod(
                            start = 'Tue Jan 04 00:00:00 UTC 2022', 
                            end = 'Tue Jan 04 00:00:00 UTC 2022', ), 
                        timescale = 'LONG_TERM', 
                        direction = 'GB_NL', 
                        notice_capacity = 56, 
                        notice_price = 1.337, 
                        posted_at = '2022-01-04T00:00Z', 
                        status = 'ACTIVE', 
                        expires_at = '2022-01-04T00:00Z', 
                        is_own = True, )
                    ],
                total_count = 0
            )
        else:
            return SecondaryMarketNoticeboardEntryBatch(
                entries = [
                    empire_platform_api_public_client.models.secondary_market_noticeboard_entry.SecondaryMarketNoticeboardEntry(
                        id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                        type = 'BUY', 
                        delivery_period = empire_platform_api_public_client.models.date_period.DatePeriod(
                            start = 'Tue Jan 04 00:00:00 UTC 2022', 
                            end = 'Tue Jan 04 00:00:00 UTC 2022', ), 
                        timescale = 'LONG_TERM', 
                        direction = 'GB_NL', 
                        notice_capacity = 56, 
                        notice_price = 1.337, 
                        posted_at = '2022-01-04T00:00Z', 
                        status = 'ACTIVE', 
                        expires_at = '2022-01-04T00:00Z', 
                        is_own = True, )
                    ],
                total_count = 0,
        )
        """

    def testSecondaryMarketNoticeboardEntryBatch(self):
        """Test SecondaryMarketNoticeboardEntryBatch"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
