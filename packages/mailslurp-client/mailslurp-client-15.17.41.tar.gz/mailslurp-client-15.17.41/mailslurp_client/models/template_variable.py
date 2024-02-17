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


class TemplateVariable(object):
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
        'name': 'str',
        'variable_type': 'str'
    }

    attribute_map = {
        'name': 'name',
        'variable_type': 'variableType'
    }

    def __init__(self, name=None, variable_type=None, local_vars_configuration=None):  # noqa: E501
        """TemplateVariable - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._variable_type = None
        self.discriminator = None

        self.name = name
        self.variable_type = variable_type

    @property
    def name(self):
        """Gets the name of this TemplateVariable.  # noqa: E501

        Name of variable. This can be used in a template as {{name}}  # noqa: E501

        :return: The name of this TemplateVariable.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this TemplateVariable.

        Name of variable. This can be used in a template as {{name}}  # noqa: E501

        :param name: The name of this TemplateVariable.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def variable_type(self):
        """Gets the variable_type of this TemplateVariable.  # noqa: E501

        The type of variable  # noqa: E501

        :return: The variable_type of this TemplateVariable.  # noqa: E501
        :rtype: str
        """
        return self._variable_type

    @variable_type.setter
    def variable_type(self, variable_type):
        """Sets the variable_type of this TemplateVariable.

        The type of variable  # noqa: E501

        :param variable_type: The variable_type of this TemplateVariable.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and variable_type is None:  # noqa: E501
            raise ValueError("Invalid value for `variable_type`, must not be `None`")  # noqa: E501
        allowed_values = ["STRING"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and variable_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `variable_type` ({0}), must be one of {1}"  # noqa: E501
                .format(variable_type, allowed_values)
            )

        self._variable_type = variable_type

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
        if not isinstance(other, TemplateVariable):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TemplateVariable):
            return True

        return self.to_dict() != other.to_dict()
