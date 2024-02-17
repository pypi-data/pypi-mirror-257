# coding: utf-8

"""
    applicants-api

    The Candidate APIs allows you to add, update and delete candidates.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: phenom
"""

import pprint
import re  # noqa: F401

import six

class ApplicantsData(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'candidates': 'list[ApplicantsDataCandidates]'
    }

    attribute_map = {
        'candidates': 'candidates'
    }

    def __init__(self, candidates=None):  # noqa: E501
        """ApplicantsData - a model defined in Swagger"""  # noqa: E501
        self._candidates = None
        self.discriminator = None
        if candidates is not None:
            self.candidates = candidates

    @property
    def candidates(self):
        """Gets the candidates of this ApplicantsData.  # noqa: E501


        :return: The candidates of this ApplicantsData.  # noqa: E501
        :rtype: list[ApplicantsDataCandidates]
        """
        return self._candidates

    @candidates.setter
    def candidates(self, candidates):
        """Sets the candidates of this ApplicantsData.


        :param candidates: The candidates of this ApplicantsData.  # noqa: E501
        :type: list[ApplicantsDataCandidates]
        """

        self._candidates = candidates

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
        if issubclass(ApplicantsData, dict):
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
        if not isinstance(other, ApplicantsData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
