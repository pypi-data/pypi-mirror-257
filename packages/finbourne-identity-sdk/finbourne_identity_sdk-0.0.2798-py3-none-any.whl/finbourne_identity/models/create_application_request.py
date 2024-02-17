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


class CreateApplicationRequest(object):
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
        'display_name': 'str',
        'client_id': 'str',
        'type': 'str',
        'redirect_uris': 'list[str]',
        'post_logout_redirect_uris': 'list[str]'
    }

    attribute_map = {
        'display_name': 'displayName',
        'client_id': 'clientId',
        'type': 'type',
        'redirect_uris': 'redirectUris',
        'post_logout_redirect_uris': 'postLogoutRedirectUris'
    }

    required_map = {
        'display_name': 'required',
        'client_id': 'required',
        'type': 'required',
        'redirect_uris': 'optional',
        'post_logout_redirect_uris': 'optional'
    }

    def __init__(self, display_name=None, client_id=None, type=None, redirect_uris=None, post_logout_redirect_uris=None, local_vars_configuration=None):  # noqa: E501
        """CreateApplicationRequest - a model defined in OpenAPI"
        
        :param display_name:  The Display Name of the application (required)
        :type display_name: str
        :param client_id:  The OpenID Connect ClientId of the application (required)
        :type client_id: str
        :param type:  The Type of the application. This must be either Native or Web (required)
        :type type: str
        :param redirect_uris:  A web application's acceptable list of post-login redirect URIs
        :type redirect_uris: list[str]
        :param post_logout_redirect_uris:  A web application's acceptable list of post-logout redirect URIs
        :type post_logout_redirect_uris: list[str]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._display_name = None
        self._client_id = None
        self._type = None
        self._redirect_uris = None
        self._post_logout_redirect_uris = None
        self.discriminator = None

        self.display_name = display_name
        self.client_id = client_id
        self.type = type
        self.redirect_uris = redirect_uris
        self.post_logout_redirect_uris = post_logout_redirect_uris

    @property
    def display_name(self):
        """Gets the display_name of this CreateApplicationRequest.  # noqa: E501

        The Display Name of the application  # noqa: E501

        :return: The display_name of this CreateApplicationRequest.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this CreateApplicationRequest.

        The Display Name of the application  # noqa: E501

        :param display_name: The display_name of this CreateApplicationRequest.  # noqa: E501
        :type display_name: str
        """
        if self.local_vars_configuration.client_side_validation and display_name is None:  # noqa: E501
            raise ValueError("Invalid value for `display_name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                display_name is not None and len(display_name) > 50):
            raise ValueError("Invalid value for `display_name`, length must be less than or equal to `50`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                display_name is not None and len(display_name) < 1):
            raise ValueError("Invalid value for `display_name`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                display_name is not None and not re.search(r'^[\s\S]*$', display_name)):  # noqa: E501
            raise ValueError(r"Invalid value for `display_name`, must be a follow pattern or equal to `/^[\s\S]*$/`")  # noqa: E501

        self._display_name = display_name

    @property
    def client_id(self):
        """Gets the client_id of this CreateApplicationRequest.  # noqa: E501

        The OpenID Connect ClientId of the application  # noqa: E501

        :return: The client_id of this CreateApplicationRequest.  # noqa: E501
        :rtype: str
        """
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        """Sets the client_id of this CreateApplicationRequest.

        The OpenID Connect ClientId of the application  # noqa: E501

        :param client_id: The client_id of this CreateApplicationRequest.  # noqa: E501
        :type client_id: str
        """
        if self.local_vars_configuration.client_side_validation and client_id is None:  # noqa: E501
            raise ValueError("Invalid value for `client_id`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                client_id is not None and len(client_id) > 50):
            raise ValueError("Invalid value for `client_id`, length must be less than or equal to `50`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                client_id is not None and len(client_id) < 6):
            raise ValueError("Invalid value for `client_id`, length must be greater than or equal to `6`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                client_id is not None and not re.search(r'^[a-zA-Z][a-zA-Z0-9-]{5,49}', client_id)):  # noqa: E501
            raise ValueError(r"Invalid value for `client_id`, must be a follow pattern or equal to `/^[a-zA-Z][a-zA-Z0-9-]{5,49}/`")  # noqa: E501

        self._client_id = client_id

    @property
    def type(self):
        """Gets the type of this CreateApplicationRequest.  # noqa: E501

        The Type of the application. This must be either Native or Web  # noqa: E501

        :return: The type of this CreateApplicationRequest.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this CreateApplicationRequest.

        The Type of the application. This must be either Native or Web  # noqa: E501

        :param type: The type of this CreateApplicationRequest.  # noqa: E501
        :type type: str
        """
        if self.local_vars_configuration.client_side_validation and type is None:  # noqa: E501
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                type is not None and len(type) > 20):
            raise ValueError("Invalid value for `type`, length must be less than or equal to `20`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                type is not None and len(type) < 1):
            raise ValueError("Invalid value for `type`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                type is not None and not re.search(r'^[a-zA-Z]*$', type)):  # noqa: E501
            raise ValueError(r"Invalid value for `type`, must be a follow pattern or equal to `/^[a-zA-Z]*$/`")  # noqa: E501

        self._type = type

    @property
    def redirect_uris(self):
        """Gets the redirect_uris of this CreateApplicationRequest.  # noqa: E501

        A web application's acceptable list of post-login redirect URIs  # noqa: E501

        :return: The redirect_uris of this CreateApplicationRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._redirect_uris

    @redirect_uris.setter
    def redirect_uris(self, redirect_uris):
        """Sets the redirect_uris of this CreateApplicationRequest.

        A web application's acceptable list of post-login redirect URIs  # noqa: E501

        :param redirect_uris: The redirect_uris of this CreateApplicationRequest.  # noqa: E501
        :type redirect_uris: list[str]
        """

        self._redirect_uris = redirect_uris

    @property
    def post_logout_redirect_uris(self):
        """Gets the post_logout_redirect_uris of this CreateApplicationRequest.  # noqa: E501

        A web application's acceptable list of post-logout redirect URIs  # noqa: E501

        :return: The post_logout_redirect_uris of this CreateApplicationRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._post_logout_redirect_uris

    @post_logout_redirect_uris.setter
    def post_logout_redirect_uris(self, post_logout_redirect_uris):
        """Sets the post_logout_redirect_uris of this CreateApplicationRequest.

        A web application's acceptable list of post-logout redirect URIs  # noqa: E501

        :param post_logout_redirect_uris: The post_logout_redirect_uris of this CreateApplicationRequest.  # noqa: E501
        :type post_logout_redirect_uris: list[str]
        """

        self._post_logout_redirect_uris = post_logout_redirect_uris

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
        if not isinstance(other, CreateApplicationRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateApplicationRequest):
            return True

        return self.to_dict() != other.to_dict()
