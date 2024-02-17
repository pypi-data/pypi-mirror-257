# coding: utf-8

"""
    FINBOURNE Identity Service API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from typing import Any, Dict
from pydantic import BaseModel, Field, constr

class SupportAccessExpiryWithRole(BaseModel):
    """
    Time at which the support access granted for a role expires  # noqa: E501
    """
    expiry: datetime = Field(..., description="DateTimeOffset at which the access will be revoked")
    permitted_role: constr(strict=True, min_length=1) = Field(..., alias="permittedRole", description="Unique identifier for permitted role.   Use GET /identity/api/authentication/support-roles to lookup role label/code from identifier.")
    __properties = ["expiry", "permittedRole"]

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
    def from_json(cls, json_str: str) -> SupportAccessExpiryWithRole:
        """Create an instance of SupportAccessExpiryWithRole from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SupportAccessExpiryWithRole:
        """Create an instance of SupportAccessExpiryWithRole from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SupportAccessExpiryWithRole.parse_obj(obj)

        _obj = SupportAccessExpiryWithRole.parse_obj({
            "expiry": obj.get("expiry"),
            "permitted_role": obj.get("permittedRole")
        })
        return _obj
