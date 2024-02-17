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
from finbourne_access.models.action_id import ActionId

class PolicySelectorDefinition(BaseModel):
    """
    PolicySelectorDefinition
    """
    identity_restriction: Optional[Dict[str, StrictStr]] = Field(None, alias="identityRestriction")
    restriction_selectors: Optional[conlist(SelectorDefinition)] = Field(None, alias="restrictionSelectors")
    actions: conlist(ActionId, min_items=1) = Field(...)
    name: Optional[constr(strict=True, max_length=100, min_length=0)] = None
    description: Optional[constr(strict=True, max_length=1024, min_length=0)] = None
    __properties = ["identityRestriction", "restrictionSelectors", "actions", "name", "description"]

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
    def from_json(cls, json_str: str) -> PolicySelectorDefinition:
        """Create an instance of PolicySelectorDefinition from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in restriction_selectors (list)
        _items = []
        if self.restriction_selectors:
            for _item in self.restriction_selectors:
                if _item:
                    _items.append(_item.to_dict())
            _dict['restrictionSelectors'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in actions (list)
        _items = []
        if self.actions:
            for _item in self.actions:
                if _item:
                    _items.append(_item.to_dict())
            _dict['actions'] = _items
        # set to None if identity_restriction (nullable) is None
        # and __fields_set__ contains the field
        if self.identity_restriction is None and "identity_restriction" in self.__fields_set__:
            _dict['identityRestriction'] = None

        # set to None if restriction_selectors (nullable) is None
        # and __fields_set__ contains the field
        if self.restriction_selectors is None and "restriction_selectors" in self.__fields_set__:
            _dict['restrictionSelectors'] = None

        # set to None if name (nullable) is None
        # and __fields_set__ contains the field
        if self.name is None and "name" in self.__fields_set__:
            _dict['name'] = None

        # set to None if description (nullable) is None
        # and __fields_set__ contains the field
        if self.description is None and "description" in self.__fields_set__:
            _dict['description'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PolicySelectorDefinition:
        """Create an instance of PolicySelectorDefinition from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PolicySelectorDefinition.parse_obj(obj)

        _obj = PolicySelectorDefinition.parse_obj({
            "identity_restriction": obj.get("identityRestriction"),
            "restriction_selectors": [SelectorDefinition.from_dict(_item) for _item in obj.get("restrictionSelectors")] if obj.get("restrictionSelectors") is not None else None,
            "actions": [ActionId.from_dict(_item) for _item in obj.get("actions")] if obj.get("actions") is not None else None,
            "name": obj.get("name"),
            "description": obj.get("description")
        })
        return _obj
