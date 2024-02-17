# coding: utf-8

"""
    FINBOURNE Access Management API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.0.3692
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

from finbourne_access.configuration import Configuration


class EffectiveDateHasQuality(object):
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
        'quality': 'DateQuality'
    }

    attribute_map = {
        'quality': 'quality'
    }

    required_map = {
        'quality': 'optional'
    }

    def __init__(self, quality=None, local_vars_configuration=None):  # noqa: E501
        """EffectiveDateHasQuality - a model defined in OpenAPI"
        
        :param quality: 
        :type quality: finbourne_access.DateQuality

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._quality = None
        self.discriminator = None

        if quality is not None:
            self.quality = quality

    @property
    def quality(self):
        """Gets the quality of this EffectiveDateHasQuality.  # noqa: E501


        :return: The quality of this EffectiveDateHasQuality.  # noqa: E501
        :rtype: finbourne_access.DateQuality
        """
        return self._quality

    @quality.setter
    def quality(self, quality):
        """Sets the quality of this EffectiveDateHasQuality.


        :param quality: The quality of this EffectiveDateHasQuality.  # noqa: E501
        :type quality: finbourne_access.DateQuality
        """

        self._quality = quality

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
        if not isinstance(other, EffectiveDateHasQuality):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, EffectiveDateHasQuality):
            return True

        return self.to_dict() != other.to_dict()
