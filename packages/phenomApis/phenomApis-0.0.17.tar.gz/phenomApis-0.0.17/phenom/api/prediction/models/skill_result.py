# coding: utf-8

"""
    prediction-api

    An API that predicts skills based on job titles and provided skill sets.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: phenom
"""

import pprint
import re  # noqa: F401

import six

class SkillResult(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'score': 'float',
        'skill': 'str'
    }

    attribute_map = {
        'score': 'score',
        'skill': 'skill'
    }

    def __init__(self, score=None, skill=None):  # noqa: E501
        """SkillResult - a model defined in Swagger"""  # noqa: E501
        self._score = None
        self._skill = None
        self.discriminator = None
        if score is not None:
            self.score = score
        if skill is not None:
            self.skill = skill

    @property
    def score(self):
        """Gets the score of this SkillResult.  # noqa: E501

        Matching score of a skill.  # noqa: E501

        :return: The score of this SkillResult.  # noqa: E501
        :rtype: float
        """
        return self._score

    @score.setter
    def score(self, score):
        """Sets the score of this SkillResult.

        Matching score of a skill.  # noqa: E501

        :param score: The score of this SkillResult.  # noqa: E501
        :type: float
        """

        self._score = score

    @property
    def skill(self):
        """Gets the skill of this SkillResult.  # noqa: E501

        Matching skill.  # noqa: E501

        :return: The skill of this SkillResult.  # noqa: E501
        :rtype: str
        """
        return self._skill

    @skill.setter
    def skill(self, skill):
        """Sets the skill of this SkillResult.

        Matching skill.  # noqa: E501

        :param skill: The skill of this SkillResult.  # noqa: E501
        :type: str
        """

        self._skill = skill

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
        if issubclass(SkillResult, dict):
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
        if not isinstance(other, SkillResult):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
