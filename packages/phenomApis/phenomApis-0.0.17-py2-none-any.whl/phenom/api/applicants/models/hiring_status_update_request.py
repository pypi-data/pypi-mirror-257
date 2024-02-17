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

class HiringStatusUpdateRequest(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'previous_hiring_status': 'str',
        'previous_step': 'str',
        'hiring_status': 'str',
        'hiring_step': 'str',
        'is_rejected': 'bool',
        'rejection_reason': 'str',
        'rejection_reason_id': 'str',
        'reject_code': 'str',
        'workflow_step_id': 'str',
        'hiring_status_update_date': 'str',
        'current_status_code': 'str',
        'current_step_code': 'str',
        'destination_status_code': 'str',
        'two_way_request': 'bool',
        'is_bulk_update_request': 'bool',
        'recruiter_name': 'str',
        'recruiter_email': 'str',
        'recruiter_user_id': 'str'
    }

    attribute_map = {
        'previous_hiring_status': 'previousHiringStatus',
        'previous_step': 'previousStep',
        'hiring_status': 'hiringStatus',
        'hiring_step': 'hiringStep',
        'is_rejected': 'isRejected',
        'rejection_reason': 'rejectionReason',
        'rejection_reason_id': 'rejectionReasonId',
        'reject_code': 'rejectCode',
        'workflow_step_id': 'workflowStepId',
        'hiring_status_update_date': 'hiringStatusUpdateDate',
        'current_status_code': 'currentStatusCode',
        'current_step_code': 'currentStepCode',
        'destination_status_code': 'destinationStatusCode',
        'two_way_request': 'twoWayRequest',
        'is_bulk_update_request': 'isBulkUpdateRequest',
        'recruiter_name': 'recruiterName',
        'recruiter_email': 'recruiterEmail',
        'recruiter_user_id': 'recruiterUserId'
    }

    def __init__(self, previous_hiring_status=None, previous_step=None, hiring_status=None, hiring_step=None, is_rejected=None, rejection_reason=None, rejection_reason_id=None, reject_code=None, workflow_step_id=None, hiring_status_update_date=None, current_status_code=None, current_step_code=None, destination_status_code=None, two_way_request=None, is_bulk_update_request=None, recruiter_name=None, recruiter_email=None, recruiter_user_id=None):  # noqa: E501
        """HiringStatusUpdateRequest - a model defined in Swagger"""  # noqa: E501
        self._previous_hiring_status = None
        self._previous_step = None
        self._hiring_status = None
        self._hiring_step = None
        self._is_rejected = None
        self._rejection_reason = None
        self._rejection_reason_id = None
        self._reject_code = None
        self._workflow_step_id = None
        self._hiring_status_update_date = None
        self._current_status_code = None
        self._current_step_code = None
        self._destination_status_code = None
        self._two_way_request = None
        self._is_bulk_update_request = None
        self._recruiter_name = None
        self._recruiter_email = None
        self._recruiter_user_id = None
        self.discriminator = None
        if previous_hiring_status is not None:
            self.previous_hiring_status = previous_hiring_status
        if previous_step is not None:
            self.previous_step = previous_step
        if hiring_status is not None:
            self.hiring_status = hiring_status
        if hiring_step is not None:
            self.hiring_step = hiring_step
        if is_rejected is not None:
            self.is_rejected = is_rejected
        if rejection_reason is not None:
            self.rejection_reason = rejection_reason
        if rejection_reason_id is not None:
            self.rejection_reason_id = rejection_reason_id
        if reject_code is not None:
            self.reject_code = reject_code
        if workflow_step_id is not None:
            self.workflow_step_id = workflow_step_id
        if hiring_status_update_date is not None:
            self.hiring_status_update_date = hiring_status_update_date
        if current_status_code is not None:
            self.current_status_code = current_status_code
        if current_step_code is not None:
            self.current_step_code = current_step_code
        if destination_status_code is not None:
            self.destination_status_code = destination_status_code
        if two_way_request is not None:
            self.two_way_request = two_way_request
        if is_bulk_update_request is not None:
            self.is_bulk_update_request = is_bulk_update_request
        if recruiter_name is not None:
            self.recruiter_name = recruiter_name
        if recruiter_email is not None:
            self.recruiter_email = recruiter_email
        if recruiter_user_id is not None:
            self.recruiter_user_id = recruiter_user_id

    @property
    def previous_hiring_status(self):
        """Gets the previous_hiring_status of this HiringStatusUpdateRequest.  # noqa: E501


        :return: The previous_hiring_status of this HiringStatusUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._previous_hiring_status

    @previous_hiring_status.setter
    def previous_hiring_status(self, previous_hiring_status):
        """Sets the previous_hiring_status of this HiringStatusUpdateRequest.


        :param previous_hiring_status: The previous_hiring_status of this HiringStatusUpdateRequest.  # noqa: E501
        :type: str
        """

        self._previous_hiring_status = previous_hiring_status

    @property
    def previous_step(self):
        """Gets the previous_step of this HiringStatusUpdateRequest.  # noqa: E501


        :return: The previous_step of this HiringStatusUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._previous_step

    @previous_step.setter
    def previous_step(self, previous_step):
        """Sets the previous_step of this HiringStatusUpdateRequest.


        :param previous_step: The previous_step of this HiringStatusUpdateRequest.  # noqa: E501
        :type: str
        """

        self._previous_step = previous_step

    @property
    def hiring_status(self):
        """Gets the hiring_status of this HiringStatusUpdateRequest.  # noqa: E501


        :return: The hiring_status of this HiringStatusUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._hiring_status

    @hiring_status.setter
    def hiring_status(self, hiring_status):
        """Sets the hiring_status of this HiringStatusUpdateRequest.


        :param hiring_status: The hiring_status of this HiringStatusUpdateRequest.  # noqa: E501
        :type: str
        """

        self._hiring_status = hiring_status

    @property
    def hiring_step(self):
        """Gets the hiring_step of this HiringStatusUpdateRequest.  # noqa: E501


        :return: The hiring_step of this HiringStatusUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._hiring_step

    @hiring_step.setter
    def hiring_step(self, hiring_step):
        """Sets the hiring_step of this HiringStatusUpdateRequest.


        :param hiring_step: The hiring_step of this HiringStatusUpdateRequest.  # noqa: E501
        :type: str
        """

        self._hiring_step = hiring_step

    @property
    def is_rejected(self):
        """Gets the is_rejected of this HiringStatusUpdateRequest.  # noqa: E501


        :return: The is_rejected of this HiringStatusUpdateRequest.  # noqa: E501
        :rtype: bool
        """
        return self._is_rejected

    @is_rejected.setter
    def is_rejected(self, is_rejected):
        """Sets the is_rejected of this HiringStatusUpdateRequest.


        :param is_rejected: The is_rejected of this HiringStatusUpdateRequest.  # noqa: E501
        :type: bool
        """

        self._is_rejected = is_rejected

    @property
    def rejection_reason(self):
        """Gets the rejection_reason of this HiringStatusUpdateRequest.  # noqa: E501


        :return: The rejection_reason of this HiringStatusUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._rejection_reason

    @rejection_reason.setter
    def rejection_reason(self, rejection_reason):
        """Sets the rejection_reason of this HiringStatusUpdateRequest.


        :param rejection_reason: The rejection_reason of this HiringStatusUpdateRequest.  # noqa: E501
        :type: str
        """

        self._rejection_reason = rejection_reason

    @property
    def rejection_reason_id(self):
        """Gets the rejection_reason_id of this HiringStatusUpdateRequest.  # noqa: E501


        :return: The rejection_reason_id of this HiringStatusUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._rejection_reason_id

    @rejection_reason_id.setter
    def rejection_reason_id(self, rejection_reason_id):
        """Sets the rejection_reason_id of this HiringStatusUpdateRequest.


        :param rejection_reason_id: The rejection_reason_id of this HiringStatusUpdateRequest.  # noqa: E501
        :type: str
        """

        self._rejection_reason_id = rejection_reason_id

    @property
    def reject_code(self):
        """Gets the reject_code of this HiringStatusUpdateRequest.  # noqa: E501


        :return: The reject_code of this HiringStatusUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._reject_code

    @reject_code.setter
    def reject_code(self, reject_code):
        """Sets the reject_code of this HiringStatusUpdateRequest.


        :param reject_code: The reject_code of this HiringStatusUpdateRequest.  # noqa: E501
        :type: str
        """

        self._reject_code = reject_code

    @property
    def workflow_step_id(self):
        """Gets the workflow_step_id of this HiringStatusUpdateRequest.  # noqa: E501


        :return: The workflow_step_id of this HiringStatusUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._workflow_step_id

    @workflow_step_id.setter
    def workflow_step_id(self, workflow_step_id):
        """Sets the workflow_step_id of this HiringStatusUpdateRequest.


        :param workflow_step_id: The workflow_step_id of this HiringStatusUpdateRequest.  # noqa: E501
        :type: str
        """

        self._workflow_step_id = workflow_step_id

    @property
    def hiring_status_update_date(self):
        """Gets the hiring_status_update_date of this HiringStatusUpdateRequest.  # noqa: E501


        :return: The hiring_status_update_date of this HiringStatusUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._hiring_status_update_date

    @hiring_status_update_date.setter
    def hiring_status_update_date(self, hiring_status_update_date):
        """Sets the hiring_status_update_date of this HiringStatusUpdateRequest.


        :param hiring_status_update_date: The hiring_status_update_date of this HiringStatusUpdateRequest.  # noqa: E501
        :type: str
        """

        self._hiring_status_update_date = hiring_status_update_date

    @property
    def current_status_code(self):
        """Gets the current_status_code of this HiringStatusUpdateRequest.  # noqa: E501


        :return: The current_status_code of this HiringStatusUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._current_status_code

    @current_status_code.setter
    def current_status_code(self, current_status_code):
        """Sets the current_status_code of this HiringStatusUpdateRequest.


        :param current_status_code: The current_status_code of this HiringStatusUpdateRequest.  # noqa: E501
        :type: str
        """

        self._current_status_code = current_status_code

    @property
    def current_step_code(self):
        """Gets the current_step_code of this HiringStatusUpdateRequest.  # noqa: E501


        :return: The current_step_code of this HiringStatusUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._current_step_code

    @current_step_code.setter
    def current_step_code(self, current_step_code):
        """Sets the current_step_code of this HiringStatusUpdateRequest.


        :param current_step_code: The current_step_code of this HiringStatusUpdateRequest.  # noqa: E501
        :type: str
        """

        self._current_step_code = current_step_code

    @property
    def destination_status_code(self):
        """Gets the destination_status_code of this HiringStatusUpdateRequest.  # noqa: E501


        :return: The destination_status_code of this HiringStatusUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._destination_status_code

    @destination_status_code.setter
    def destination_status_code(self, destination_status_code):
        """Sets the destination_status_code of this HiringStatusUpdateRequest.


        :param destination_status_code: The destination_status_code of this HiringStatusUpdateRequest.  # noqa: E501
        :type: str
        """

        self._destination_status_code = destination_status_code

    @property
    def two_way_request(self):
        """Gets the two_way_request of this HiringStatusUpdateRequest.  # noqa: E501


        :return: The two_way_request of this HiringStatusUpdateRequest.  # noqa: E501
        :rtype: bool
        """
        return self._two_way_request

    @two_way_request.setter
    def two_way_request(self, two_way_request):
        """Sets the two_way_request of this HiringStatusUpdateRequest.


        :param two_way_request: The two_way_request of this HiringStatusUpdateRequest.  # noqa: E501
        :type: bool
        """

        self._two_way_request = two_way_request

    @property
    def is_bulk_update_request(self):
        """Gets the is_bulk_update_request of this HiringStatusUpdateRequest.  # noqa: E501


        :return: The is_bulk_update_request of this HiringStatusUpdateRequest.  # noqa: E501
        :rtype: bool
        """
        return self._is_bulk_update_request

    @is_bulk_update_request.setter
    def is_bulk_update_request(self, is_bulk_update_request):
        """Sets the is_bulk_update_request of this HiringStatusUpdateRequest.


        :param is_bulk_update_request: The is_bulk_update_request of this HiringStatusUpdateRequest.  # noqa: E501
        :type: bool
        """

        self._is_bulk_update_request = is_bulk_update_request

    @property
    def recruiter_name(self):
        """Gets the recruiter_name of this HiringStatusUpdateRequest.  # noqa: E501


        :return: The recruiter_name of this HiringStatusUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._recruiter_name

    @recruiter_name.setter
    def recruiter_name(self, recruiter_name):
        """Sets the recruiter_name of this HiringStatusUpdateRequest.


        :param recruiter_name: The recruiter_name of this HiringStatusUpdateRequest.  # noqa: E501
        :type: str
        """

        self._recruiter_name = recruiter_name

    @property
    def recruiter_email(self):
        """Gets the recruiter_email of this HiringStatusUpdateRequest.  # noqa: E501


        :return: The recruiter_email of this HiringStatusUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._recruiter_email

    @recruiter_email.setter
    def recruiter_email(self, recruiter_email):
        """Sets the recruiter_email of this HiringStatusUpdateRequest.


        :param recruiter_email: The recruiter_email of this HiringStatusUpdateRequest.  # noqa: E501
        :type: str
        """

        self._recruiter_email = recruiter_email

    @property
    def recruiter_user_id(self):
        """Gets the recruiter_user_id of this HiringStatusUpdateRequest.  # noqa: E501


        :return: The recruiter_user_id of this HiringStatusUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._recruiter_user_id

    @recruiter_user_id.setter
    def recruiter_user_id(self, recruiter_user_id):
        """Sets the recruiter_user_id of this HiringStatusUpdateRequest.


        :param recruiter_user_id: The recruiter_user_id of this HiringStatusUpdateRequest.  # noqa: E501
        :type: str
        """

        self._recruiter_user_id = recruiter_user_id

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
        if issubclass(HiringStatusUpdateRequest, dict):
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
        if not isinstance(other, HiringStatusUpdateRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
