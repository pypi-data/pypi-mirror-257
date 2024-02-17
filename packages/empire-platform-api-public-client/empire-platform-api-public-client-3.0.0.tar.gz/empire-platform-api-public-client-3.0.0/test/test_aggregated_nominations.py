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

from empire_platform_api_public_client.models.aggregated_nominations import AggregatedNominations  # noqa: E501

class TestAggregatedNominations(unittest.TestCase):
    """AggregatedNominations unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AggregatedNominations:
        """Test AggregatedNominations
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AggregatedNominations`
        """
        model = AggregatedNominations()  # noqa: E501
        if include_optional:
            return AggregatedNominations(
                mns = empire_platform_api_public_client.models.aggregated_nominations_mns_or_gb.AggregatedNominationsMnsOrGb(
                    mtu_size = 'MTU_15_MINS', 
                    mtus = [
                        empire_platform_api_public_client.models.aggregated_nominations_mns_or_gb_mtus.AggregatedNominationsMnsOrGb_mtus(
                            mtu = '2022-01-04T10:00Z', 
                            values = [
                                empire_platform_api_public_client.models.aggregated_nominations_mtu_value.AggregatedNominationsMtuValue(
                                    direction = 'GB_NL', 
                                    value = 56, )
                                ], 
                            netted_nominations = empire_platform_api_public_client.models.aggregated_nominations_mtu_netted_nominations.AggregatedNominationsMtuNettedNominations(
                                direction = 'GB_NL', 
                                flow = 56, ), )
                        ], ),
                gb = empire_platform_api_public_client.models.aggregated_nominations_mns_or_gb.AggregatedNominationsMnsOrGb(
                    mtu_size = 'MTU_15_MINS', 
                    mtus = [
                        empire_platform_api_public_client.models.aggregated_nominations_mns_or_gb_mtus.AggregatedNominationsMnsOrGb_mtus(
                            mtu = '2022-01-04T10:00Z', 
                            values = [
                                empire_platform_api_public_client.models.aggregated_nominations_mtu_value.AggregatedNominationsMtuValue(
                                    direction = 'GB_NL', 
                                    value = 56, )
                                ], 
                            netted_nominations = empire_platform_api_public_client.models.aggregated_nominations_mtu_netted_nominations.AggregatedNominationsMtuNettedNominations(
                                direction = 'GB_NL', 
                                flow = 56, ), )
                        ], ),
                nl = empire_platform_api_public_client.models.aggregated_nominations_nl.AggregatedNominationsNl(
                    mtu_size = 'MTU_15_MINS', 
                    mtus = [
                        empire_platform_api_public_client.models.aggregated_nominations_nl_mtus.AggregatedNominationsNl_mtus(
                            mtu = '2022-01-04T10:00Z', 
                            values = [
                                empire_platform_api_public_client.models.aggregated_nominations_mtu_value.AggregatedNominationsMtuValue(
                                    direction = 'GB_NL', 
                                    value = 56, )
                                ], 
                            netted_nominations = empire_platform_api_public_client.models.aggregated_nominations_mtu_netted_nominations.AggregatedNominationsMtuNettedNominations(
                                direction = 'GB_NL', 
                                flow = 56, ), 
                            eprogram_values = empire_platform_api_public_client.models.aggregated_nominations_nl_mtus_eprogram_values.AggregatedNominationsNl_mtus_eprogramValues(
                                participant = 56, 
                                system = 56, ), )
                        ], )
            )
        else:
            return AggregatedNominations(
                mns = empire_platform_api_public_client.models.aggregated_nominations_mns_or_gb.AggregatedNominationsMnsOrGb(
                    mtu_size = 'MTU_15_MINS', 
                    mtus = [
                        empire_platform_api_public_client.models.aggregated_nominations_mns_or_gb_mtus.AggregatedNominationsMnsOrGb_mtus(
                            mtu = '2022-01-04T10:00Z', 
                            values = [
                                empire_platform_api_public_client.models.aggregated_nominations_mtu_value.AggregatedNominationsMtuValue(
                                    direction = 'GB_NL', 
                                    value = 56, )
                                ], 
                            netted_nominations = empire_platform_api_public_client.models.aggregated_nominations_mtu_netted_nominations.AggregatedNominationsMtuNettedNominations(
                                direction = 'GB_NL', 
                                flow = 56, ), )
                        ], ),
                gb = empire_platform_api_public_client.models.aggregated_nominations_mns_or_gb.AggregatedNominationsMnsOrGb(
                    mtu_size = 'MTU_15_MINS', 
                    mtus = [
                        empire_platform_api_public_client.models.aggregated_nominations_mns_or_gb_mtus.AggregatedNominationsMnsOrGb_mtus(
                            mtu = '2022-01-04T10:00Z', 
                            values = [
                                empire_platform_api_public_client.models.aggregated_nominations_mtu_value.AggregatedNominationsMtuValue(
                                    direction = 'GB_NL', 
                                    value = 56, )
                                ], 
                            netted_nominations = empire_platform_api_public_client.models.aggregated_nominations_mtu_netted_nominations.AggregatedNominationsMtuNettedNominations(
                                direction = 'GB_NL', 
                                flow = 56, ), )
                        ], ),
                nl = empire_platform_api_public_client.models.aggregated_nominations_nl.AggregatedNominationsNl(
                    mtu_size = 'MTU_15_MINS', 
                    mtus = [
                        empire_platform_api_public_client.models.aggregated_nominations_nl_mtus.AggregatedNominationsNl_mtus(
                            mtu = '2022-01-04T10:00Z', 
                            values = [
                                empire_platform_api_public_client.models.aggregated_nominations_mtu_value.AggregatedNominationsMtuValue(
                                    direction = 'GB_NL', 
                                    value = 56, )
                                ], 
                            netted_nominations = empire_platform_api_public_client.models.aggregated_nominations_mtu_netted_nominations.AggregatedNominationsMtuNettedNominations(
                                direction = 'GB_NL', 
                                flow = 56, ), 
                            eprogram_values = empire_platform_api_public_client.models.aggregated_nominations_nl_mtus_eprogram_values.AggregatedNominationsNl_mtus_eprogramValues(
                                participant = 56, 
                                system = 56, ), )
                        ], ),
        )
        """

    def testAggregatedNominations(self):
        """Test AggregatedNominations"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
