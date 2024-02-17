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

class CandidateDataCandidateImportedCandidates(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'job_category': 'str',
        'date_created': 'float',
        'job_location': 'str',
        'job_title': 'str',
        'job_seq_no': 'str',
        'locale': 'str',
        'site_type': 'str',
        'referrer_crm_user_id': 'str',
        'referrer_im_profile_id': 'str',
        'is_confidential': 'bool',
        'job_seeker_source': 'str',
        'application_id': 'str',
        'job_id': 'str',
        'franchisee_id': 'str'
    }

    attribute_map = {
        'job_category': 'jobCategory',
        'date_created': 'dateCreated',
        'job_location': 'jobLocation',
        'job_title': 'jobTitle',
        'job_seq_no': 'jobSeqNo',
        'locale': 'locale',
        'site_type': 'siteType',
        'referrer_crm_user_id': 'referrerCrmUserId',
        'referrer_im_profile_id': 'referrerImProfileId',
        'is_confidential': 'isConfidential',
        'job_seeker_source': 'jobSeekerSource',
        'application_id': 'applicationId',
        'job_id': 'jobId',
        'franchisee_id': 'franchiseeId'
    }

    def __init__(self, job_category=None, date_created=None, job_location=None, job_title=None, job_seq_no=None, locale=None, site_type=None, referrer_crm_user_id=None, referrer_im_profile_id=None, is_confidential=None, job_seeker_source=None, application_id=None, job_id=None, franchisee_id=None):  # noqa: E501
        """CandidateDataCandidateImportedCandidates - a model defined in Swagger"""  # noqa: E501
        self._job_category = None
        self._date_created = None
        self._job_location = None
        self._job_title = None
        self._job_seq_no = None
        self._locale = None
        self._site_type = None
        self._referrer_crm_user_id = None
        self._referrer_im_profile_id = None
        self._is_confidential = None
        self._job_seeker_source = None
        self._application_id = None
        self._job_id = None
        self._franchisee_id = None
        self.discriminator = None
        if job_category is not None:
            self.job_category = job_category
        if date_created is not None:
            self.date_created = date_created
        if job_location is not None:
            self.job_location = job_location
        if job_title is not None:
            self.job_title = job_title
        if job_seq_no is not None:
            self.job_seq_no = job_seq_no
        if locale is not None:
            self.locale = locale
        if site_type is not None:
            self.site_type = site_type
        if referrer_crm_user_id is not None:
            self.referrer_crm_user_id = referrer_crm_user_id
        if referrer_im_profile_id is not None:
            self.referrer_im_profile_id = referrer_im_profile_id
        if is_confidential is not None:
            self.is_confidential = is_confidential
        if job_seeker_source is not None:
            self.job_seeker_source = job_seeker_source
        if application_id is not None:
            self.application_id = application_id
        if job_id is not None:
            self.job_id = job_id
        if franchisee_id is not None:
            self.franchisee_id = franchisee_id

    @property
    def job_category(self):
        """Gets the job_category of this CandidateDataCandidateImportedCandidates.  # noqa: E501


        :return: The job_category of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :rtype: str
        """
        return self._job_category

    @job_category.setter
    def job_category(self, job_category):
        """Sets the job_category of this CandidateDataCandidateImportedCandidates.


        :param job_category: The job_category of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :type: str
        """

        self._job_category = job_category

    @property
    def date_created(self):
        """Gets the date_created of this CandidateDataCandidateImportedCandidates.  # noqa: E501


        :return: The date_created of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :rtype: float
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """Sets the date_created of this CandidateDataCandidateImportedCandidates.


        :param date_created: The date_created of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :type: float
        """

        self._date_created = date_created

    @property
    def job_location(self):
        """Gets the job_location of this CandidateDataCandidateImportedCandidates.  # noqa: E501


        :return: The job_location of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :rtype: str
        """
        return self._job_location

    @job_location.setter
    def job_location(self, job_location):
        """Sets the job_location of this CandidateDataCandidateImportedCandidates.


        :param job_location: The job_location of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :type: str
        """

        self._job_location = job_location

    @property
    def job_title(self):
        """Gets the job_title of this CandidateDataCandidateImportedCandidates.  # noqa: E501


        :return: The job_title of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :rtype: str
        """
        return self._job_title

    @job_title.setter
    def job_title(self, job_title):
        """Sets the job_title of this CandidateDataCandidateImportedCandidates.


        :param job_title: The job_title of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :type: str
        """

        self._job_title = job_title

    @property
    def job_seq_no(self):
        """Gets the job_seq_no of this CandidateDataCandidateImportedCandidates.  # noqa: E501


        :return: The job_seq_no of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :rtype: str
        """
        return self._job_seq_no

    @job_seq_no.setter
    def job_seq_no(self, job_seq_no):
        """Sets the job_seq_no of this CandidateDataCandidateImportedCandidates.


        :param job_seq_no: The job_seq_no of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :type: str
        """

        self._job_seq_no = job_seq_no

    @property
    def locale(self):
        """Gets the locale of this CandidateDataCandidateImportedCandidates.  # noqa: E501


        :return: The locale of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :rtype: str
        """
        return self._locale

    @locale.setter
    def locale(self, locale):
        """Sets the locale of this CandidateDataCandidateImportedCandidates.


        :param locale: The locale of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :type: str
        """

        self._locale = locale

    @property
    def site_type(self):
        """Gets the site_type of this CandidateDataCandidateImportedCandidates.  # noqa: E501


        :return: The site_type of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :rtype: str
        """
        return self._site_type

    @site_type.setter
    def site_type(self, site_type):
        """Sets the site_type of this CandidateDataCandidateImportedCandidates.


        :param site_type: The site_type of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :type: str
        """

        self._site_type = site_type

    @property
    def referrer_crm_user_id(self):
        """Gets the referrer_crm_user_id of this CandidateDataCandidateImportedCandidates.  # noqa: E501


        :return: The referrer_crm_user_id of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :rtype: str
        """
        return self._referrer_crm_user_id

    @referrer_crm_user_id.setter
    def referrer_crm_user_id(self, referrer_crm_user_id):
        """Sets the referrer_crm_user_id of this CandidateDataCandidateImportedCandidates.


        :param referrer_crm_user_id: The referrer_crm_user_id of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :type: str
        """

        self._referrer_crm_user_id = referrer_crm_user_id

    @property
    def referrer_im_profile_id(self):
        """Gets the referrer_im_profile_id of this CandidateDataCandidateImportedCandidates.  # noqa: E501


        :return: The referrer_im_profile_id of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :rtype: str
        """
        return self._referrer_im_profile_id

    @referrer_im_profile_id.setter
    def referrer_im_profile_id(self, referrer_im_profile_id):
        """Sets the referrer_im_profile_id of this CandidateDataCandidateImportedCandidates.


        :param referrer_im_profile_id: The referrer_im_profile_id of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :type: str
        """

        self._referrer_im_profile_id = referrer_im_profile_id

    @property
    def is_confidential(self):
        """Gets the is_confidential of this CandidateDataCandidateImportedCandidates.  # noqa: E501


        :return: The is_confidential of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :rtype: bool
        """
        return self._is_confidential

    @is_confidential.setter
    def is_confidential(self, is_confidential):
        """Sets the is_confidential of this CandidateDataCandidateImportedCandidates.


        :param is_confidential: The is_confidential of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :type: bool
        """

        self._is_confidential = is_confidential

    @property
    def job_seeker_source(self):
        """Gets the job_seeker_source of this CandidateDataCandidateImportedCandidates.  # noqa: E501


        :return: The job_seeker_source of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :rtype: str
        """
        return self._job_seeker_source

    @job_seeker_source.setter
    def job_seeker_source(self, job_seeker_source):
        """Sets the job_seeker_source of this CandidateDataCandidateImportedCandidates.


        :param job_seeker_source: The job_seeker_source of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :type: str
        """

        self._job_seeker_source = job_seeker_source

    @property
    def application_id(self):
        """Gets the application_id of this CandidateDataCandidateImportedCandidates.  # noqa: E501


        :return: The application_id of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :rtype: str
        """
        return self._application_id

    @application_id.setter
    def application_id(self, application_id):
        """Sets the application_id of this CandidateDataCandidateImportedCandidates.


        :param application_id: The application_id of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :type: str
        """

        self._application_id = application_id

    @property
    def job_id(self):
        """Gets the job_id of this CandidateDataCandidateImportedCandidates.  # noqa: E501


        :return: The job_id of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :rtype: str
        """
        return self._job_id

    @job_id.setter
    def job_id(self, job_id):
        """Sets the job_id of this CandidateDataCandidateImportedCandidates.


        :param job_id: The job_id of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :type: str
        """

        self._job_id = job_id

    @property
    def franchisee_id(self):
        """Gets the franchisee_id of this CandidateDataCandidateImportedCandidates.  # noqa: E501


        :return: The franchisee_id of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :rtype: str
        """
        return self._franchisee_id

    @franchisee_id.setter
    def franchisee_id(self, franchisee_id):
        """Sets the franchisee_id of this CandidateDataCandidateImportedCandidates.


        :param franchisee_id: The franchisee_id of this CandidateDataCandidateImportedCandidates.  # noqa: E501
        :type: str
        """

        self._franchisee_id = franchisee_id

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
        if issubclass(CandidateDataCandidateImportedCandidates, dict):
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
        if not isinstance(other, CandidateDataCandidateImportedCandidates):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
