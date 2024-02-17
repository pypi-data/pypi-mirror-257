# coding: utf-8

"""
    projects-api

    These APIs allows you to create workflow statuses, which are then assigned to workflows. These workflows, containing multiple statuses, are subsequently linked to projects. Additionally, candidates are associated with projects, defining the path they are meant to follow within the established workflows.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: phenom
"""

import pprint
import re  # noqa: F401

import six

class UpdateWorkflowRequest(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'op_type': 'str',
        'stages': 'list[UpdateWorkflowRequestStages]'
    }

    attribute_map = {
        'op_type': 'opType',
        'stages': 'stages'
    }

    def __init__(self, op_type=None, stages=None):  # noqa: E501
        """UpdateWorkflowRequest - a model defined in Swagger"""  # noqa: E501
        self._op_type = None
        self._stages = None
        self.discriminator = None
        if op_type is not None:
            self.op_type = op_type
        if stages is not None:
            self.stages = stages

    @property
    def op_type(self):
        """Gets the op_type of this UpdateWorkflowRequest.  # noqa: E501


        :return: The op_type of this UpdateWorkflowRequest.  # noqa: E501
        :rtype: str
        """
        return self._op_type

    @op_type.setter
    def op_type(self, op_type):
        """Sets the op_type of this UpdateWorkflowRequest.


        :param op_type: The op_type of this UpdateWorkflowRequest.  # noqa: E501
        :type: str
        """

        self._op_type = op_type

    @property
    def stages(self):
        """Gets the stages of this UpdateWorkflowRequest.  # noqa: E501


        :return: The stages of this UpdateWorkflowRequest.  # noqa: E501
        :rtype: list[UpdateWorkflowRequestStages]
        """
        return self._stages

    @stages.setter
    def stages(self, stages):
        """Sets the stages of this UpdateWorkflowRequest.


        :param stages: The stages of this UpdateWorkflowRequest.  # noqa: E501
        :type: list[UpdateWorkflowRequestStages]
        """

        self._stages = stages

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
        if issubclass(UpdateWorkflowRequest, dict):
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
        if not isinstance(other, UpdateWorkflowRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
