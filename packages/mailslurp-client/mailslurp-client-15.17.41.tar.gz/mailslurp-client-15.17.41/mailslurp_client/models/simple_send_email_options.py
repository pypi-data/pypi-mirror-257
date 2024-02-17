# coding: utf-8

"""
    MailSlurp API

    MailSlurp is an API for sending and receiving emails from dynamically allocated email addresses. It's designed for developers and QA teams to test applications, process inbound emails, send templated notifications, attachments, and more.  ## Resources  - [Homepage](https://www.mailslurp.com) - Get an [API KEY](https://app.mailslurp.com/sign-up/) - Generated [SDK Clients](https://docs.mailslurp.com/) - [Examples](https://github.com/mailslurp/examples) repository  # noqa: E501

    The version of the OpenAPI document: 6.5.2
    Contact: contact@mailslurp.dev
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from mailslurp_client.configuration import Configuration


class SimpleSendEmailOptions(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'sender_id': 'str',
        'to': 'str',
        'body': 'str',
        'subject': 'str'
    }

    attribute_map = {
        'sender_id': 'senderId',
        'to': 'to',
        'body': 'body',
        'subject': 'subject'
    }

    def __init__(self, sender_id=None, to=None, body=None, subject=None, local_vars_configuration=None):  # noqa: E501
        """SimpleSendEmailOptions - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._sender_id = None
        self._to = None
        self._body = None
        self._subject = None
        self.discriminator = None

        self.sender_id = sender_id
        self.to = to
        self.body = body
        self.subject = subject

    @property
    def sender_id(self):
        """Gets the sender_id of this SimpleSendEmailOptions.  # noqa: E501

        ID of inbox to send from. If null an inbox will be created for sending  # noqa: E501

        :return: The sender_id of this SimpleSendEmailOptions.  # noqa: E501
        :rtype: str
        """
        return self._sender_id

    @sender_id.setter
    def sender_id(self, sender_id):
        """Sets the sender_id of this SimpleSendEmailOptions.

        ID of inbox to send from. If null an inbox will be created for sending  # noqa: E501

        :param sender_id: The sender_id of this SimpleSendEmailOptions.  # noqa: E501
        :type: str
        """

        self._sender_id = sender_id

    @property
    def to(self):
        """Gets the to of this SimpleSendEmailOptions.  # noqa: E501

        Email address to send to  # noqa: E501

        :return: The to of this SimpleSendEmailOptions.  # noqa: E501
        :rtype: str
        """
        return self._to

    @to.setter
    def to(self, to):
        """Sets the to of this SimpleSendEmailOptions.

        Email address to send to  # noqa: E501

        :param to: The to of this SimpleSendEmailOptions.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and to is None:  # noqa: E501
            raise ValueError("Invalid value for `to`, must not be `None`")  # noqa: E501

        self._to = to

    @property
    def body(self):
        """Gets the body of this SimpleSendEmailOptions.  # noqa: E501

        Body of the email message. Supports HTML  # noqa: E501

        :return: The body of this SimpleSendEmailOptions.  # noqa: E501
        :rtype: str
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this SimpleSendEmailOptions.

        Body of the email message. Supports HTML  # noqa: E501

        :param body: The body of this SimpleSendEmailOptions.  # noqa: E501
        :type: str
        """

        self._body = body

    @property
    def subject(self):
        """Gets the subject of this SimpleSendEmailOptions.  # noqa: E501

        Subject line of the email  # noqa: E501

        :return: The subject of this SimpleSendEmailOptions.  # noqa: E501
        :rtype: str
        """
        return self._subject

    @subject.setter
    def subject(self, subject):
        """Sets the subject of this SimpleSendEmailOptions.

        Subject line of the email  # noqa: E501

        :param subject: The subject of this SimpleSendEmailOptions.  # noqa: E501
        :type: str
        """

        self._subject = subject

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SimpleSendEmailOptions):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SimpleSendEmailOptions):
            return True

        return self.to_dict() != other.to_dict()
