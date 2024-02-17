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


class InboxReplierDto(object):
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
        'id': 'str',
        'inbox_id': 'str',
        'name': 'str',
        'field': 'str',
        'match': 'str',
        'reply_to': 'str',
        'subject': 'str',
        '_from': 'str',
        'charset': 'str',
        'is_html': 'bool',
        'template_id': 'str',
        'template_variables': 'dict(str, object)',
        'ignore_reply_to': 'bool',
        'created_at': 'datetime'
    }

    attribute_map = {
        'id': 'id',
        'inbox_id': 'inboxId',
        'name': 'name',
        'field': 'field',
        'match': 'match',
        'reply_to': 'replyTo',
        'subject': 'subject',
        '_from': 'from',
        'charset': 'charset',
        'is_html': 'isHTML',
        'template_id': 'templateId',
        'template_variables': 'templateVariables',
        'ignore_reply_to': 'ignoreReplyTo',
        'created_at': 'createdAt'
    }

    def __init__(self, id=None, inbox_id=None, name=None, field=None, match=None, reply_to=None, subject=None, _from=None, charset=None, is_html=None, template_id=None, template_variables=None, ignore_reply_to=None, created_at=None, local_vars_configuration=None):  # noqa: E501
        """InboxReplierDto - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._inbox_id = None
        self._name = None
        self._field = None
        self._match = None
        self._reply_to = None
        self._subject = None
        self.__from = None
        self._charset = None
        self._is_html = None
        self._template_id = None
        self._template_variables = None
        self._ignore_reply_to = None
        self._created_at = None
        self.discriminator = None

        self.id = id
        self.inbox_id = inbox_id
        self.name = name
        self.field = field
        self.match = match
        self.reply_to = reply_to
        self.subject = subject
        self._from = _from
        self.charset = charset
        self.is_html = is_html
        self.template_id = template_id
        self.template_variables = template_variables
        self.ignore_reply_to = ignore_reply_to
        self.created_at = created_at

    @property
    def id(self):
        """Gets the id of this InboxReplierDto.  # noqa: E501


        :return: The id of this InboxReplierDto.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this InboxReplierDto.


        :param id: The id of this InboxReplierDto.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def inbox_id(self):
        """Gets the inbox_id of this InboxReplierDto.  # noqa: E501


        :return: The inbox_id of this InboxReplierDto.  # noqa: E501
        :rtype: str
        """
        return self._inbox_id

    @inbox_id.setter
    def inbox_id(self, inbox_id):
        """Sets the inbox_id of this InboxReplierDto.


        :param inbox_id: The inbox_id of this InboxReplierDto.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and inbox_id is None:  # noqa: E501
            raise ValueError("Invalid value for `inbox_id`, must not be `None`")  # noqa: E501

        self._inbox_id = inbox_id

    @property
    def name(self):
        """Gets the name of this InboxReplierDto.  # noqa: E501


        :return: The name of this InboxReplierDto.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this InboxReplierDto.


        :param name: The name of this InboxReplierDto.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def field(self):
        """Gets the field of this InboxReplierDto.  # noqa: E501


        :return: The field of this InboxReplierDto.  # noqa: E501
        :rtype: str
        """
        return self._field

    @field.setter
    def field(self, field):
        """Sets the field of this InboxReplierDto.


        :param field: The field of this InboxReplierDto.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and field is None:  # noqa: E501
            raise ValueError("Invalid value for `field`, must not be `None`")  # noqa: E501
        allowed_values = ["RECIPIENTS", "SENDER", "SUBJECT", "ATTACHMENTS"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and field not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `field` ({0}), must be one of {1}"  # noqa: E501
                .format(field, allowed_values)
            )

        self._field = field

    @property
    def match(self):
        """Gets the match of this InboxReplierDto.  # noqa: E501


        :return: The match of this InboxReplierDto.  # noqa: E501
        :rtype: str
        """
        return self._match

    @match.setter
    def match(self, match):
        """Sets the match of this InboxReplierDto.


        :param match: The match of this InboxReplierDto.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and match is None:  # noqa: E501
            raise ValueError("Invalid value for `match`, must not be `None`")  # noqa: E501

        self._match = match

    @property
    def reply_to(self):
        """Gets the reply_to of this InboxReplierDto.  # noqa: E501


        :return: The reply_to of this InboxReplierDto.  # noqa: E501
        :rtype: str
        """
        return self._reply_to

    @reply_to.setter
    def reply_to(self, reply_to):
        """Sets the reply_to of this InboxReplierDto.


        :param reply_to: The reply_to of this InboxReplierDto.  # noqa: E501
        :type: str
        """

        self._reply_to = reply_to

    @property
    def subject(self):
        """Gets the subject of this InboxReplierDto.  # noqa: E501


        :return: The subject of this InboxReplierDto.  # noqa: E501
        :rtype: str
        """
        return self._subject

    @subject.setter
    def subject(self, subject):
        """Sets the subject of this InboxReplierDto.


        :param subject: The subject of this InboxReplierDto.  # noqa: E501
        :type: str
        """

        self._subject = subject

    @property
    def _from(self):
        """Gets the _from of this InboxReplierDto.  # noqa: E501


        :return: The _from of this InboxReplierDto.  # noqa: E501
        :rtype: str
        """
        return self.__from

    @_from.setter
    def _from(self, _from):
        """Sets the _from of this InboxReplierDto.


        :param _from: The _from of this InboxReplierDto.  # noqa: E501
        :type: str
        """

        self.__from = _from

    @property
    def charset(self):
        """Gets the charset of this InboxReplierDto.  # noqa: E501


        :return: The charset of this InboxReplierDto.  # noqa: E501
        :rtype: str
        """
        return self._charset

    @charset.setter
    def charset(self, charset):
        """Sets the charset of this InboxReplierDto.


        :param charset: The charset of this InboxReplierDto.  # noqa: E501
        :type: str
        """

        self._charset = charset

    @property
    def is_html(self):
        """Gets the is_html of this InboxReplierDto.  # noqa: E501


        :return: The is_html of this InboxReplierDto.  # noqa: E501
        :rtype: bool
        """
        return self._is_html

    @is_html.setter
    def is_html(self, is_html):
        """Sets the is_html of this InboxReplierDto.


        :param is_html: The is_html of this InboxReplierDto.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and is_html is None:  # noqa: E501
            raise ValueError("Invalid value for `is_html`, must not be `None`")  # noqa: E501

        self._is_html = is_html

    @property
    def template_id(self):
        """Gets the template_id of this InboxReplierDto.  # noqa: E501


        :return: The template_id of this InboxReplierDto.  # noqa: E501
        :rtype: str
        """
        return self._template_id

    @template_id.setter
    def template_id(self, template_id):
        """Sets the template_id of this InboxReplierDto.


        :param template_id: The template_id of this InboxReplierDto.  # noqa: E501
        :type: str
        """

        self._template_id = template_id

    @property
    def template_variables(self):
        """Gets the template_variables of this InboxReplierDto.  # noqa: E501


        :return: The template_variables of this InboxReplierDto.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._template_variables

    @template_variables.setter
    def template_variables(self, template_variables):
        """Sets the template_variables of this InboxReplierDto.


        :param template_variables: The template_variables of this InboxReplierDto.  # noqa: E501
        :type: dict(str, object)
        """

        self._template_variables = template_variables

    @property
    def ignore_reply_to(self):
        """Gets the ignore_reply_to of this InboxReplierDto.  # noqa: E501


        :return: The ignore_reply_to of this InboxReplierDto.  # noqa: E501
        :rtype: bool
        """
        return self._ignore_reply_to

    @ignore_reply_to.setter
    def ignore_reply_to(self, ignore_reply_to):
        """Sets the ignore_reply_to of this InboxReplierDto.


        :param ignore_reply_to: The ignore_reply_to of this InboxReplierDto.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and ignore_reply_to is None:  # noqa: E501
            raise ValueError("Invalid value for `ignore_reply_to`, must not be `None`")  # noqa: E501

        self._ignore_reply_to = ignore_reply_to

    @property
    def created_at(self):
        """Gets the created_at of this InboxReplierDto.  # noqa: E501


        :return: The created_at of this InboxReplierDto.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this InboxReplierDto.


        :param created_at: The created_at of this InboxReplierDto.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_at is None:  # noqa: E501
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

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
        if not isinstance(other, InboxReplierDto):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InboxReplierDto):
            return True

        return self.to_dict() != other.to_dict()
