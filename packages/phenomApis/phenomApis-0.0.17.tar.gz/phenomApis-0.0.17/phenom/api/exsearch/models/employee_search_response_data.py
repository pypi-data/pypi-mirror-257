# coding: utf-8

"""
    ex-search-api

    These APIs helps in searching and providing suggestions based on keywords within employee profiles.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: phenom
"""

import pprint
import re  # noqa: F401

import six

class EmployeeSearchResponseData(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'employees': 'list[EmployeeNode]',
        'facets': 'list[FacetsNode]'
    }

    attribute_map = {
        'employees': 'employees',
        'facets': 'facets'
    }

    def __init__(self, employees=None, facets=None):  # noqa: E501
        """EmployeeSearchResponseData - a model defined in Swagger"""  # noqa: E501
        self._employees = None
        self._facets = None
        self.discriminator = None
        if employees is not None:
            self.employees = employees
        if facets is not None:
            self.facets = facets

    @property
    def employees(self):
        """Gets the employees of this EmployeeSearchResponseData.  # noqa: E501


        :return: The employees of this EmployeeSearchResponseData.  # noqa: E501
        :rtype: list[EmployeeNode]
        """
        return self._employees

    @employees.setter
    def employees(self, employees):
        """Sets the employees of this EmployeeSearchResponseData.


        :param employees: The employees of this EmployeeSearchResponseData.  # noqa: E501
        :type: list[EmployeeNode]
        """

        self._employees = employees

    @property
    def facets(self):
        """Gets the facets of this EmployeeSearchResponseData.  # noqa: E501


        :return: The facets of this EmployeeSearchResponseData.  # noqa: E501
        :rtype: list[FacetsNode]
        """
        return self._facets

    @facets.setter
    def facets(self, facets):
        """Sets the facets of this EmployeeSearchResponseData.


        :param facets: The facets of this EmployeeSearchResponseData.  # noqa: E501
        :type: list[FacetsNode]
        """

        self._facets = facets

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
        if issubclass(EmployeeSearchResponseData, dict):
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
        if not isinstance(other, EmployeeSearchResponseData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
