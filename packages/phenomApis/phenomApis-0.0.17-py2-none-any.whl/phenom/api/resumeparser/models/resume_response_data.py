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

class ResumeResponseData(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'resumedata': 'ResumeResponseDataResumedata'
    }

    attribute_map = {
        'resumedata': 'resumedata'
    }

    def __init__(self, resumedata=None):  # noqa: E501
        """ResumeResponseData - a model defined in Swagger"""  # noqa: E501
        self._resumedata = None
        self.discriminator = None
        if resumedata is not None:
            self.resumedata = resumedata

    @property
    def resumedata(self):
        """Gets the resumedata of this ResumeResponseData.  # noqa: E501


        :return: The resumedata of this ResumeResponseData.  # noqa: E501
        :rtype: ResumeResponseDataResumedata
        """
        return self._resumedata

    @resumedata.setter
    def resumedata(self, resumedata):
        """Sets the resumedata of this ResumeResponseData.


        :param resumedata: The resumedata of this ResumeResponseData.  # noqa: E501
        :type: ResumeResponseDataResumedata
        """

        self._resumedata = resumedata

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
        if issubclass(ResumeResponseData, dict):
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
        if not isinstance(other, ResumeResponseData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
