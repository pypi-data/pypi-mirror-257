# coding: utf-8

"""
    notes-api

    The Note APIs allows you to Add, Update and Delete Notes  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: phenom
"""

import pprint
import re  # noqa: F401

import six

class BadRequestError(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'status': 'str',
        'errors': 'list[BadRequestErrorErrors]'
    }

    attribute_map = {
        'status': 'status',
        'errors': 'errors'
    }

    def __init__(self, status=None, errors=None):  # noqa: E501
        """BadRequestError - a model defined in Swagger"""  # noqa: E501
        self._status = None
        self._errors = None
        self.discriminator = None
        self.status = status
        self.errors = errors

    @property
    def status(self):
        """Gets the status of this BadRequestError.  # noqa: E501


        :return: The status of this BadRequestError.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this BadRequestError.


        :param status: The status of this BadRequestError.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def errors(self):
        """Gets the errors of this BadRequestError.  # noqa: E501


        :return: The errors of this BadRequestError.  # noqa: E501
        :rtype: list[BadRequestErrorErrors]
        """
        return self._errors

    @errors.setter
    def errors(self, errors):
        """Sets the errors of this BadRequestError.


        :param errors: The errors of this BadRequestError.  # noqa: E501
        :type: list[BadRequestErrorErrors]
        """
        if errors is None:
            raise ValueError("Invalid value for `errors`, must not be `None`")  # noqa: E501

        self._errors = errors

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
        if issubclass(BadRequestError, dict):
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
        if not isinstance(other, BadRequestError):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
