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

class EducationDataEducations(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'school_and_university': 'str',
        'university_name': 'str',
        'end_date': 'float',
        'is_high_education': 'bool',
        'field_id': 'str',
        'university_name_org': 'str',
        'priority': 'float',
        'source': 'str',
        'transaction_id': 'str'
    }

    attribute_map = {
        'school_and_university': 'schoolAndUniversity',
        'university_name': 'universityName',
        'end_date': 'endDate',
        'is_high_education': 'isHighEducation',
        'field_id': 'fieldID',
        'university_name_org': 'universityName_org',
        'priority': 'priority',
        'source': 'source',
        'transaction_id': 'transactionId'
    }

    def __init__(self, school_and_university=None, university_name=None, end_date=None, is_high_education=None, field_id=None, university_name_org=None, priority=None, source=None, transaction_id=None):  # noqa: E501
        """EducationDataEducations - a model defined in Swagger"""  # noqa: E501
        self._school_and_university = None
        self._university_name = None
        self._end_date = None
        self._is_high_education = None
        self._field_id = None
        self._university_name_org = None
        self._priority = None
        self._source = None
        self._transaction_id = None
        self.discriminator = None
        if school_and_university is not None:
            self.school_and_university = school_and_university
        if university_name is not None:
            self.university_name = university_name
        if end_date is not None:
            self.end_date = end_date
        if is_high_education is not None:
            self.is_high_education = is_high_education
        if field_id is not None:
            self.field_id = field_id
        if university_name_org is not None:
            self.university_name_org = university_name_org
        if priority is not None:
            self.priority = priority
        if source is not None:
            self.source = source
        if transaction_id is not None:
            self.transaction_id = transaction_id

    @property
    def school_and_university(self):
        """Gets the school_and_university of this EducationDataEducations.  # noqa: E501


        :return: The school_and_university of this EducationDataEducations.  # noqa: E501
        :rtype: str
        """
        return self._school_and_university

    @school_and_university.setter
    def school_and_university(self, school_and_university):
        """Sets the school_and_university of this EducationDataEducations.


        :param school_and_university: The school_and_university of this EducationDataEducations.  # noqa: E501
        :type: str
        """

        self._school_and_university = school_and_university

    @property
    def university_name(self):
        """Gets the university_name of this EducationDataEducations.  # noqa: E501


        :return: The university_name of this EducationDataEducations.  # noqa: E501
        :rtype: str
        """
        return self._university_name

    @university_name.setter
    def university_name(self, university_name):
        """Sets the university_name of this EducationDataEducations.


        :param university_name: The university_name of this EducationDataEducations.  # noqa: E501
        :type: str
        """

        self._university_name = university_name

    @property
    def end_date(self):
        """Gets the end_date of this EducationDataEducations.  # noqa: E501


        :return: The end_date of this EducationDataEducations.  # noqa: E501
        :rtype: float
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """Sets the end_date of this EducationDataEducations.


        :param end_date: The end_date of this EducationDataEducations.  # noqa: E501
        :type: float
        """

        self._end_date = end_date

    @property
    def is_high_education(self):
        """Gets the is_high_education of this EducationDataEducations.  # noqa: E501


        :return: The is_high_education of this EducationDataEducations.  # noqa: E501
        :rtype: bool
        """
        return self._is_high_education

    @is_high_education.setter
    def is_high_education(self, is_high_education):
        """Sets the is_high_education of this EducationDataEducations.


        :param is_high_education: The is_high_education of this EducationDataEducations.  # noqa: E501
        :type: bool
        """

        self._is_high_education = is_high_education

    @property
    def field_id(self):
        """Gets the field_id of this EducationDataEducations.  # noqa: E501


        :return: The field_id of this EducationDataEducations.  # noqa: E501
        :rtype: str
        """
        return self._field_id

    @field_id.setter
    def field_id(self, field_id):
        """Sets the field_id of this EducationDataEducations.


        :param field_id: The field_id of this EducationDataEducations.  # noqa: E501
        :type: str
        """

        self._field_id = field_id

    @property
    def university_name_org(self):
        """Gets the university_name_org of this EducationDataEducations.  # noqa: E501


        :return: The university_name_org of this EducationDataEducations.  # noqa: E501
        :rtype: str
        """
        return self._university_name_org

    @university_name_org.setter
    def university_name_org(self, university_name_org):
        """Sets the university_name_org of this EducationDataEducations.


        :param university_name_org: The university_name_org of this EducationDataEducations.  # noqa: E501
        :type: str
        """

        self._university_name_org = university_name_org

    @property
    def priority(self):
        """Gets the priority of this EducationDataEducations.  # noqa: E501


        :return: The priority of this EducationDataEducations.  # noqa: E501
        :rtype: float
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """Sets the priority of this EducationDataEducations.


        :param priority: The priority of this EducationDataEducations.  # noqa: E501
        :type: float
        """

        self._priority = priority

    @property
    def source(self):
        """Gets the source of this EducationDataEducations.  # noqa: E501


        :return: The source of this EducationDataEducations.  # noqa: E501
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this EducationDataEducations.


        :param source: The source of this EducationDataEducations.  # noqa: E501
        :type: str
        """

        self._source = source

    @property
    def transaction_id(self):
        """Gets the transaction_id of this EducationDataEducations.  # noqa: E501


        :return: The transaction_id of this EducationDataEducations.  # noqa: E501
        :rtype: str
        """
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, transaction_id):
        """Sets the transaction_id of this EducationDataEducations.


        :param transaction_id: The transaction_id of this EducationDataEducations.  # noqa: E501
        :type: str
        """

        self._transaction_id = transaction_id

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
        if issubclass(EducationDataEducations, dict):
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
        if not isinstance(other, EducationDataEducations):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
