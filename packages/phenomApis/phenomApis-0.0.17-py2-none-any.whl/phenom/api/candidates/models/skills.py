# coding: utf-8

"""
    candidates-api

    The Candidate APIs allows you to add, update and delete candidates.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: phenom
"""

import pprint
import re  # noqa: F401

import six

class Skills(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'data': 'SkillsData',
        'message': 'str',
        'status': 'str'
    }

    attribute_map = {
        'data': 'data',
        'message': 'message',
        'status': 'status'
    }

    def __init__(self, data=None, message=None, status=None):  # noqa: E501
        """Skills - a model defined in Swagger"""  # noqa: E501
        self._data = None
        self._message = None
        self._status = None
        self.discriminator = None
        if data is not None:
            self.data = data
        if message is not None:
            self.message = message
        if status is not None:
            self.status = status

    @property
    def data(self):
        """Gets the data of this Skills.  # noqa: E501


        :return: The data of this Skills.  # noqa: E501
        :rtype: SkillsData
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this Skills.


        :param data: The data of this Skills.  # noqa: E501
        :type: SkillsData
        """

        self._data = data

    @property
    def message(self):
        """Gets the message of this Skills.  # noqa: E501


        :return: The message of this Skills.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this Skills.


        :param message: The message of this Skills.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def status(self):
        """Gets the status of this Skills.  # noqa: E501


        :return: The status of this Skills.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Skills.


        :param status: The status of this Skills.  # noqa: E501
        :type: str
        """

        self._status = status

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
        if issubclass(Skills, dict):
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
        if not isinstance(other, Skills):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
