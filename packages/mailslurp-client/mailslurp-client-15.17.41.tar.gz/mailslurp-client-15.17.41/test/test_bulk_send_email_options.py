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
from mailslurp_client.models.bulk_send_email_options import BulkSendEmailOptions  # noqa: E501
from mailslurp_client.rest import ApiException

class TestBulkSendEmailOptions(unittest.TestCase):
    """BulkSendEmailOptions unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test BulkSendEmailOptions
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = mailslurp_client.models.bulk_send_email_options.BulkSendEmailOptions()  # noqa: E501
        if include_optional :
            return BulkSendEmailOptions(
                inbox_ids = [
                    '0'
                    ], 
                send_email_options = mailslurp_client.models.send_email_options.SendEmailOptions(
                    to_contacts = [
                        '0'
                        ], 
                    to_group = '0', 
                    to = [
                        '0'
                        ], 
                    from = '0', 
                    cc = [
                        '0'
                        ], 
                    bcc = [
                        '0'
                        ], 
                    subject = '0', 
                    reply_to = '0', 
                    custom_headers = {
                        'key' : '0'
                        }, 
                    body = '0', 
                    html = True, 
                    is_html = True, 
                    charset = '0', 
                    attachments = [
                        '0'
                        ], 
                    template_variables = {
                        'key' : None
                        }, 
                    template = '0', 
                    send_strategy = 'SINGLE_MESSAGE', 
                    use_inbox_name = True, 
                    add_tracking_pixel = True, 
                    filter_bounced_recipients = True, 
                    validate_email_addresses = 'VALIDATE_FILTER_REMOVE_INVALID', 
                    ignore_empty_recipients = True, 
                    is_x_amp_html = True, 
                    body_parts = [
                        mailslurp_client.models.send_email_body_part.SendEmailBodyPart(
                            content_type = '0', 
                            content_body = '0', )
                        ], )
            )
        else :
            return BulkSendEmailOptions(
                inbox_ids = [
                    '0'
                    ],
                send_email_options = mailslurp_client.models.send_email_options.SendEmailOptions(
                    to_contacts = [
                        '0'
                        ], 
                    to_group = '0', 
                    to = [
                        '0'
                        ], 
                    from = '0', 
                    cc = [
                        '0'
                        ], 
                    bcc = [
                        '0'
                        ], 
                    subject = '0', 
                    reply_to = '0', 
                    custom_headers = {
                        'key' : '0'
                        }, 
                    body = '0', 
                    html = True, 
                    is_html = True, 
                    charset = '0', 
                    attachments = [
                        '0'
                        ], 
                    template_variables = {
                        'key' : None
                        }, 
                    template = '0', 
                    send_strategy = 'SINGLE_MESSAGE', 
                    use_inbox_name = True, 
                    add_tracking_pixel = True, 
                    filter_bounced_recipients = True, 
                    validate_email_addresses = 'VALIDATE_FILTER_REMOVE_INVALID', 
                    ignore_empty_recipients = True, 
                    is_x_amp_html = True, 
                    body_parts = [
                        mailslurp_client.models.send_email_body_part.SendEmailBodyPart(
                            content_type = '0', 
                            content_body = '0', )
                        ], ),
        )

    def testBulkSendEmailOptions(self):
        """Test BulkSendEmailOptions"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
