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

class GetAllWorkflowStatusResponseData(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'status_id': 'str',
        'name': 'str',
        'status_code': 'str',
        'status_type': 'str',
        'associated_workflows': 'list[object]',
        'created_by_recruiter_info': 'GetAllWorkflowResponseCreatedByRecruiterInfo',
        'created_date': 'float',
        'updated_date': 'float'
    }

    attribute_map = {
        'status_id': 'statusId',
        'name': 'name',
        'status_code': 'statusCode',
        'status_type': 'statusType',
        'associated_workflows': 'associatedWorkflows',
        'created_by_recruiter_info': 'createdByRecruiterInfo',
        'created_date': 'createdDate',
        'updated_date': 'updatedDate'
    }

    def __init__(self, status_id=None, name=None, status_code=None, status_type=None, associated_workflows=None, created_by_recruiter_info=None, created_date=None, updated_date=None):  # noqa: E501
        """GetAllWorkflowStatusResponseData - a model defined in Swagger"""  # noqa: E501
        self._status_id = None
        self._name = None
        self._status_code = None
        self._status_type = None
        self._associated_workflows = None
        self._created_by_recruiter_info = None
        self._created_date = None
        self._updated_date = None
        self.discriminator = None
        self.status_id = status_id
        self.name = name
        self.status_code = status_code
        self.status_type = status_type
        self.associated_workflows = associated_workflows
        self.created_by_recruiter_info = created_by_recruiter_info
        self.created_date = created_date
        self.updated_date = updated_date

    @property
    def status_id(self):
        """Gets the status_id of this GetAllWorkflowStatusResponseData.  # noqa: E501


        :return: The status_id of this GetAllWorkflowStatusResponseData.  # noqa: E501
        :rtype: str
        """
        return self._status_id

    @status_id.setter
    def status_id(self, status_id):
        """Sets the status_id of this GetAllWorkflowStatusResponseData.


        :param status_id: The status_id of this GetAllWorkflowStatusResponseData.  # noqa: E501
        :type: str
        """
        if status_id is None:
            raise ValueError("Invalid value for `status_id`, must not be `None`")  # noqa: E501

        self._status_id = status_id

    @property
    def name(self):
        """Gets the name of this GetAllWorkflowStatusResponseData.  # noqa: E501


        :return: The name of this GetAllWorkflowStatusResponseData.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GetAllWorkflowStatusResponseData.


        :param name: The name of this GetAllWorkflowStatusResponseData.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def status_code(self):
        """Gets the status_code of this GetAllWorkflowStatusResponseData.  # noqa: E501


        :return: The status_code of this GetAllWorkflowStatusResponseData.  # noqa: E501
        :rtype: str
        """
        return self._status_code

    @status_code.setter
    def status_code(self, status_code):
        """Sets the status_code of this GetAllWorkflowStatusResponseData.


        :param status_code: The status_code of this GetAllWorkflowStatusResponseData.  # noqa: E501
        :type: str
        """
        if status_code is None:
            raise ValueError("Invalid value for `status_code`, must not be `None`")  # noqa: E501

        self._status_code = status_code

    @property
    def status_type(self):
        """Gets the status_type of this GetAllWorkflowStatusResponseData.  # noqa: E501


        :return: The status_type of this GetAllWorkflowStatusResponseData.  # noqa: E501
        :rtype: str
        """
        return self._status_type

    @status_type.setter
    def status_type(self, status_type):
        """Sets the status_type of this GetAllWorkflowStatusResponseData.


        :param status_type: The status_type of this GetAllWorkflowStatusResponseData.  # noqa: E501
        :type: str
        """
        if status_type is None:
            raise ValueError("Invalid value for `status_type`, must not be `None`")  # noqa: E501

        self._status_type = status_type

    @property
    def associated_workflows(self):
        """Gets the associated_workflows of this GetAllWorkflowStatusResponseData.  # noqa: E501


        :return: The associated_workflows of this GetAllWorkflowStatusResponseData.  # noqa: E501
        :rtype: list[object]
        """
        return self._associated_workflows

    @associated_workflows.setter
    def associated_workflows(self, associated_workflows):
        """Sets the associated_workflows of this GetAllWorkflowStatusResponseData.


        :param associated_workflows: The associated_workflows of this GetAllWorkflowStatusResponseData.  # noqa: E501
        :type: list[object]
        """
        if associated_workflows is None:
            raise ValueError("Invalid value for `associated_workflows`, must not be `None`")  # noqa: E501

        self._associated_workflows = associated_workflows

    @property
    def created_by_recruiter_info(self):
        """Gets the created_by_recruiter_info of this GetAllWorkflowStatusResponseData.  # noqa: E501


        :return: The created_by_recruiter_info of this GetAllWorkflowStatusResponseData.  # noqa: E501
        :rtype: GetAllWorkflowResponseCreatedByRecruiterInfo
        """
        return self._created_by_recruiter_info

    @created_by_recruiter_info.setter
    def created_by_recruiter_info(self, created_by_recruiter_info):
        """Sets the created_by_recruiter_info of this GetAllWorkflowStatusResponseData.


        :param created_by_recruiter_info: The created_by_recruiter_info of this GetAllWorkflowStatusResponseData.  # noqa: E501
        :type: GetAllWorkflowResponseCreatedByRecruiterInfo
        """
        if created_by_recruiter_info is None:
            raise ValueError("Invalid value for `created_by_recruiter_info`, must not be `None`")  # noqa: E501

        self._created_by_recruiter_info = created_by_recruiter_info

    @property
    def created_date(self):
        """Gets the created_date of this GetAllWorkflowStatusResponseData.  # noqa: E501


        :return: The created_date of this GetAllWorkflowStatusResponseData.  # noqa: E501
        :rtype: float
        """
        return self._created_date

    @created_date.setter
    def created_date(self, created_date):
        """Sets the created_date of this GetAllWorkflowStatusResponseData.


        :param created_date: The created_date of this GetAllWorkflowStatusResponseData.  # noqa: E501
        :type: float
        """
        if created_date is None:
            raise ValueError("Invalid value for `created_date`, must not be `None`")  # noqa: E501

        self._created_date = created_date

    @property
    def updated_date(self):
        """Gets the updated_date of this GetAllWorkflowStatusResponseData.  # noqa: E501


        :return: The updated_date of this GetAllWorkflowStatusResponseData.  # noqa: E501
        :rtype: float
        """
        return self._updated_date

    @updated_date.setter
    def updated_date(self, updated_date):
        """Sets the updated_date of this GetAllWorkflowStatusResponseData.


        :param updated_date: The updated_date of this GetAllWorkflowStatusResponseData.  # noqa: E501
        :type: float
        """
        if updated_date is None:
            raise ValueError("Invalid value for `updated_date`, must not be `None`")  # noqa: E501

        self._updated_date = updated_date

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
        if issubclass(GetAllWorkflowStatusResponseData, dict):
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
        if not isinstance(other, GetAllWorkflowStatusResponseData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
