# coding: utf-8

"""
    projects-api

    These APIs allows you to create workflow statuses, which are then assigned to workflows. These workflows, containing multiple statuses, are subsequently linked to projects. Additionally, candidates are associated with projects, defining the path they are meant to follow within the established workflows.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: phenom
"""

import pprint
import re  # noqa: F401

import six

class InternalServerError(object):
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
        """InternalServerError - a model defined in Swagger"""  # noqa: E501
        self._status = None
        self._message = None
        self._timestamp = None
        self.discriminator = None
        if status is not None:
            self.status = status
        if message is not None:
            self.message = message
        if timestamp is not None:
            self.timestamp = timestamp

    @property
    def status(self):
        """Gets the status of this InternalServerError.  # noqa: E501


        :return: The status of this InternalServerError.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this InternalServerError.


        :param status: The status of this InternalServerError.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def message(self):
        """Gets the message of this InternalServerError.  # noqa: E501


        :return: The message of this InternalServerError.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this InternalServerError.


        :param message: The message of this InternalServerError.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def timestamp(self):
        """Gets the timestamp of this InternalServerError.  # noqa: E501


        :return: The timestamp of this InternalServerError.  # noqa: E501
        :rtype: str
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this InternalServerError.


        :param timestamp: The timestamp of this InternalServerError.  # noqa: E501
        :type: str
        """

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
        if issubclass(InternalServerError, dict):
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
        if not isinstance(other, InternalServerError):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
