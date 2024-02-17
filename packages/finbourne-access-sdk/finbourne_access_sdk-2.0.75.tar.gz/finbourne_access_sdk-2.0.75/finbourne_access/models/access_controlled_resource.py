# coding: utf-8

"""
    FINBOURNE Access Management API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist, constr
from finbourne_access.models.access_controlled_action import AccessControlledAction
from finbourne_access.models.identifier_part_schema import IdentifierPartSchema
from finbourne_access.models.link import Link

class AccessControlledResource(BaseModel):
    """
    AccessControlledResource
    """
    application: Optional[StrictStr] = None
    name: Optional[StrictStr] = None
    description: constr(strict=True, min_length=1) = Field(...)
    actions: conlist(AccessControlledAction) = Field(...)
    identifier_parts: Optional[conlist(IdentifierPartSchema)] = Field(None, alias="identifierParts")
    links: Optional[conlist(Link)] = None
    __properties = ["application", "name", "description", "actions", "identifierParts", "links"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AccessControlledResource:
        """Create an instance of AccessControlledResource from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in actions (list)
        _items = []
        if self.actions:
            for _item in self.actions:
                if _item:
                    _items.append(_item.to_dict())
            _dict['actions'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in identifier_parts (list)
        _items = []
        if self.identifier_parts:
            for _item in self.identifier_parts:
                if _item:
                    _items.append(_item.to_dict())
            _dict['identifierParts'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in links (list)
        _items = []
        if self.links:
            for _item in self.links:
                if _item:
                    _items.append(_item.to_dict())
            _dict['links'] = _items
        # set to None if application (nullable) is None
        # and __fields_set__ contains the field
        if self.application is None and "application" in self.__fields_set__:
            _dict['application'] = None

        # set to None if name (nullable) is None
        # and __fields_set__ contains the field
        if self.name is None and "name" in self.__fields_set__:
            _dict['name'] = None

        # set to None if identifier_parts (nullable) is None
        # and __fields_set__ contains the field
        if self.identifier_parts is None and "identifier_parts" in self.__fields_set__:
            _dict['identifierParts'] = None

        # set to None if links (nullable) is None
        # and __fields_set__ contains the field
        if self.links is None and "links" in self.__fields_set__:
            _dict['links'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AccessControlledResource:
        """Create an instance of AccessControlledResource from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AccessControlledResource.parse_obj(obj)

        _obj = AccessControlledResource.parse_obj({
            "application": obj.get("application"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "actions": [AccessControlledAction.from_dict(_item) for _item in obj.get("actions")] if obj.get("actions") is not None else None,
            "identifier_parts": [IdentifierPartSchema.from_dict(_item) for _item in obj.get("identifierParts")] if obj.get("identifierParts") is not None else None,
            "links": [Link.from_dict(_item) for _item in obj.get("links")] if obj.get("links") is not None else None
        })
        return _obj
