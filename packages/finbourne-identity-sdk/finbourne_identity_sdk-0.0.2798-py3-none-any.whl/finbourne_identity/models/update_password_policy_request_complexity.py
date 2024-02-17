# coding: utf-8

"""
    FINBOURNE Identity Service API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.0.2798
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from finbourne_identity.configuration import Configuration


class UpdatePasswordPolicyRequestComplexity(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'min_length': 'int',
        'exclude_first_name': 'bool',
        'exclude_last_name': 'bool'
    }

    attribute_map = {
        'min_length': 'minLength',
        'exclude_first_name': 'excludeFirstName',
        'exclude_last_name': 'excludeLastName'
    }

    required_map = {
        'min_length': 'required',
        'exclude_first_name': 'required',
        'exclude_last_name': 'required'
    }

    def __init__(self, min_length=None, exclude_first_name=None, exclude_last_name=None, local_vars_configuration=None):  # noqa: E501
        """UpdatePasswordPolicyRequestComplexity - a model defined in OpenAPI"
        
        :param min_length:  The minimum length for a password (required)
        :type min_length: int
        :param exclude_first_name:  Rule determining whether a user's first name should be permitted in their password (required)
        :type exclude_first_name: bool
        :param exclude_last_name:  Rule determining whether a user's last name should be permitted in their password (required)
        :type exclude_last_name: bool

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._min_length = None
        self._exclude_first_name = None
        self._exclude_last_name = None
        self.discriminator = None

        self.min_length = min_length
        self.exclude_first_name = exclude_first_name
        self.exclude_last_name = exclude_last_name

    @property
    def min_length(self):
        """Gets the min_length of this UpdatePasswordPolicyRequestComplexity.  # noqa: E501

        The minimum length for a password  # noqa: E501

        :return: The min_length of this UpdatePasswordPolicyRequestComplexity.  # noqa: E501
        :rtype: int
        """
        return self._min_length

    @min_length.setter
    def min_length(self, min_length):
        """Sets the min_length of this UpdatePasswordPolicyRequestComplexity.

        The minimum length for a password  # noqa: E501

        :param min_length: The min_length of this UpdatePasswordPolicyRequestComplexity.  # noqa: E501
        :type min_length: int
        """
        if self.local_vars_configuration.client_side_validation and min_length is None:  # noqa: E501
            raise ValueError("Invalid value for `min_length`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                min_length is not None and min_length > 30):  # noqa: E501
            raise ValueError("Invalid value for `min_length`, must be a value less than or equal to `30`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                min_length is not None and min_length < 12):  # noqa: E501
            raise ValueError("Invalid value for `min_length`, must be a value greater than or equal to `12`")  # noqa: E501

        self._min_length = min_length

    @property
    def exclude_first_name(self):
        """Gets the exclude_first_name of this UpdatePasswordPolicyRequestComplexity.  # noqa: E501

        Rule determining whether a user's first name should be permitted in their password  # noqa: E501

        :return: The exclude_first_name of this UpdatePasswordPolicyRequestComplexity.  # noqa: E501
        :rtype: bool
        """
        return self._exclude_first_name

    @exclude_first_name.setter
    def exclude_first_name(self, exclude_first_name):
        """Sets the exclude_first_name of this UpdatePasswordPolicyRequestComplexity.

        Rule determining whether a user's first name should be permitted in their password  # noqa: E501

        :param exclude_first_name: The exclude_first_name of this UpdatePasswordPolicyRequestComplexity.  # noqa: E501
        :type exclude_first_name: bool
        """
        if self.local_vars_configuration.client_side_validation and exclude_first_name is None:  # noqa: E501
            raise ValueError("Invalid value for `exclude_first_name`, must not be `None`")  # noqa: E501

        self._exclude_first_name = exclude_first_name

    @property
    def exclude_last_name(self):
        """Gets the exclude_last_name of this UpdatePasswordPolicyRequestComplexity.  # noqa: E501

        Rule determining whether a user's last name should be permitted in their password  # noqa: E501

        :return: The exclude_last_name of this UpdatePasswordPolicyRequestComplexity.  # noqa: E501
        :rtype: bool
        """
        return self._exclude_last_name

    @exclude_last_name.setter
    def exclude_last_name(self, exclude_last_name):
        """Sets the exclude_last_name of this UpdatePasswordPolicyRequestComplexity.

        Rule determining whether a user's last name should be permitted in their password  # noqa: E501

        :param exclude_last_name: The exclude_last_name of this UpdatePasswordPolicyRequestComplexity.  # noqa: E501
        :type exclude_last_name: bool
        """
        if self.local_vars_configuration.client_side_validation and exclude_last_name is None:  # noqa: E501
            raise ValueError("Invalid value for `exclude_last_name`, must not be `None`")  # noqa: E501

        self._exclude_last_name = exclude_last_name

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, UpdatePasswordPolicyRequestComplexity):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpdatePasswordPolicyRequestComplexity):
            return True

        return self.to_dict() != other.to_dict()
