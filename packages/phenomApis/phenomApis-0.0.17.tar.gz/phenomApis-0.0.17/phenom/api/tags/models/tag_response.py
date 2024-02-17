# coding: utf-8

"""
    tags-api

    These APIs enable tag management for candidates, offering functionalities to create, update, delete tags, and add or remove them from candidate profiles.  # noqa: E501

    OpenAPI spec version: 1.0.3
    
    Generated by: phenom
"""

import pprint
import re  # noqa: F401

import six

class TagResponse(object):
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
        'timestamp': 'str'
    }

    attribute_map = {
        'status': 'status',
        'message': 'message',
        'timestamp': 'timestamp'
    }

    def __init__(self, status=None, message=None, timestamp=None):  # noqa: E501
        """TagResponse - a model defined in Swagger"""  # noqa: E501
        self._status = None
        self._message = None
        self._timestamp = None
        self.discriminator = None
        self.status = status
        self.message = message
        self.timestamp = timestamp

    @property
    def status(self):
        """Gets the status of this TagResponse.  # noqa: E501


        :return: The status of this TagResponse.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this TagResponse.


        :param status: The status of this TagResponse.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def message(self):
        """Gets the message of this TagResponse.  # noqa: E501


        :return: The message of this TagResponse.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this TagResponse.


        :param message: The message of this TagResponse.  # noqa: E501
        :type: str
        """
        if message is None:
            raise ValueError("Invalid value for `message`, must not be `None`")  # noqa: E501

        self._message = message

    @property
    def timestamp(self):
        """Gets the timestamp of this TagResponse.  # noqa: E501


        :return: The timestamp of this TagResponse.  # noqa: E501
        :rtype: str
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this TagResponse.


        :param timestamp: The timestamp of this TagResponse.  # noqa: E501
        :type: str
        """
        if timestamp is None:
            raise ValueError("Invalid value for `timestamp`, must not be `None`")  # noqa: E501

        self._timestamp = timestamp

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
        if issubclass(TagResponse, dict):
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
        if not isinstance(other, TagResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
