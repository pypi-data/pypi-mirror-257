# coding: utf-8

"""
    jobs-questionnarie-api

    These APIs streamline question management, providing tools to create, delete, and update questions. Additionally, they offer functionality to attach question lists to specific job profiles.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: phenom
"""

import pprint
import re  # noqa: F401

import six

class UpdateQuestionnaireTemplateRequest(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'questionnaire_name': 'str',
        'job_category': 'str',
        'as_default': 'bool',
        'auto_assign_to_jobs': 'bool',
        'template_type': 'str',
        'pre_screening_questions': 'list[UpdateQuestionnaireTemplateRequestPreScreeningQuestions]'
    }

    attribute_map = {
        'questionnaire_name': 'questionnaireName',
        'job_category': 'jobCategory',
        'as_default': 'asDefault',
        'auto_assign_to_jobs': 'autoAssignToJobs',
        'template_type': 'templateType',
        'pre_screening_questions': 'preScreeningQuestions'
    }

    def __init__(self, questionnaire_name=None, job_category=None, as_default=None, auto_assign_to_jobs=None, template_type=None, pre_screening_questions=None):  # noqa: E501
        """UpdateQuestionnaireTemplateRequest - a model defined in Swagger"""  # noqa: E501
        self._questionnaire_name = None
        self._job_category = None
        self._as_default = None
        self._auto_assign_to_jobs = None
        self._template_type = None
        self._pre_screening_questions = None
        self.discriminator = None
        if questionnaire_name is not None:
            self.questionnaire_name = questionnaire_name
        if job_category is not None:
            self.job_category = job_category
        if as_default is not None:
            self.as_default = as_default
        if auto_assign_to_jobs is not None:
            self.auto_assign_to_jobs = auto_assign_to_jobs
        if template_type is not None:
            self.template_type = template_type
        if pre_screening_questions is not None:
            self.pre_screening_questions = pre_screening_questions

    @property
    def questionnaire_name(self):
        """Gets the questionnaire_name of this UpdateQuestionnaireTemplateRequest.  # noqa: E501


        :return: The questionnaire_name of this UpdateQuestionnaireTemplateRequest.  # noqa: E501
        :rtype: str
        """
        return self._questionnaire_name

    @questionnaire_name.setter
    def questionnaire_name(self, questionnaire_name):
        """Sets the questionnaire_name of this UpdateQuestionnaireTemplateRequest.


        :param questionnaire_name: The questionnaire_name of this UpdateQuestionnaireTemplateRequest.  # noqa: E501
        :type: str
        """

        self._questionnaire_name = questionnaire_name

    @property
    def job_category(self):
        """Gets the job_category of this UpdateQuestionnaireTemplateRequest.  # noqa: E501


        :return: The job_category of this UpdateQuestionnaireTemplateRequest.  # noqa: E501
        :rtype: str
        """
        return self._job_category

    @job_category.setter
    def job_category(self, job_category):
        """Sets the job_category of this UpdateQuestionnaireTemplateRequest.


        :param job_category: The job_category of this UpdateQuestionnaireTemplateRequest.  # noqa: E501
        :type: str
        """

        self._job_category = job_category

    @property
    def as_default(self):
        """Gets the as_default of this UpdateQuestionnaireTemplateRequest.  # noqa: E501


        :return: The as_default of this UpdateQuestionnaireTemplateRequest.  # noqa: E501
        :rtype: bool
        """
        return self._as_default

    @as_default.setter
    def as_default(self, as_default):
        """Sets the as_default of this UpdateQuestionnaireTemplateRequest.


        :param as_default: The as_default of this UpdateQuestionnaireTemplateRequest.  # noqa: E501
        :type: bool
        """

        self._as_default = as_default

    @property
    def auto_assign_to_jobs(self):
        """Gets the auto_assign_to_jobs of this UpdateQuestionnaireTemplateRequest.  # noqa: E501


        :return: The auto_assign_to_jobs of this UpdateQuestionnaireTemplateRequest.  # noqa: E501
        :rtype: bool
        """
        return self._auto_assign_to_jobs

    @auto_assign_to_jobs.setter
    def auto_assign_to_jobs(self, auto_assign_to_jobs):
        """Sets the auto_assign_to_jobs of this UpdateQuestionnaireTemplateRequest.


        :param auto_assign_to_jobs: The auto_assign_to_jobs of this UpdateQuestionnaireTemplateRequest.  # noqa: E501
        :type: bool
        """

        self._auto_assign_to_jobs = auto_assign_to_jobs

    @property
    def template_type(self):
        """Gets the template_type of this UpdateQuestionnaireTemplateRequest.  # noqa: E501


        :return: The template_type of this UpdateQuestionnaireTemplateRequest.  # noqa: E501
        :rtype: str
        """
        return self._template_type

    @template_type.setter
    def template_type(self, template_type):
        """Sets the template_type of this UpdateQuestionnaireTemplateRequest.


        :param template_type: The template_type of this UpdateQuestionnaireTemplateRequest.  # noqa: E501
        :type: str
        """

        self._template_type = template_type

    @property
    def pre_screening_questions(self):
        """Gets the pre_screening_questions of this UpdateQuestionnaireTemplateRequest.  # noqa: E501


        :return: The pre_screening_questions of this UpdateQuestionnaireTemplateRequest.  # noqa: E501
        :rtype: list[UpdateQuestionnaireTemplateRequestPreScreeningQuestions]
        """
        return self._pre_screening_questions

    @pre_screening_questions.setter
    def pre_screening_questions(self, pre_screening_questions):
        """Sets the pre_screening_questions of this UpdateQuestionnaireTemplateRequest.


        :param pre_screening_questions: The pre_screening_questions of this UpdateQuestionnaireTemplateRequest.  # noqa: E501
        :type: list[UpdateQuestionnaireTemplateRequestPreScreeningQuestions]
        """

        self._pre_screening_questions = pre_screening_questions

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
        if issubclass(UpdateQuestionnaireTemplateRequest, dict):
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
        if not isinstance(other, UpdateQuestionnaireTemplateRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
