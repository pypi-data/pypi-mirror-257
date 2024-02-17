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

class JobActivitiesData(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'job_category': 'str',
        'job_title': 'str',
        'site_type': 'str',
        'traffic_source_list': 'list[JobActivitiesTrafficSourceList]',
        'job_location': 'str',
        'updated_date': 'str',
        'field_id': 'str',
        'locale': 'str',
        'job_id': 'str',
        'action_type': 'str',
        'is_confidential': 'str',
        'created_date': 'str',
        'traffic_sources': 'list[JobActivitiesTrafficSourceList]'
    }

    attribute_map = {
        'job_category': 'jobCategory',
        'job_title': 'jobTitle',
        'site_type': 'siteType',
        'traffic_source_list': 'trafficSourceList',
        'job_location': 'jobLocation',
        'updated_date': 'updatedDate',
        'field_id': 'fieldID',
        'locale': 'locale',
        'job_id': 'jobId',
        'action_type': 'actionType',
        'is_confidential': 'isConfidential',
        'created_date': 'createdDate',
        'traffic_sources': 'trafficSources'
    }

    def __init__(self, job_category=None, job_title=None, site_type=None, traffic_source_list=None, job_location=None, updated_date=None, field_id=None, locale=None, job_id=None, action_type=None, is_confidential=None, created_date=None, traffic_sources=None):  # noqa: E501
        """JobActivitiesData - a model defined in Swagger"""  # noqa: E501
        self._job_category = None
        self._job_title = None
        self._site_type = None
        self._traffic_source_list = None
        self._job_location = None
        self._updated_date = None
        self._field_id = None
        self._locale = None
        self._job_id = None
        self._action_type = None
        self._is_confidential = None
        self._created_date = None
        self._traffic_sources = None
        self.discriminator = None
        if job_category is not None:
            self.job_category = job_category
        if job_title is not None:
            self.job_title = job_title
        if site_type is not None:
            self.site_type = site_type
        if traffic_source_list is not None:
            self.traffic_source_list = traffic_source_list
        if job_location is not None:
            self.job_location = job_location
        if updated_date is not None:
            self.updated_date = updated_date
        if field_id is not None:
            self.field_id = field_id
        if locale is not None:
            self.locale = locale
        if job_id is not None:
            self.job_id = job_id
        if action_type is not None:
            self.action_type = action_type
        if is_confidential is not None:
            self.is_confidential = is_confidential
        if created_date is not None:
            self.created_date = created_date
        if traffic_sources is not None:
            self.traffic_sources = traffic_sources

    @property
    def job_category(self):
        """Gets the job_category of this JobActivitiesData.  # noqa: E501


        :return: The job_category of this JobActivitiesData.  # noqa: E501
        :rtype: str
        """
        return self._job_category

    @job_category.setter
    def job_category(self, job_category):
        """Sets the job_category of this JobActivitiesData.


        :param job_category: The job_category of this JobActivitiesData.  # noqa: E501
        :type: str
        """

        self._job_category = job_category

    @property
    def job_title(self):
        """Gets the job_title of this JobActivitiesData.  # noqa: E501


        :return: The job_title of this JobActivitiesData.  # noqa: E501
        :rtype: str
        """
        return self._job_title

    @job_title.setter
    def job_title(self, job_title):
        """Sets the job_title of this JobActivitiesData.


        :param job_title: The job_title of this JobActivitiesData.  # noqa: E501
        :type: str
        """

        self._job_title = job_title

    @property
    def site_type(self):
        """Gets the site_type of this JobActivitiesData.  # noqa: E501


        :return: The site_type of this JobActivitiesData.  # noqa: E501
        :rtype: str
        """
        return self._site_type

    @site_type.setter
    def site_type(self, site_type):
        """Sets the site_type of this JobActivitiesData.


        :param site_type: The site_type of this JobActivitiesData.  # noqa: E501
        :type: str
        """

        self._site_type = site_type

    @property
    def traffic_source_list(self):
        """Gets the traffic_source_list of this JobActivitiesData.  # noqa: E501


        :return: The traffic_source_list of this JobActivitiesData.  # noqa: E501
        :rtype: list[JobActivitiesTrafficSourceList]
        """
        return self._traffic_source_list

    @traffic_source_list.setter
    def traffic_source_list(self, traffic_source_list):
        """Sets the traffic_source_list of this JobActivitiesData.


        :param traffic_source_list: The traffic_source_list of this JobActivitiesData.  # noqa: E501
        :type: list[JobActivitiesTrafficSourceList]
        """

        self._traffic_source_list = traffic_source_list

    @property
    def job_location(self):
        """Gets the job_location of this JobActivitiesData.  # noqa: E501


        :return: The job_location of this JobActivitiesData.  # noqa: E501
        :rtype: str
        """
        return self._job_location

    @job_location.setter
    def job_location(self, job_location):
        """Sets the job_location of this JobActivitiesData.


        :param job_location: The job_location of this JobActivitiesData.  # noqa: E501
        :type: str
        """

        self._job_location = job_location

    @property
    def updated_date(self):
        """Gets the updated_date of this JobActivitiesData.  # noqa: E501


        :return: The updated_date of this JobActivitiesData.  # noqa: E501
        :rtype: str
        """
        return self._updated_date

    @updated_date.setter
    def updated_date(self, updated_date):
        """Sets the updated_date of this JobActivitiesData.


        :param updated_date: The updated_date of this JobActivitiesData.  # noqa: E501
        :type: str
        """

        self._updated_date = updated_date

    @property
    def field_id(self):
        """Gets the field_id of this JobActivitiesData.  # noqa: E501


        :return: The field_id of this JobActivitiesData.  # noqa: E501
        :rtype: str
        """
        return self._field_id

    @field_id.setter
    def field_id(self, field_id):
        """Sets the field_id of this JobActivitiesData.


        :param field_id: The field_id of this JobActivitiesData.  # noqa: E501
        :type: str
        """

        self._field_id = field_id

    @property
    def locale(self):
        """Gets the locale of this JobActivitiesData.  # noqa: E501


        :return: The locale of this JobActivitiesData.  # noqa: E501
        :rtype: str
        """
        return self._locale

    @locale.setter
    def locale(self, locale):
        """Sets the locale of this JobActivitiesData.


        :param locale: The locale of this JobActivitiesData.  # noqa: E501
        :type: str
        """

        self._locale = locale

    @property
    def job_id(self):
        """Gets the job_id of this JobActivitiesData.  # noqa: E501


        :return: The job_id of this JobActivitiesData.  # noqa: E501
        :rtype: str
        """
        return self._job_id

    @job_id.setter
    def job_id(self, job_id):
        """Sets the job_id of this JobActivitiesData.


        :param job_id: The job_id of this JobActivitiesData.  # noqa: E501
        :type: str
        """

        self._job_id = job_id

    @property
    def action_type(self):
        """Gets the action_type of this JobActivitiesData.  # noqa: E501


        :return: The action_type of this JobActivitiesData.  # noqa: E501
        :rtype: str
        """
        return self._action_type

    @action_type.setter
    def action_type(self, action_type):
        """Sets the action_type of this JobActivitiesData.


        :param action_type: The action_type of this JobActivitiesData.  # noqa: E501
        :type: str
        """

        self._action_type = action_type

    @property
    def is_confidential(self):
        """Gets the is_confidential of this JobActivitiesData.  # noqa: E501


        :return: The is_confidential of this JobActivitiesData.  # noqa: E501
        :rtype: str
        """
        return self._is_confidential

    @is_confidential.setter
    def is_confidential(self, is_confidential):
        """Sets the is_confidential of this JobActivitiesData.


        :param is_confidential: The is_confidential of this JobActivitiesData.  # noqa: E501
        :type: str
        """

        self._is_confidential = is_confidential

    @property
    def created_date(self):
        """Gets the created_date of this JobActivitiesData.  # noqa: E501


        :return: The created_date of this JobActivitiesData.  # noqa: E501
        :rtype: str
        """
        return self._created_date

    @created_date.setter
    def created_date(self, created_date):
        """Sets the created_date of this JobActivitiesData.


        :param created_date: The created_date of this JobActivitiesData.  # noqa: E501
        :type: str
        """

        self._created_date = created_date

    @property
    def traffic_sources(self):
        """Gets the traffic_sources of this JobActivitiesData.  # noqa: E501


        :return: The traffic_sources of this JobActivitiesData.  # noqa: E501
        :rtype: list[JobActivitiesTrafficSourceList]
        """
        return self._traffic_sources

    @traffic_sources.setter
    def traffic_sources(self, traffic_sources):
        """Sets the traffic_sources of this JobActivitiesData.


        :param traffic_sources: The traffic_sources of this JobActivitiesData.  # noqa: E501
        :type: list[JobActivitiesTrafficSourceList]
        """

        self._traffic_sources = traffic_sources

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
        if issubclass(JobActivitiesData, dict):
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
        if not isinstance(other, JobActivitiesData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
