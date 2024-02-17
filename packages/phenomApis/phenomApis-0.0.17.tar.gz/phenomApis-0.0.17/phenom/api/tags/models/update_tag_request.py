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

class UpdateTagRequest(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'new_tag': 'str'
    }

    attribute_map = {
        'new_tag': 'newTag'
    }

    def __init__(self, new_tag=None):  # noqa: E501
        """UpdateTagRequest - a model defined in Swagger"""  # noqa: E501
        self._new_tag = None
        self.discriminator = None
        self.new_tag = new_tag

    @property
    def new_tag(self):
        """Gets the new_tag of this UpdateTagRequest.  # noqa: E501


        :return: The new_tag of this UpdateTagRequest.  # noqa: E501
        :rtype: str
        """
        return self._new_tag

    @new_tag.setter
    def new_tag(self, new_tag):
        """Sets the new_tag of this UpdateTagRequest.


        :param new_tag: The new_tag of this UpdateTagRequest.  # noqa: E501
        :type: str
        """
        if new_tag is None:
            raise ValueError("Invalid value for `new_tag`, must not be `None`")  # noqa: E501

        self._new_tag = new_tag

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
        if issubclass(UpdateTagRequest, dict):
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
        if not isinstance(other, UpdateTagRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
