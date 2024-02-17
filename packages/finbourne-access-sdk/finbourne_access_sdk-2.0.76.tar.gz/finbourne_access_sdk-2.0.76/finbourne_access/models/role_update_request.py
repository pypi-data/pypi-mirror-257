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


from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, constr
from finbourne_access.models.role_resource_request import RoleResourceRequest
from finbourne_access.models.when_spec import WhenSpec

class RoleUpdateRequest(BaseModel):
    """
    Role update does not allow the changing of the id  # noqa: E501
    """
    description: Optional[constr(strict=True, max_length=1024, min_length=0)] = Field(None, description="The description of the role")
    resource: RoleResourceRequest = Field(...)
    when: WhenSpec = Field(...)
    __properties = ["description", "resource", "when"]

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
    def from_json(cls, json_str: str) -> RoleUpdateRequest:
        """Create an instance of RoleUpdateRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of resource
        if self.resource:
            _dict['resource'] = self.resource.to_dict()
        # override the default output from pydantic by calling `to_dict()` of when
        if self.when:
            _dict['when'] = self.when.to_dict()
        # set to None if description (nullable) is None
        # and __fields_set__ contains the field
        if self.description is None and "description" in self.__fields_set__:
            _dict['description'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RoleUpdateRequest:
        """Create an instance of RoleUpdateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RoleUpdateRequest.parse_obj(obj)

        _obj = RoleUpdateRequest.parse_obj({
            "description": obj.get("description"),
            "resource": RoleResourceRequest.from_dict(obj.get("resource")) if obj.get("resource") is not None else None,
            "when": WhenSpec.from_dict(obj.get("when")) if obj.get("when") is not None else None
        })
        return _obj
