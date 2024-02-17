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


class EmailFeaturePlatformName(object):
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
        'slug': 'str',
        'name': 'str'
    }

    attribute_map = {
        'slug': 'slug',
        'name': 'name'
    }

    def __init__(self, slug=None, name=None, local_vars_configuration=None):  # noqa: E501
        """EmailFeaturePlatformName - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._slug = None
        self._name = None
        self.discriminator = None

        self.slug = slug
        self.name = name

    @property
    def slug(self):
        """Gets the slug of this EmailFeaturePlatformName.  # noqa: E501


        :return: The slug of this EmailFeaturePlatformName.  # noqa: E501
        :rtype: str
        """
        return self._slug

    @slug.setter
    def slug(self, slug):
        """Sets the slug of this EmailFeaturePlatformName.


        :param slug: The slug of this EmailFeaturePlatformName.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and slug is None:  # noqa: E501
            raise ValueError("Invalid value for `slug`, must not be `None`")  # noqa: E501
        allowed_values = ["android", "desktop-app", "desktop-webmail", "ios", "macos", "mobile-webmail", "outlook-com", "webmail", "windows", "windows-mail"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and slug not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `slug` ({0}), must be one of {1}"  # noqa: E501
                .format(slug, allowed_values)
            )

        self._slug = slug

    @property
    def name(self):
        """Gets the name of this EmailFeaturePlatformName.  # noqa: E501


        :return: The name of this EmailFeaturePlatformName.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this EmailFeaturePlatformName.


        :param name: The name of this EmailFeaturePlatformName.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

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
        if not isinstance(other, EmailFeaturePlatformName):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, EmailFeaturePlatformName):
            return True

        return self.to_dict() != other.to_dict()
