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


class LookupDmarcDomainResults(object):
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
        'valid': 'bool',
        'query': 'DNSLookupOptions',
        'records': 'list[DNSLookupResult]',
        'errors': 'list[str]',
        'warnings': 'list[str]'
    }

    attribute_map = {
        'valid': 'valid',
        'query': 'query',
        'records': 'records',
        'errors': 'errors',
        'warnings': 'warnings'
    }

    def __init__(self, valid=None, query=None, records=None, errors=None, warnings=None, local_vars_configuration=None):  # noqa: E501
        """LookupDmarcDomainResults - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._valid = None
        self._query = None
        self._records = None
        self._errors = None
        self._warnings = None
        self.discriminator = None

        self.valid = valid
        self.query = query
        self.records = records
        self.errors = errors
        self.warnings = warnings

    @property
    def valid(self):
        """Gets the valid of this LookupDmarcDomainResults.  # noqa: E501


        :return: The valid of this LookupDmarcDomainResults.  # noqa: E501
        :rtype: bool
        """
        return self._valid

    @valid.setter
    def valid(self, valid):
        """Sets the valid of this LookupDmarcDomainResults.


        :param valid: The valid of this LookupDmarcDomainResults.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and valid is None:  # noqa: E501
            raise ValueError("Invalid value for `valid`, must not be `None`")  # noqa: E501

        self._valid = valid

    @property
    def query(self):
        """Gets the query of this LookupDmarcDomainResults.  # noqa: E501


        :return: The query of this LookupDmarcDomainResults.  # noqa: E501
        :rtype: DNSLookupOptions
        """
        return self._query

    @query.setter
    def query(self, query):
        """Sets the query of this LookupDmarcDomainResults.


        :param query: The query of this LookupDmarcDomainResults.  # noqa: E501
        :type: DNSLookupOptions
        """
        if self.local_vars_configuration.client_side_validation and query is None:  # noqa: E501
            raise ValueError("Invalid value for `query`, must not be `None`")  # noqa: E501

        self._query = query

    @property
    def records(self):
        """Gets the records of this LookupDmarcDomainResults.  # noqa: E501


        :return: The records of this LookupDmarcDomainResults.  # noqa: E501
        :rtype: list[DNSLookupResult]
        """
        return self._records

    @records.setter
    def records(self, records):
        """Sets the records of this LookupDmarcDomainResults.


        :param records: The records of this LookupDmarcDomainResults.  # noqa: E501
        :type: list[DNSLookupResult]
        """
        if self.local_vars_configuration.client_side_validation and records is None:  # noqa: E501
            raise ValueError("Invalid value for `records`, must not be `None`")  # noqa: E501

        self._records = records

    @property
    def errors(self):
        """Gets the errors of this LookupDmarcDomainResults.  # noqa: E501


        :return: The errors of this LookupDmarcDomainResults.  # noqa: E501
        :rtype: list[str]
        """
        return self._errors

    @errors.setter
    def errors(self, errors):
        """Sets the errors of this LookupDmarcDomainResults.


        :param errors: The errors of this LookupDmarcDomainResults.  # noqa: E501
        :type: list[str]
        """
        if self.local_vars_configuration.client_side_validation and errors is None:  # noqa: E501
            raise ValueError("Invalid value for `errors`, must not be `None`")  # noqa: E501

        self._errors = errors

    @property
    def warnings(self):
        """Gets the warnings of this LookupDmarcDomainResults.  # noqa: E501


        :return: The warnings of this LookupDmarcDomainResults.  # noqa: E501
        :rtype: list[str]
        """
        return self._warnings

    @warnings.setter
    def warnings(self, warnings):
        """Sets the warnings of this LookupDmarcDomainResults.


        :param warnings: The warnings of this LookupDmarcDomainResults.  # noqa: E501
        :type: list[str]
        """
        if self.local_vars_configuration.client_side_validation and warnings is None:  # noqa: E501
            raise ValueError("Invalid value for `warnings`, must not be `None`")  # noqa: E501

        self._warnings = warnings

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
        if not isinstance(other, LookupDmarcDomainResults):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, LookupDmarcDomainResults):
            return True

        return self.to_dict() != other.to_dict()
