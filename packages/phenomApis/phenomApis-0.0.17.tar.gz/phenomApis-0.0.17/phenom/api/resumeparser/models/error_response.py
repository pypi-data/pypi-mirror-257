# coding: utf-8

"""
    resume-parser-api

    The Resume Parser extracts important information of a candidate such as candidate's name, contact information, email id, education, work experience, and skills, etc. from the resume using Deep learning models.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: phenom
"""

import pprint
import re  # noqa: F401

import six

class ErrorResponse(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'status': 'str',
        'errors': 'ErrorResponseErrors'
    }

    attribute_map = {
        'status': 'status',
        'errors': 'errors'
    }

    def __init__(self, status=None, errors=None):  # noqa: E501
        """ErrorResponse - a model defined in Swagger"""  # noqa: E501
        self._status = None
        self._errors = None
        self.discriminator = None
        if status is not None:
            self.status = status
        if errors is not None:
            self.errors = errors

    @property
    def status(self):
        """Gets the status of this ErrorResponse.  # noqa: E501

        Status code of encountered error.  # noqa: E501

        :return: The status of this ErrorResponse.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ErrorResponse.

        Status code of encountered error.  # noqa: E501

        :param status: The status of this ErrorResponse.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def errors(self):
        """Gets the errors of this ErrorResponse.  # noqa: E501


        :return: The errors of this ErrorResponse.  # noqa: E501
        :rtype: ErrorResponseErrors
        """
        return self._errors

    @errors.setter
    def errors(self, errors):
        """Sets the errors of this ErrorResponse.


        :param errors: The errors of this ErrorResponse.  # noqa: E501
        :type: ErrorResponseErrors
        """

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
        if issubclass(ErrorResponse, dict):
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
        if not isinstance(other, ErrorResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
