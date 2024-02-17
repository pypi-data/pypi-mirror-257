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

from empire_platform_api_public_client.models.default_nomination_options import DefaultNominationOptions  # noqa: E501

class TestDefaultNominationOptions(unittest.TestCase):
    """DefaultNominationOptions unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DefaultNominationOptions:
        """Test DefaultNominationOptions
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DefaultNominationOptions`
        """
        model = DefaultNominationOptions()  # noqa: E501
        if include_optional:
            return DefaultNominationOptions(
                mtu_sizes = [
                    empire_platform_api_public_client.models.mtu_size_per_timescale.MtuSizePerTimescale(
                        timescale = 'LONG_TERM', 
                        mtu_size = 'MTU_15_MINS', )
                    ]
            )
        else:
            return DefaultNominationOptions(
                mtu_sizes = [
                    empire_platform_api_public_client.models.mtu_size_per_timescale.MtuSizePerTimescale(
                        timescale = 'LONG_TERM', 
                        mtu_size = 'MTU_15_MINS', )
                    ],
        )
        """

    def testDefaultNominationOptions(self):
        """Test DefaultNominationOptions"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
