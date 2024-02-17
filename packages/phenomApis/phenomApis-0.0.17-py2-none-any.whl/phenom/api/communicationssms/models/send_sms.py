# coding: utf-8

"""
    communications-sms

    These APIs ensures an easy integration process of SMS management for developers to send, read, and track SMS histories within applications.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: phenom
"""

import pprint
import re  # noqa: F401

import six

class SendSMS(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'data': 'SendSMSData',
        'status': 'str'
    }

    attribute_map = {
        'data': 'data',
        'status': 'status'
    }

    def __init__(self, data=None, status=None):  # noqa: E501
        """SendSMS - a model defined in Swagger"""  # noqa: E501
        self._data = None
        self._status = None
        self.discriminator = None
        self.data = data
        self.status = status

    @property
    def data(self):
        """Gets the data of this SendSMS.  # noqa: E501


        :return: The data of this SendSMS.  # noqa: E501
        :rtype: SendSMSData
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this SendSMS.


        :param data: The data of this SendSMS.  # noqa: E501
        :type: SendSMSData
        """
        if data is None:
            raise ValueError("Invalid value for `data`, must not be `None`")  # noqa: E501

        self._data = data

    @property
    def status(self):
        """Gets the status of this SendSMS.  # noqa: E501

        The status of the SMS sending operation.  # noqa: E501

        :return: The status of this SendSMS.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this SendSMS.

        The status of the SMS sending operation.  # noqa: E501

        :param status: The status of this SendSMS.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

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
        if issubclass(SendSMS, dict):
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
        if not isinstance(other, SendSMS):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
