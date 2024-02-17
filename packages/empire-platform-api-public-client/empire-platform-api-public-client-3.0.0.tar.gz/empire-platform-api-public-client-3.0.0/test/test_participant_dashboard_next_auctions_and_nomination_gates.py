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

from empire_platform_api_public_client.models.participant_dashboard_next_auctions_and_nomination_gates import ParticipantDashboardNextAuctionsAndNominationGates  # noqa: E501

class TestParticipantDashboardNextAuctionsAndNominationGates(unittest.TestCase):
    """ParticipantDashboardNextAuctionsAndNominationGates unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ParticipantDashboardNextAuctionsAndNominationGates:
        """Test ParticipantDashboardNextAuctionsAndNominationGates
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ParticipantDashboardNextAuctionsAndNominationGates`
        """
        model = ParticipantDashboardNextAuctionsAndNominationGates()  # noqa: E501
        if include_optional:
            return ParticipantDashboardNextAuctionsAndNominationGates(
                nomination_gates = [
                    empire_platform_api_public_client.models.dashboard_next_nomination_gate.DashboardNextNominationGate(
                        timescale = 'LONG_TERM', 
                        window = empire_platform_api_public_client.models.dashboard_next_nomination_gate_window.DashboardNextNominationGate_window(
                            opens_at = '2022-01-04T00:00Z', 
                            closes_at = '2022-01-04T00:00Z', ), 
                        delivery_period = empire_platform_api_public_client.models.mtu_period.MtuPeriod(
                            from_mtu_start = '2022-01-04T10:00Z', 
                            to_mtu_end = '2022-01-04T11:00Z', ), 
                        status = 'NOT_YET_OPEN', 
                        next_action_at = '2022-01-04T00:00Z', )
                    ],
                day_ahead_auctions = [
                    empire_platform_api_public_client.models.participant_dashboard_next_auction.ParticipantDashboardNextAuction(
                        id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                        name = '2022 May Auction', 
                        delivery_period = empire_platform_api_public_client.models.mtu_period.MtuPeriod(
                            from_mtu_start = '2022-01-04T10:00Z', 
                            to_mtu_end = '2022-01-04T11:00Z', ), 
                        product_type = 'LT_EXPLICIT_MULTI_ANNUAL', 
                        border_direction = 'GB_NL', 
                        status = 'CREATED', 
                        pre_bidding_allowed = True, 
                        bids_count = 0, 
                        offered_capacity = 56, 
                        next_action_at = '2022-01-04T00:00Z', )
                    ],
                intra_day_auctions = [
                    empire_platform_api_public_client.models.participant_dashboard_next_auction.ParticipantDashboardNextAuction(
                        id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                        name = '2022 May Auction', 
                        delivery_period = empire_platform_api_public_client.models.mtu_period.MtuPeriod(
                            from_mtu_start = '2022-01-04T10:00Z', 
                            to_mtu_end = '2022-01-04T11:00Z', ), 
                        product_type = 'LT_EXPLICIT_MULTI_ANNUAL', 
                        border_direction = 'GB_NL', 
                        status = 'CREATED', 
                        pre_bidding_allowed = True, 
                        bids_count = 0, 
                        offered_capacity = 56, 
                        next_action_at = '2022-01-04T00:00Z', )
                    ]
            )
        else:
            return ParticipantDashboardNextAuctionsAndNominationGates(
                nomination_gates = [
                    empire_platform_api_public_client.models.dashboard_next_nomination_gate.DashboardNextNominationGate(
                        timescale = 'LONG_TERM', 
                        window = empire_platform_api_public_client.models.dashboard_next_nomination_gate_window.DashboardNextNominationGate_window(
                            opens_at = '2022-01-04T00:00Z', 
                            closes_at = '2022-01-04T00:00Z', ), 
                        delivery_period = empire_platform_api_public_client.models.mtu_period.MtuPeriod(
                            from_mtu_start = '2022-01-04T10:00Z', 
                            to_mtu_end = '2022-01-04T11:00Z', ), 
                        status = 'NOT_YET_OPEN', 
                        next_action_at = '2022-01-04T00:00Z', )
                    ],
                day_ahead_auctions = [
                    empire_platform_api_public_client.models.participant_dashboard_next_auction.ParticipantDashboardNextAuction(
                        id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                        name = '2022 May Auction', 
                        delivery_period = empire_platform_api_public_client.models.mtu_period.MtuPeriod(
                            from_mtu_start = '2022-01-04T10:00Z', 
                            to_mtu_end = '2022-01-04T11:00Z', ), 
                        product_type = 'LT_EXPLICIT_MULTI_ANNUAL', 
                        border_direction = 'GB_NL', 
                        status = 'CREATED', 
                        pre_bidding_allowed = True, 
                        bids_count = 0, 
                        offered_capacity = 56, 
                        next_action_at = '2022-01-04T00:00Z', )
                    ],
                intra_day_auctions = [
                    empire_platform_api_public_client.models.participant_dashboard_next_auction.ParticipantDashboardNextAuction(
                        id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                        name = '2022 May Auction', 
                        delivery_period = empire_platform_api_public_client.models.mtu_period.MtuPeriod(
                            from_mtu_start = '2022-01-04T10:00Z', 
                            to_mtu_end = '2022-01-04T11:00Z', ), 
                        product_type = 'LT_EXPLICIT_MULTI_ANNUAL', 
                        border_direction = 'GB_NL', 
                        status = 'CREATED', 
                        pre_bidding_allowed = True, 
                        bids_count = 0, 
                        offered_capacity = 56, 
                        next_action_at = '2022-01-04T00:00Z', )
                    ],
        )
        """

    def testParticipantDashboardNextAuctionsAndNominationGates(self):
        """Test ParticipantDashboardNextAuctionsAndNominationGates"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
