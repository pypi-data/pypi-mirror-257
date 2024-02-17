# coding: utf-8

"""
    MailSlurp API

    MailSlurp is an API for sending and receiving emails from dynamically allocated email addresses. It's designed for developers and QA teams to test applications, process inbound emails, send templated notifications, attachments, and more.  ## Resources  - [Homepage](https://www.mailslurp.com) - Get an [API KEY](https://app.mailslurp.com/sign-up/) - Generated [SDK Clients](https://docs.mailslurp.com/) - [Examples](https://github.com/mailslurp/examples) repository  # noqa: E501

    The version of the OpenAPI document: 6.5.2
    Contact: contact@mailslurp.dev
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import mailslurp_client
from mailslurp_client.models.page_delivery_status import PageDeliveryStatus  # noqa: E501
from mailslurp_client.rest import ApiException

class TestPageDeliveryStatus(unittest.TestCase):
    """PageDeliveryStatus unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PageDeliveryStatus
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = mailslurp_client.models.page_delivery_status.PageDeliveryStatus()  # noqa: E501
        if include_optional :
            return PageDeliveryStatus(
                content = [
                    mailslurp_client.models.delivery_status_dto.DeliveryStatusDto(
                        id = '0', 
                        user_id = '0', 
                        sent_id = '0', 
                        remote_mta_ip = '0', 
                        inbox_id = '0', 
                        reporting_mta = '0', 
                        recipients = [
                            '0'
                            ], 
                        smtp_response = '0', 
                        smtp_status_code = 56, 
                        processing_time_millis = 56, 
                        received = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        subject = '0', 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                    ], 
                pageable = mailslurp_client.models.pageable_object.PageableObject(
                    page_number = 56, 
                    page_size = 56, 
                    paged = True, 
                    unpaged = True, 
                    offset = 56, 
                    sort = mailslurp_client.models.sort_object.SortObject(
                        sorted = True, 
                        unsorted = True, 
                        empty = True, ), ), 
                total_pages = 56, 
                total_elements = 56, 
                last = True, 
                number_of_elements = 56, 
                first = True, 
                size = 56, 
                number = 56, 
                sort = mailslurp_client.models.sort_object.SortObject(
                    sorted = True, 
                    unsorted = True, 
                    empty = True, ), 
                empty = True
            )
        else :
            return PageDeliveryStatus(
                total_pages = 56,
                total_elements = 56,
        )

    def testPageDeliveryStatus(self):
        """Test PageDeliveryStatus"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
