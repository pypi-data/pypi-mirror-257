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


class ThreadProjection(object):
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
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'user_id': 'str',
        'inbox_id': 'str',
        'to': 'list[str]',
        'bcc': 'list[str]',
        'cc': 'list[str]',
        'alias_id': 'str',
        'subject': 'str',
        'name': 'str',
        'id': 'str'
    }

    attribute_map = {
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'user_id': 'userId',
        'inbox_id': 'inboxId',
        'to': 'to',
        'bcc': 'bcc',
        'cc': 'cc',
        'alias_id': 'aliasId',
        'subject': 'subject',
        'name': 'name',
        'id': 'id'
    }

    def __init__(self, created_at=None, updated_at=None, user_id=None, inbox_id=None, to=None, bcc=None, cc=None, alias_id=None, subject=None, name=None, id=None, local_vars_configuration=None):  # noqa: E501
        """ThreadProjection - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._created_at = None
        self._updated_at = None
        self._user_id = None
        self._inbox_id = None
        self._to = None
        self._bcc = None
        self._cc = None
        self._alias_id = None
        self._subject = None
        self._name = None
        self._id = None
        self.discriminator = None

        self.created_at = created_at
        self.updated_at = updated_at
        self.user_id = user_id
        self.inbox_id = inbox_id
        self.to = to
        if bcc is not None:
            self.bcc = bcc
        if cc is not None:
            self.cc = cc
        self.alias_id = alias_id
        if subject is not None:
            self.subject = subject
        if name is not None:
            self.name = name
        self.id = id

    @property
    def created_at(self):
        """Gets the created_at of this ThreadProjection.  # noqa: E501

        Created at DateTime  # noqa: E501

        :return: The created_at of this ThreadProjection.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ThreadProjection.

        Created at DateTime  # noqa: E501

        :param created_at: The created_at of this ThreadProjection.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_at is None:  # noqa: E501
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this ThreadProjection.  # noqa: E501

        Updated at DateTime  # noqa: E501

        :return: The updated_at of this ThreadProjection.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this ThreadProjection.

        Updated at DateTime  # noqa: E501

        :param updated_at: The updated_at of this ThreadProjection.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and updated_at is None:  # noqa: E501
            raise ValueError("Invalid value for `updated_at`, must not be `None`")  # noqa: E501

        self._updated_at = updated_at

    @property
    def user_id(self):
        """Gets the user_id of this ThreadProjection.  # noqa: E501

        User ID  # noqa: E501

        :return: The user_id of this ThreadProjection.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this ThreadProjection.

        User ID  # noqa: E501

        :param user_id: The user_id of this ThreadProjection.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and user_id is None:  # noqa: E501
            raise ValueError("Invalid value for `user_id`, must not be `None`")  # noqa: E501

        self._user_id = user_id

    @property
    def inbox_id(self):
        """Gets the inbox_id of this ThreadProjection.  # noqa: E501

        Inbox ID  # noqa: E501

        :return: The inbox_id of this ThreadProjection.  # noqa: E501
        :rtype: str
        """
        return self._inbox_id

    @inbox_id.setter
    def inbox_id(self, inbox_id):
        """Sets the inbox_id of this ThreadProjection.

        Inbox ID  # noqa: E501

        :param inbox_id: The inbox_id of this ThreadProjection.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and inbox_id is None:  # noqa: E501
            raise ValueError("Invalid value for `inbox_id`, must not be `None`")  # noqa: E501

        self._inbox_id = inbox_id

    @property
    def to(self):
        """Gets the to of this ThreadProjection.  # noqa: E501

        To recipients  # noqa: E501

        :return: The to of this ThreadProjection.  # noqa: E501
        :rtype: list[str]
        """
        return self._to

    @to.setter
    def to(self, to):
        """Sets the to of this ThreadProjection.

        To recipients  # noqa: E501

        :param to: The to of this ThreadProjection.  # noqa: E501
        :type: list[str]
        """
        if self.local_vars_configuration.client_side_validation and to is None:  # noqa: E501
            raise ValueError("Invalid value for `to`, must not be `None`")  # noqa: E501

        self._to = to

    @property
    def bcc(self):
        """Gets the bcc of this ThreadProjection.  # noqa: E501

        BCC recipients  # noqa: E501

        :return: The bcc of this ThreadProjection.  # noqa: E501
        :rtype: list[str]
        """
        return self._bcc

    @bcc.setter
    def bcc(self, bcc):
        """Sets the bcc of this ThreadProjection.

        BCC recipients  # noqa: E501

        :param bcc: The bcc of this ThreadProjection.  # noqa: E501
        :type: list[str]
        """

        self._bcc = bcc

    @property
    def cc(self):
        """Gets the cc of this ThreadProjection.  # noqa: E501

        CC recipients  # noqa: E501

        :return: The cc of this ThreadProjection.  # noqa: E501
        :rtype: list[str]
        """
        return self._cc

    @cc.setter
    def cc(self, cc):
        """Sets the cc of this ThreadProjection.

        CC recipients  # noqa: E501

        :param cc: The cc of this ThreadProjection.  # noqa: E501
        :type: list[str]
        """

        self._cc = cc

    @property
    def alias_id(self):
        """Gets the alias_id of this ThreadProjection.  # noqa: E501

        Alias ID  # noqa: E501

        :return: The alias_id of this ThreadProjection.  # noqa: E501
        :rtype: str
        """
        return self._alias_id

    @alias_id.setter
    def alias_id(self, alias_id):
        """Sets the alias_id of this ThreadProjection.

        Alias ID  # noqa: E501

        :param alias_id: The alias_id of this ThreadProjection.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and alias_id is None:  # noqa: E501
            raise ValueError("Invalid value for `alias_id`, must not be `None`")  # noqa: E501

        self._alias_id = alias_id

    @property
    def subject(self):
        """Gets the subject of this ThreadProjection.  # noqa: E501

        Thread subject  # noqa: E501

        :return: The subject of this ThreadProjection.  # noqa: E501
        :rtype: str
        """
        return self._subject

    @subject.setter
    def subject(self, subject):
        """Sets the subject of this ThreadProjection.

        Thread subject  # noqa: E501

        :param subject: The subject of this ThreadProjection.  # noqa: E501
        :type: str
        """

        self._subject = subject

    @property
    def name(self):
        """Gets the name of this ThreadProjection.  # noqa: E501

        Name of thread  # noqa: E501

        :return: The name of this ThreadProjection.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ThreadProjection.

        Name of thread  # noqa: E501

        :param name: The name of this ThreadProjection.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def id(self):
        """Gets the id of this ThreadProjection.  # noqa: E501

        ID of email thread  # noqa: E501

        :return: The id of this ThreadProjection.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ThreadProjection.

        ID of email thread  # noqa: E501

        :param id: The id of this ThreadProjection.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

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
        if not isinstance(other, ThreadProjection):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ThreadProjection):
            return True

        return self.to_dict() != other.to_dict()
