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

class CandidateTagsAssociation(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'candidate_ids': 'list[str]',
        'tags': 'list[str]'
    }

    attribute_map = {
        'candidate_ids': 'candidateIds',
        'tags': 'tags'
    }

    def __init__(self, candidate_ids=None, tags=None):  # noqa: E501
        """CandidateTagsAssociation - a model defined in Swagger"""  # noqa: E501
        self._candidate_ids = None
        self._tags = None
        self.discriminator = None
        self.candidate_ids = candidate_ids
        self.tags = tags

    @property
    def candidate_ids(self):
        """Gets the candidate_ids of this CandidateTagsAssociation.  # noqa: E501


        :return: The candidate_ids of this CandidateTagsAssociation.  # noqa: E501
        :rtype: list[str]
        """
        return self._candidate_ids

    @candidate_ids.setter
    def candidate_ids(self, candidate_ids):
        """Sets the candidate_ids of this CandidateTagsAssociation.


        :param candidate_ids: The candidate_ids of this CandidateTagsAssociation.  # noqa: E501
        :type: list[str]
        """
        if candidate_ids is None:
            raise ValueError("Invalid value for `candidate_ids`, must not be `None`")  # noqa: E501

        self._candidate_ids = candidate_ids

    @property
    def tags(self):
        """Gets the tags of this CandidateTagsAssociation.  # noqa: E501


        :return: The tags of this CandidateTagsAssociation.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this CandidateTagsAssociation.


        :param tags: The tags of this CandidateTagsAssociation.  # noqa: E501
        :type: list[str]
        """
        if tags is None:
            raise ValueError("Invalid value for `tags`, must not be `None`")  # noqa: E501

        self._tags = tags

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
        if issubclass(CandidateTagsAssociation, dict):
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
        if not isinstance(other, CandidateTagsAssociation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
