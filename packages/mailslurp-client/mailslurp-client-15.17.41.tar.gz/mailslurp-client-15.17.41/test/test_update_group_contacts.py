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
from mailslurp_client.models.update_group_contacts import UpdateGroupContacts  # noqa: E501
from mailslurp_client.rest import ApiException

class TestUpdateGroupContacts(unittest.TestCase):
    """UpdateGroupContacts unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test UpdateGroupContacts
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = mailslurp_client.models.update_group_contacts.UpdateGroupContacts()  # noqa: E501
        if include_optional :
            return UpdateGroupContacts(
                contact_ids = [
                    '0'
                    ]
            )
        else :
            return UpdateGroupContacts(
                contact_ids = [
                    '0'
                    ],
        )

    def testUpdateGroupContacts(self):
        """Test UpdateGroupContacts"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
