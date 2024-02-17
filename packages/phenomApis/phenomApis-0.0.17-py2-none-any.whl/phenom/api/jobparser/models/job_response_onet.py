# coding: utf-8

"""
    job-parser-api

    The process of extracting important information from the raw job description is called Job Parsing. This information can include things like job titles, required skills, required experience, job duties, and qualifications.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: phenom
"""

import pprint
import re  # noqa: F401

import six

class JobResponseOnet(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'onet_code': 'str',
        'onet_title': 'str',
        'score': 'float'
    }

    attribute_map = {
        'onet_code': 'onetCode',
        'onet_title': 'onetTitle',
        'score': 'score'
    }

    def __init__(self, onet_code=None, onet_title=None, score=None):  # noqa: E501
        """JobResponseOnet - a model defined in Swagger"""  # noqa: E501
        self._onet_code = None
        self._onet_title = None
        self._score = None
        self.discriminator = None
        if onet_code is not None:
            self.onet_code = onet_code
        if onet_title is not None:
            self.onet_title = onet_title
        if score is not None:
            self.score = score

    @property
    def onet_code(self):
        """Gets the onet_code of this JobResponseOnet.  # noqa: E501

        Job special code according O*NET standard.  # noqa: E501

        :return: The onet_code of this JobResponseOnet.  # noqa: E501
        :rtype: str
        """
        return self._onet_code

    @onet_code.setter
    def onet_code(self, onet_code):
        """Sets the onet_code of this JobResponseOnet.

        Job special code according O*NET standard.  # noqa: E501

        :param onet_code: The onet_code of this JobResponseOnet.  # noqa: E501
        :type: str
        """

        self._onet_code = onet_code

    @property
    def onet_title(self):
        """Gets the onet_title of this JobResponseOnet.  # noqa: E501

        Job special title according O*NET standard.  # noqa: E501

        :return: The onet_title of this JobResponseOnet.  # noqa: E501
        :rtype: str
        """
        return self._onet_title

    @onet_title.setter
    def onet_title(self, onet_title):
        """Sets the onet_title of this JobResponseOnet.

        Job special title according O*NET standard.  # noqa: E501

        :param onet_title: The onet_title of this JobResponseOnet.  # noqa: E501
        :type: str
        """

        self._onet_title = onet_title

    @property
    def score(self):
        """Gets the score of this JobResponseOnet.  # noqa: E501

        O*NET score.  # noqa: E501

        :return: The score of this JobResponseOnet.  # noqa: E501
        :rtype: float
        """
        return self._score

    @score.setter
    def score(self, score):
        """Sets the score of this JobResponseOnet.

        O*NET score.  # noqa: E501

        :param score: The score of this JobResponseOnet.  # noqa: E501
        :type: float
        """

        self._score = score

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
        if issubclass(JobResponseOnet, dict):
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
        if not isinstance(other, JobResponseOnet):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
