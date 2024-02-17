# coding: utf-8

"""
    candidates-api

    The Candidate APIs allows you to add, update and delete candidates.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: phenom
"""

import pprint
import re  # noqa: F401

import six

class AddSkills(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'skill_list': 'list[AddSkillsSkillList]'
    }

    attribute_map = {
        'skill_list': 'skillList'
    }

    def __init__(self, skill_list=None):  # noqa: E501
        """AddSkills - a model defined in Swagger"""  # noqa: E501
        self._skill_list = None
        self.discriminator = None
        if skill_list is not None:
            self.skill_list = skill_list

    @property
    def skill_list(self):
        """Gets the skill_list of this AddSkills.  # noqa: E501


        :return: The skill_list of this AddSkills.  # noqa: E501
        :rtype: list[AddSkillsSkillList]
        """
        return self._skill_list

    @skill_list.setter
    def skill_list(self, skill_list):
        """Sets the skill_list of this AddSkills.


        :param skill_list: The skill_list of this AddSkills.  # noqa: E501
        :type: list[AddSkillsSkillList]
        """

        self._skill_list = skill_list

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
        if issubclass(AddSkills, dict):
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
        if not isinstance(other, AddSkills):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
