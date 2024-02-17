# coding: utf-8

"""
    campaigns-sms

    These APIs ensures an easy integration process of SMS management for developers to send, read, and track SMS campaigns within applications.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: phenom
"""

import pprint
import re  # noqa: F401

import six

class SendSMSRequest(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'message': 'str',
        'phone_number': 'str'
    }

    attribute_map = {
        'message': 'message',
        'phone_number': 'phoneNumber'
    }

    def __init__(self, message=None, phone_number=None):  # noqa: E501
        """SendSMSRequest - a model defined in Swagger"""  # noqa: E501
        self._message = None
        self._phone_number = None
        self.discriminator = None
        self.message = message
        self.phone_number = phone_number

    @property
    def message(self):
        """Gets the message of this SendSMSRequest.  # noqa: E501

        The user readable information regarding the send sms request.  # noqa: E501

        :return: The message of this SendSMSRequest.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this SendSMSRequest.

        The user readable information regarding the send sms request.  # noqa: E501

        :param message: The message of this SendSMSRequest.  # noqa: E501
        :type: str
        """
        if message is None:
            raise ValueError("Invalid value for `message`, must not be `None`")  # noqa: E501

        self._message = message

    @property
    def phone_number(self):
        """Gets the phone_number of this SendSMSRequest.  # noqa: E501

        Phone Number associated with the send sms request.  # noqa: E501

        :return: The phone_number of this SendSMSRequest.  # noqa: E501
        :rtype: str
        """
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        """Sets the phone_number of this SendSMSRequest.

        Phone Number associated with the send sms request.  # noqa: E501

        :param phone_number: The phone_number of this SendSMSRequest.  # noqa: E501
        :type: str
        """
        if phone_number is None:
            raise ValueError("Invalid value for `phone_number`, must not be `None`")  # noqa: E501

        self._phone_number = phone_number

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
        if issubclass(SendSMSRequest, dict):
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
        if not isinstance(other, SendSMSRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
