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

class FitscoreResponseSkillGap(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'exact_match': 'list[str]',
        'semantic_match': 'list[str]',
        'no_match': 'list[str]'
    }

    attribute_map = {
        'exact_match': 'exactMatch',
        'semantic_match': 'semanticMatch',
        'no_match': 'noMatch'
    }

    def __init__(self, exact_match=None, semantic_match=None, no_match=None):  # noqa: E501
        """FitscoreResponseSkillGap - a model defined in Swagger"""  # noqa: E501
        self._exact_match = None
        self._semantic_match = None
        self._no_match = None
        self.discriminator = None
        if exact_match is not None:
            self.exact_match = exact_match
        if semantic_match is not None:
            self.semantic_match = semantic_match
        if no_match is not None:
            self.no_match = no_match

    @property
    def exact_match(self):
        """Gets the exact_match of this FitscoreResponseSkillGap.  # noqa: E501

        Exact Matched Skills.  # noqa: E501

        :return: The exact_match of this FitscoreResponseSkillGap.  # noqa: E501
        :rtype: list[str]
        """
        return self._exact_match

    @exact_match.setter
    def exact_match(self, exact_match):
        """Sets the exact_match of this FitscoreResponseSkillGap.

        Exact Matched Skills.  # noqa: E501

        :param exact_match: The exact_match of this FitscoreResponseSkillGap.  # noqa: E501
        :type: list[str]
        """

        self._exact_match = exact_match

    @property
    def semantic_match(self):
        """Gets the semantic_match of this FitscoreResponseSkillGap.  # noqa: E501

        Semantically Matched Skills.  # noqa: E501

        :return: The semantic_match of this FitscoreResponseSkillGap.  # noqa: E501
        :rtype: list[str]
        """
        return self._semantic_match

    @semantic_match.setter
    def semantic_match(self, semantic_match):
        """Sets the semantic_match of this FitscoreResponseSkillGap.

        Semantically Matched Skills.  # noqa: E501

        :param semantic_match: The semantic_match of this FitscoreResponseSkillGap.  # noqa: E501
        :type: list[str]
        """

        self._semantic_match = semantic_match

    @property
    def no_match(self):
        """Gets the no_match of this FitscoreResponseSkillGap.  # noqa: E501

        UnMatched Skills.  # noqa: E501

        :return: The no_match of this FitscoreResponseSkillGap.  # noqa: E501
        :rtype: list[str]
        """
        return self._no_match

    @no_match.setter
    def no_match(self, no_match):
        """Sets the no_match of this FitscoreResponseSkillGap.

        UnMatched Skills.  # noqa: E501

        :param no_match: The no_match of this FitscoreResponseSkillGap.  # noqa: E501
        :type: list[str]
        """

        self._no_match = no_match

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
        if issubclass(FitscoreResponseSkillGap, dict):
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
        if not isinstance(other, FitscoreResponseSkillGap):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
