# coding: utf-8

"""
    jobs-activities-api

    These API's allows you to perform activities on Jobs  # noqa: E501

    OpenAPI spec version: 1.0.3
    
    Generated by: phenom
"""

import pprint
import re  # noqa: F401

import six

class UpdateJobsHiringTeamRequest(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'op_type': 'str',
        'hiring_team_list': 'list[UpdateJobsHiringTeamRequestHiringTeamList]'
    }

    attribute_map = {
        'op_type': 'opType',
        'hiring_team_list': 'hiringTeamList'
    }

    def __init__(self, op_type=None, hiring_team_list=None):  # noqa: E501
        """UpdateJobsHiringTeamRequest - a model defined in Swagger"""  # noqa: E501
        self._op_type = None
        self._hiring_team_list = None
        self.discriminator = None
        if op_type is not None:
            self.op_type = op_type
        if hiring_team_list is not None:
            self.hiring_team_list = hiring_team_list

    @property
    def op_type(self):
        """Gets the op_type of this UpdateJobsHiringTeamRequest.  # noqa: E501


        :return: The op_type of this UpdateJobsHiringTeamRequest.  # noqa: E501
        :rtype: str
        """
        return self._op_type

    @op_type.setter
    def op_type(self, op_type):
        """Sets the op_type of this UpdateJobsHiringTeamRequest.


        :param op_type: The op_type of this UpdateJobsHiringTeamRequest.  # noqa: E501
        :type: str
        """

        self._op_type = op_type

    @property
    def hiring_team_list(self):
        """Gets the hiring_team_list of this UpdateJobsHiringTeamRequest.  # noqa: E501


        :return: The hiring_team_list of this UpdateJobsHiringTeamRequest.  # noqa: E501
        :rtype: list[UpdateJobsHiringTeamRequestHiringTeamList]
        """
        return self._hiring_team_list

    @hiring_team_list.setter
    def hiring_team_list(self, hiring_team_list):
        """Sets the hiring_team_list of this UpdateJobsHiringTeamRequest.


        :param hiring_team_list: The hiring_team_list of this UpdateJobsHiringTeamRequest.  # noqa: E501
        :type: list[UpdateJobsHiringTeamRequestHiringTeamList]
        """

        self._hiring_team_list = hiring_team_list

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
        if issubclass(UpdateJobsHiringTeamRequest, dict):
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
        if not isinstance(other, UpdateJobsHiringTeamRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
