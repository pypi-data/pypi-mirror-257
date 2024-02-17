# coding: utf-8

"""
    search-api

    These APIs helps to search and suggest based on keyword among available jobs.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: phenom
"""

import pprint
import re  # noqa: F401

import six

class JobTitlesResponseDataTitles(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'title': 'str',
        'job_id': 'str',
        'title_html': 'str'
    }

    attribute_map = {
        'title': 'title',
        'job_id': 'jobId',
        'title_html': 'titleHtml'
    }

    def __init__(self, title=None, job_id=None, title_html=None):  # noqa: E501
        """JobTitlesResponseDataTitles - a model defined in Swagger"""  # noqa: E501
        self._title = None
        self._job_id = None
        self._title_html = None
        self.discriminator = None
        if title is not None:
            self.title = title
        if job_id is not None:
            self.job_id = job_id
        if title_html is not None:
            self.title_html = title_html

    @property
    def title(self):
        """Gets the title of this JobTitlesResponseDataTitles.  # noqa: E501

        Title of the job.  # noqa: E501

        :return: The title of this JobTitlesResponseDataTitles.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this JobTitlesResponseDataTitles.

        Title of the job.  # noqa: E501

        :param title: The title of this JobTitlesResponseDataTitles.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def job_id(self):
        """Gets the job_id of this JobTitlesResponseDataTitles.  # noqa: E501

        Job ID - Unique Identifier of the job.  # noqa: E501

        :return: The job_id of this JobTitlesResponseDataTitles.  # noqa: E501
        :rtype: str
        """
        return self._job_id

    @job_id.setter
    def job_id(self, job_id):
        """Sets the job_id of this JobTitlesResponseDataTitles.

        Job ID - Unique Identifier of the job.  # noqa: E501

        :param job_id: The job_id of this JobTitlesResponseDataTitles.  # noqa: E501
        :type: str
        """

        self._job_id = job_id

    @property
    def title_html(self):
        """Gets the title_html of this JobTitlesResponseDataTitles.  # noqa: E501

        Title of the job with highlighted tags.  # noqa: E501

        :return: The title_html of this JobTitlesResponseDataTitles.  # noqa: E501
        :rtype: str
        """
        return self._title_html

    @title_html.setter
    def title_html(self, title_html):
        """Sets the title_html of this JobTitlesResponseDataTitles.

        Title of the job with highlighted tags.  # noqa: E501

        :param title_html: The title_html of this JobTitlesResponseDataTitles.  # noqa: E501
        :type: str
        """

        self._title_html = title_html

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
        if issubclass(JobTitlesResponseDataTitles, dict):
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
        if not isinstance(other, JobTitlesResponseDataTitles):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
