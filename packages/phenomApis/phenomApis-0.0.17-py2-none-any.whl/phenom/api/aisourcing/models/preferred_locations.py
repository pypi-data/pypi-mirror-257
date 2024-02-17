# coding: utf-8

"""
    aisourcing-api

    AI matching FitScore provides a concise assessment indicating how well a candidate aligns with a job based on their skills, experience, and qualifications.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: phenom
"""

import pprint
import re  # noqa: F401

import six

class PreferredLocations(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'location': 'str',
        'latlong': 'PreferredLocationsLatlong'
    }

    attribute_map = {
        'location': 'location',
        'latlong': 'latlong'
    }

    def __init__(self, location=None, latlong=None):  # noqa: E501
        """PreferredLocations - a model defined in Swagger"""  # noqa: E501
        self._location = None
        self._latlong = None
        self.discriminator = None
        if location is not None:
            self.location = location
        if latlong is not None:
            self.latlong = latlong

    @property
    def location(self):
        """Gets the location of this PreferredLocations.  # noqa: E501

        Preferred location name.  # noqa: E501

        :return: The location of this PreferredLocations.  # noqa: E501
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location):
        """Sets the location of this PreferredLocations.

        Preferred location name.  # noqa: E501

        :param location: The location of this PreferredLocations.  # noqa: E501
        :type: str
        """

        self._location = location

    @property
    def latlong(self):
        """Gets the latlong of this PreferredLocations.  # noqa: E501


        :return: The latlong of this PreferredLocations.  # noqa: E501
        :rtype: PreferredLocationsLatlong
        """
        return self._latlong

    @latlong.setter
    def latlong(self, latlong):
        """Sets the latlong of this PreferredLocations.


        :param latlong: The latlong of this PreferredLocations.  # noqa: E501
        :type: PreferredLocationsLatlong
        """

        self._latlong = latlong

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
        if issubclass(PreferredLocations, dict):
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
        if not isinstance(other, PreferredLocations):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
