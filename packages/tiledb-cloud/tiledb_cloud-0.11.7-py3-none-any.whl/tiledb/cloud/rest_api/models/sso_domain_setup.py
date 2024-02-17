# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from tiledb.cloud.rest_api.configuration import Configuration


class SSODomainSetup(object):
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
    """
    openapi_types = {"txt": "str", "cname_src": "str", "cname_dst": "str"}

    attribute_map = {"txt": "txt", "cname_src": "cname_src", "cname_dst": "cname_dst"}

    def __init__(
        self, txt=None, cname_src=None, cname_dst=None, local_vars_configuration=None
    ):  # noqa: E501
        """SSODomainSetup - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._txt = None
        self._cname_src = None
        self._cname_dst = None
        self.discriminator = None

        if txt is not None:
            self.txt = txt
        if cname_src is not None:
            self.cname_src = cname_src
        if cname_dst is not None:
            self.cname_dst = cname_dst

    @property
    def txt(self):
        """Gets the txt of this SSODomainSetup.  # noqa: E501

        a DNS TXT record to set on the domain to claim.  # noqa: E501

        :return: The txt of this SSODomainSetup.  # noqa: E501
        :rtype: str
        """
        return self._txt

    @txt.setter
    def txt(self, txt):
        """Sets the txt of this SSODomainSetup.

        a DNS TXT record to set on the domain to claim.  # noqa: E501

        :param txt: The txt of this SSODomainSetup.  # noqa: E501
        :type: str
        """

        self._txt = txt

    @property
    def cname_src(self):
        """Gets the cname_src of this SSODomainSetup.  # noqa: E501

        a DNS name to set a CNAME record on  # noqa: E501

        :return: The cname_src of this SSODomainSetup.  # noqa: E501
        :rtype: str
        """
        return self._cname_src

    @cname_src.setter
    def cname_src(self, cname_src):
        """Sets the cname_src of this SSODomainSetup.

        a DNS name to set a CNAME record on  # noqa: E501

        :param cname_src: The cname_src of this SSODomainSetup.  # noqa: E501
        :type: str
        """

        self._cname_src = cname_src

    @property
    def cname_dst(self):
        """Gets the cname_dst of this SSODomainSetup.  # noqa: E501

        the CNAME target of `cname_src`.  # noqa: E501

        :return: The cname_dst of this SSODomainSetup.  # noqa: E501
        :rtype: str
        """
        return self._cname_dst

    @cname_dst.setter
    def cname_dst(self, cname_dst):
        """Sets the cname_dst of this SSODomainSetup.

        the CNAME target of `cname_src`.  # noqa: E501

        :param cname_dst: The cname_dst of this SSODomainSetup.  # noqa: E501
        :type: str
        """

        self._cname_dst = cname_dst

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SSODomainSetup):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SSODomainSetup):
            return True

        return self.to_dict() != other.to_dict()
