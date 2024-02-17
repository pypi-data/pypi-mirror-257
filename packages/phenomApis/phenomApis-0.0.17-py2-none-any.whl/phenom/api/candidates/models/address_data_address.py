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

class AddressDataAddress(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'city': 'str',
        'state': 'str',
        'country': 'str',
        'source': 'str',
        'created_date': 'float',
        'updated_date': 'float',
        'location_ip': 'UpdateAddressLocationIp',
        'location': 'str',
        'residential_type': 'str',
        'zip_code': 'str',
        'address_lines': 'list[str]',
        'lat_long': 'object',
        'source_type': 'object',
        'is_derived': 'bool',
        'standardized': 'bool',
        'standardized_date': 'float',
        'field_id': 'str',
        'original': 'AddressDataOriginal'
    }

    attribute_map = {
        'city': 'city',
        'state': 'state',
        'country': 'country',
        'source': 'source',
        'created_date': 'createdDate',
        'updated_date': 'updatedDate',
        'location_ip': 'locationIp',
        'location': 'location',
        'residential_type': 'residentialType',
        'zip_code': 'zipCode',
        'address_lines': 'addressLines',
        'lat_long': 'latLong',
        'source_type': 'sourceType',
        'is_derived': 'isDerived',
        'standardized': 'standardized',
        'standardized_date': 'standardizedDate',
        'field_id': 'fieldId',
        'original': 'original'
    }

    def __init__(self, city=None, state=None, country=None, source=None, created_date=None, updated_date=None, location_ip=None, location=None, residential_type=None, zip_code=None, address_lines=None, lat_long=None, source_type=None, is_derived=None, standardized=None, standardized_date=None, field_id=None, original=None):  # noqa: E501
        """AddressDataAddress - a model defined in Swagger"""  # noqa: E501
        self._city = None
        self._state = None
        self._country = None
        self._source = None
        self._created_date = None
        self._updated_date = None
        self._location_ip = None
        self._location = None
        self._residential_type = None
        self._zip_code = None
        self._address_lines = None
        self._lat_long = None
        self._source_type = None
        self._is_derived = None
        self._standardized = None
        self._standardized_date = None
        self._field_id = None
        self._original = None
        self.discriminator = None
        if city is not None:
            self.city = city
        if state is not None:
            self.state = state
        if country is not None:
            self.country = country
        if source is not None:
            self.source = source
        if created_date is not None:
            self.created_date = created_date
        if updated_date is not None:
            self.updated_date = updated_date
        if location_ip is not None:
            self.location_ip = location_ip
        if location is not None:
            self.location = location
        if residential_type is not None:
            self.residential_type = residential_type
        if zip_code is not None:
            self.zip_code = zip_code
        if address_lines is not None:
            self.address_lines = address_lines
        if lat_long is not None:
            self.lat_long = lat_long
        if source_type is not None:
            self.source_type = source_type
        if is_derived is not None:
            self.is_derived = is_derived
        if standardized is not None:
            self.standardized = standardized
        if standardized_date is not None:
            self.standardized_date = standardized_date
        if field_id is not None:
            self.field_id = field_id
        if original is not None:
            self.original = original

    @property
    def city(self):
        """Gets the city of this AddressDataAddress.  # noqa: E501


        :return: The city of this AddressDataAddress.  # noqa: E501
        :rtype: str
        """
        return self._city

    @city.setter
    def city(self, city):
        """Sets the city of this AddressDataAddress.


        :param city: The city of this AddressDataAddress.  # noqa: E501
        :type: str
        """

        self._city = city

    @property
    def state(self):
        """Gets the state of this AddressDataAddress.  # noqa: E501


        :return: The state of this AddressDataAddress.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this AddressDataAddress.


        :param state: The state of this AddressDataAddress.  # noqa: E501
        :type: str
        """

        self._state = state

    @property
    def country(self):
        """Gets the country of this AddressDataAddress.  # noqa: E501


        :return: The country of this AddressDataAddress.  # noqa: E501
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country):
        """Sets the country of this AddressDataAddress.


        :param country: The country of this AddressDataAddress.  # noqa: E501
        :type: str
        """

        self._country = country

    @property
    def source(self):
        """Gets the source of this AddressDataAddress.  # noqa: E501


        :return: The source of this AddressDataAddress.  # noqa: E501
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this AddressDataAddress.


        :param source: The source of this AddressDataAddress.  # noqa: E501
        :type: str
        """

        self._source = source

    @property
    def created_date(self):
        """Gets the created_date of this AddressDataAddress.  # noqa: E501


        :return: The created_date of this AddressDataAddress.  # noqa: E501
        :rtype: float
        """
        return self._created_date

    @created_date.setter
    def created_date(self, created_date):
        """Sets the created_date of this AddressDataAddress.


        :param created_date: The created_date of this AddressDataAddress.  # noqa: E501
        :type: float
        """

        self._created_date = created_date

    @property
    def updated_date(self):
        """Gets the updated_date of this AddressDataAddress.  # noqa: E501


        :return: The updated_date of this AddressDataAddress.  # noqa: E501
        :rtype: float
        """
        return self._updated_date

    @updated_date.setter
    def updated_date(self, updated_date):
        """Sets the updated_date of this AddressDataAddress.


        :param updated_date: The updated_date of this AddressDataAddress.  # noqa: E501
        :type: float
        """

        self._updated_date = updated_date

    @property
    def location_ip(self):
        """Gets the location_ip of this AddressDataAddress.  # noqa: E501


        :return: The location_ip of this AddressDataAddress.  # noqa: E501
        :rtype: UpdateAddressLocationIp
        """
        return self._location_ip

    @location_ip.setter
    def location_ip(self, location_ip):
        """Sets the location_ip of this AddressDataAddress.


        :param location_ip: The location_ip of this AddressDataAddress.  # noqa: E501
        :type: UpdateAddressLocationIp
        """

        self._location_ip = location_ip

    @property
    def location(self):
        """Gets the location of this AddressDataAddress.  # noqa: E501


        :return: The location of this AddressDataAddress.  # noqa: E501
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location):
        """Sets the location of this AddressDataAddress.


        :param location: The location of this AddressDataAddress.  # noqa: E501
        :type: str
        """

        self._location = location

    @property
    def residential_type(self):
        """Gets the residential_type of this AddressDataAddress.  # noqa: E501


        :return: The residential_type of this AddressDataAddress.  # noqa: E501
        :rtype: str
        """
        return self._residential_type

    @residential_type.setter
    def residential_type(self, residential_type):
        """Sets the residential_type of this AddressDataAddress.


        :param residential_type: The residential_type of this AddressDataAddress.  # noqa: E501
        :type: str
        """

        self._residential_type = residential_type

    @property
    def zip_code(self):
        """Gets the zip_code of this AddressDataAddress.  # noqa: E501


        :return: The zip_code of this AddressDataAddress.  # noqa: E501
        :rtype: str
        """
        return self._zip_code

    @zip_code.setter
    def zip_code(self, zip_code):
        """Sets the zip_code of this AddressDataAddress.


        :param zip_code: The zip_code of this AddressDataAddress.  # noqa: E501
        :type: str
        """

        self._zip_code = zip_code

    @property
    def address_lines(self):
        """Gets the address_lines of this AddressDataAddress.  # noqa: E501


        :return: The address_lines of this AddressDataAddress.  # noqa: E501
        :rtype: list[str]
        """
        return self._address_lines

    @address_lines.setter
    def address_lines(self, address_lines):
        """Sets the address_lines of this AddressDataAddress.


        :param address_lines: The address_lines of this AddressDataAddress.  # noqa: E501
        :type: list[str]
        """

        self._address_lines = address_lines

    @property
    def lat_long(self):
        """Gets the lat_long of this AddressDataAddress.  # noqa: E501


        :return: The lat_long of this AddressDataAddress.  # noqa: E501
        :rtype: object
        """
        return self._lat_long

    @lat_long.setter
    def lat_long(self, lat_long):
        """Sets the lat_long of this AddressDataAddress.


        :param lat_long: The lat_long of this AddressDataAddress.  # noqa: E501
        :type: object
        """

        self._lat_long = lat_long

    @property
    def source_type(self):
        """Gets the source_type of this AddressDataAddress.  # noqa: E501


        :return: The source_type of this AddressDataAddress.  # noqa: E501
        :rtype: object
        """
        return self._source_type

    @source_type.setter
    def source_type(self, source_type):
        """Sets the source_type of this AddressDataAddress.


        :param source_type: The source_type of this AddressDataAddress.  # noqa: E501
        :type: object
        """

        self._source_type = source_type

    @property
    def is_derived(self):
        """Gets the is_derived of this AddressDataAddress.  # noqa: E501


        :return: The is_derived of this AddressDataAddress.  # noqa: E501
        :rtype: bool
        """
        return self._is_derived

    @is_derived.setter
    def is_derived(self, is_derived):
        """Sets the is_derived of this AddressDataAddress.


        :param is_derived: The is_derived of this AddressDataAddress.  # noqa: E501
        :type: bool
        """

        self._is_derived = is_derived

    @property
    def standardized(self):
        """Gets the standardized of this AddressDataAddress.  # noqa: E501


        :return: The standardized of this AddressDataAddress.  # noqa: E501
        :rtype: bool
        """
        return self._standardized

    @standardized.setter
    def standardized(self, standardized):
        """Sets the standardized of this AddressDataAddress.


        :param standardized: The standardized of this AddressDataAddress.  # noqa: E501
        :type: bool
        """

        self._standardized = standardized

    @property
    def standardized_date(self):
        """Gets the standardized_date of this AddressDataAddress.  # noqa: E501


        :return: The standardized_date of this AddressDataAddress.  # noqa: E501
        :rtype: float
        """
        return self._standardized_date

    @standardized_date.setter
    def standardized_date(self, standardized_date):
        """Sets the standardized_date of this AddressDataAddress.


        :param standardized_date: The standardized_date of this AddressDataAddress.  # noqa: E501
        :type: float
        """

        self._standardized_date = standardized_date

    @property
    def field_id(self):
        """Gets the field_id of this AddressDataAddress.  # noqa: E501


        :return: The field_id of this AddressDataAddress.  # noqa: E501
        :rtype: str
        """
        return self._field_id

    @field_id.setter
    def field_id(self, field_id):
        """Sets the field_id of this AddressDataAddress.


        :param field_id: The field_id of this AddressDataAddress.  # noqa: E501
        :type: str
        """

        self._field_id = field_id

    @property
    def original(self):
        """Gets the original of this AddressDataAddress.  # noqa: E501


        :return: The original of this AddressDataAddress.  # noqa: E501
        :rtype: AddressDataOriginal
        """
        return self._original

    @original.setter
    def original(self, original):
        """Sets the original of this AddressDataAddress.


        :param original: The original of this AddressDataAddress.  # noqa: E501
        :type: AddressDataOriginal
        """

        self._original = original

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
        if issubclass(AddressDataAddress, dict):
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
        if not isinstance(other, AddressDataAddress):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
