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

from empire_platform_api_public_client.models.organisation_document import OrganisationDocument  # noqa: E501

class TestOrganisationDocument(unittest.TestCase):
    """OrganisationDocument unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> OrganisationDocument:
        """Test OrganisationDocument
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `OrganisationDocument`
        """
        model = OrganisationDocument()  # noqa: E501
        if include_optional:
            return OrganisationDocument(
                id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09',
                file_type = 'IMAGE',
                description = '',
                uploaded_at = '2022-01-04T00:00Z',
                uploaded_by_user = empire_platform_api_public_client.models.organisation_document_uploaded_by_user.OrganisationDocument_uploadedByUser(
                    id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                    name = '', 
                    organisation = empire_platform_api_public_client.models.organisation_document_uploaded_by_user_organisation.OrganisationDocument_uploadedByUser_organisation(
                        id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                        name = '', ), ),
                status = 'UPLOADED',
                attachment = empire_platform_api_public_client.models.attachment.Attachment(
                    id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                    file_name = '', 
                    file_size = 0, 
                    mime_type = '', 
                    url = '', )
            )
        else:
            return OrganisationDocument(
                id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09',
                file_type = 'IMAGE',
                description = '',
                uploaded_at = '2022-01-04T00:00Z',
                uploaded_by_user = empire_platform_api_public_client.models.organisation_document_uploaded_by_user.OrganisationDocument_uploadedByUser(
                    id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                    name = '', 
                    organisation = empire_platform_api_public_client.models.organisation_document_uploaded_by_user_organisation.OrganisationDocument_uploadedByUser_organisation(
                        id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                        name = '', ), ),
                status = 'UPLOADED',
        )
        """

    def testOrganisationDocument(self):
        """Test OrganisationDocument"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
