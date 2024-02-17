# coding: utf-8

"""
    communications-email

    These APIs ensures an easy integration process of email management for developers to send, read, and track email histories within applications.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: phenom
"""

import pprint
import re  # noqa: F401

import six

class UnauthorizedRequest(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'status': 'str',
        'message': 'str',
        'errors': 'list[ApiError]',
        'api_link': 'ApiLink'
    }

    attribute_map = {
        'status': 'status',
        'message': 'message',
        'errors': 'errors',
        'api_link': 'apiLink'
    }

    def __init__(self, status=None, message=None, errors=None, api_link=None):  # noqa: E501
        """UnauthorizedRequest - a model defined in Swagger"""  # noqa: E501
        self._status = None
        self._message = None
        self._errors = None
        self._api_link = None
        self.discriminator = None
        if status is not None:
            self.status = status
        if message is not None:
            self.message = message
        if errors is not None:
            self.errors = errors
        if api_link is not None:
            self.api_link = api_link

    @property
    def status(self):
        """Gets the status of this UnauthorizedRequest.  # noqa: E501

        Status of unauthorized request.  # noqa: E501

        :return: The status of this UnauthorizedRequest.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this UnauthorizedRequest.

        Status of unauthorized request.  # noqa: E501

        :param status: The status of this UnauthorizedRequest.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def message(self):
        """Gets the message of this UnauthorizedRequest.  # noqa: E501

        A user-readable message describing the Unauthorized Request.  # noqa: E501

        :return: The message of this UnauthorizedRequest.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this UnauthorizedRequest.

        A user-readable message describing the Unauthorized Request.  # noqa: E501

        :param message: The message of this UnauthorizedRequest.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def errors(self):
        """Gets the errors of this UnauthorizedRequest.  # noqa: E501


        :return: The errors of this UnauthorizedRequest.  # noqa: E501
        :rtype: list[ApiError]
        """
        return self._errors

    @errors.setter
    def errors(self, errors):
        """Sets the errors of this UnauthorizedRequest.


        :param errors: The errors of this UnauthorizedRequest.  # noqa: E501
        :type: list[ApiError]
        """

        self._errors = errors

    @property
    def api_link(self):
        """Gets the api_link of this UnauthorizedRequest.  # noqa: E501


        :return: The api_link of this UnauthorizedRequest.  # noqa: E501
        :rtype: ApiLink
        """
        return self._api_link

    @api_link.setter
    def api_link(self, api_link):
        """Sets the api_link of this UnauthorizedRequest.


        :param api_link: The api_link of this UnauthorizedRequest.  # noqa: E501
        :type: ApiLink
        """

        self._api_link = api_link

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(UnauthorizedRequest, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, UnauthorizedRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
