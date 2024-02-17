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

from empire_platform_api_public_client.models.public_long_term_auction import PublicLongTermAuction  # noqa: E501

class TestPublicLongTermAuction(unittest.TestCase):
    """PublicLongTermAuction unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> PublicLongTermAuction:
        """Test PublicLongTermAuction
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `PublicLongTermAuction`
        """
        model = PublicLongTermAuction()  # noqa: E501
        if include_optional:
            return PublicLongTermAuction(
                id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09',
                name = '2022 May Auction',
                display_id = 'BDL-NL-GB-E-BASE---220305-01',
                product_type = 'LT_EXPLICIT_MULTI_ANNUAL',
                border_direction = 'GB_NL',
                status = 'PRELIMINARY_SPEC_PUBLISHED',
                processing = True,
                delivery_period = empire_platform_api_public_client.models.mtu_period.MtuPeriod(
                    from_mtu_start = '2022-01-04T10:00Z', 
                    to_mtu_end = '2022-01-04T11:00Z', ),
                allocation_mtu_size = 'MTU_15_MINS',
                allocation_resolution = 'RES_1_KW',
                process_steps = empire_platform_api_public_client.models.auction_process_steps_absolute.AuctionProcessStepsAbsolute(
                    preliminary_spec_publish = '2022-01-04T00:00Z', 
                    returns_window_close = '2022-01-04T00:00Z', 
                    final_spec_publish = '2022-01-04T00:00Z', 
                    bidding_open = '2022-01-04T00:00Z', 
                    show_bids_for_open_auctions = '2022-01-04T00:00Z', 
                    bidding_close = '2022-01-04T00:00Z', 
                    provisional_results_publish = '2022-01-04T00:00Z', 
                    final_results_publish = '2022-01-04T00:00Z', ),
                offered_capacity = empire_platform_api_public_client.models.long_term_offered_capacity.LongTermOfferedCapacity(
                    preliminary_oc = 56, 
                    returned_oc = 56, 
                    final_oc = 56, ),
                reserve_price = empire_platform_api_public_client.models.long_term_reserve_price.LongTermReservePrice(
                    steps = [
                        empire_platform_api_public_client.models.long_term_reserve_price_steps.LongTermReservePrice_steps(
                            from = 56, 
                            to = 56, 
                            reserve_price = 1.337, )
                        ], 
                    publish = 'PRELIMINARY_SPEC_PUBLISHED', )
            )
        else:
            return PublicLongTermAuction(
                id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09',
                name = '2022 May Auction',
                display_id = 'BDL-NL-GB-E-BASE---220305-01',
                product_type = 'LT_EXPLICIT_MULTI_ANNUAL',
                border_direction = 'GB_NL',
                status = 'PRELIMINARY_SPEC_PUBLISHED',
                processing = True,
                delivery_period = empire_platform_api_public_client.models.mtu_period.MtuPeriod(
                    from_mtu_start = '2022-01-04T10:00Z', 
                    to_mtu_end = '2022-01-04T11:00Z', ),
                allocation_mtu_size = 'MTU_15_MINS',
                allocation_resolution = 'RES_1_KW',
                process_steps = empire_platform_api_public_client.models.auction_process_steps_absolute.AuctionProcessStepsAbsolute(
                    preliminary_spec_publish = '2022-01-04T00:00Z', 
                    returns_window_close = '2022-01-04T00:00Z', 
                    final_spec_publish = '2022-01-04T00:00Z', 
                    bidding_open = '2022-01-04T00:00Z', 
                    show_bids_for_open_auctions = '2022-01-04T00:00Z', 
                    bidding_close = '2022-01-04T00:00Z', 
                    provisional_results_publish = '2022-01-04T00:00Z', 
                    final_results_publish = '2022-01-04T00:00Z', ),
                offered_capacity = empire_platform_api_public_client.models.long_term_offered_capacity.LongTermOfferedCapacity(
                    preliminary_oc = 56, 
                    returned_oc = 56, 
                    final_oc = 56, ),
        )
        """

    def testPublicLongTermAuction(self):
        """Test PublicLongTermAuction"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
