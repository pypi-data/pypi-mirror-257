# -*- coding: utf-8 -*-
# Copyright (C) 2023 Pillar ML <https://www.pillar.ml>. All rights reserved.
#
# This file is a part of saphiera.
# https://github.com/Pillar-ML/saphiera
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


"""Fields used for schema validation. Built on top of strictyaml validators."""

from typing import Any, Optional

from strictyaml import YAML

from saphiera.exceptions import InvalidSchemaDefinition
from saphiera.schema import validators
from saphiera.schema.validators import Validator
from saphiera.types import Enum


class Field(Validator):
    """
    A wrapper around strictyaml validators.

    Represents a yaml attribute, storing the title and data type. Also allows
    for defining defaults and optional.

    For example, the yaml attribute `foo: [1, 2]` has the following values:
        title = "foo"
        type = list
        val = [1, 2]
    """

    validator: Validator = validators.Any()

    def __init__(
        self,
        title: str,
        optional: bool = False,
        default: Optional[Any] = None,
        description: Optional[str] = None,
    ) -> None:
        """Initialize field object.

        :param title: The name of the yaml key
        :param optional: Whether the key is required in the final schema. Defaults to False.
        :param default: Default value to use in case it isn't defined in the yaml.
        :param description: Optional description to define the field.
        """
        super().__init__()
        self.title = title
        self.optional = optional
        self.description = description
        self.default = default

    @property
    def schema(self) -> dict:
        if self.optional or self.default is not None:
            return {validators.Optional(self.title, self.default): self.validator}
        else:
            return {self.title: self.validator}

    def __call__(self, chunk: str) -> YAML:
        return self.validator(chunk)

    def __or__(self, other: Any) -> "Field":
        if isinstance(other, Field):
            self.validator = self.validator | other.validator
        elif isinstance(other, Validator):
            self.validator = self.validator | other
        else:
            raise InvalidSchemaDefinition(
                f"Trying to create an invalid union between {self.__class__} and {other.__class__}. "
                f"Expected other to be in {[Field, Validator]}"
            )

        return self

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.title})"


class DictField(Field):
    """
    Represents a yaml attribute with a dictionary data type.

    Generates a schema for all subfields.
    """

    def __init__(
        self,
        title: str,
        fields: list[Field],
        strict: bool = True,
        optional: bool = False,
        description: Optional[str] = None,
    ) -> None:
        """Initialize Dictionary Field for defining multiple schema fields

        :param title: Name of the yaml key
        :param fields: List of subfields that are contained within the dictionary
        :param strict: Raise an error if a non-defined field is defined. Defaults to True.
        :param optional: Whether the field is required in the final schema.
        :param description: Optional description defining the field.
        """
        super().__init__(
            title=title, optional=optional, default=None, description=description
        )

        self.strict = strict
        self.fields = fields

        if strict:
            self.validator = validators.Map(self._build_mapping(fields))
        else:
            self.validator = validators.MapCombined(
                self._build_mapping(fields),
                key_validator=validators.Str(),
                value_validator=validators.Any(),
            )

    @staticmethod
    def _build_mapping(fields: list[Field]) -> dict:
        mapping = {}

        for field in fields:
            for key, value in field.schema.items():
                mapping[key] = value

        return mapping


class ListField(Field):
    """
    Represents a yaml attribute with a list data type.

    Allows for defining the list item field type.
    """

    def __init__(
        self,
        title: str,
        field: Field,
        unique: bool = False,
        optional: bool = False,
        default: Optional[Any] = None,
        description: Optional[str] = None,
    ) -> None:
        """Initialize List Field for containing a list of field types.

        :param title: Name of the yaml key
        :param field: Field type to validate the list against
        :param unique: Raises an error on duplicate values if true. Defaults to False.
        :param optional: Whether the field is optional in the final schema. Defaults to False.
        :param default: Default value for the field. Defaults to None.
        :param description: Optional description defining the field.
        """
        super().__init__(
            title=title, optional=optional, default=default, description=description
        )

        self.field = field
        self.unique = unique

        if unique:
            self.validator = validators.UniqueSeq(field.validator)
        else:
            self.validator = validators.Seq(field.validator)


class EnumField(Field):
    """Restricts field to values provided in the enum."""

    def __init__(
        self,
        title: str,
        enum: Enum | list | tuple,
        item_validator: validators.ScalarValidator | None = None,
        optional: bool = False,
        default: Optional[Any] = None,
        description: Optional[str] = None,
    ) -> None:
        """Initialize an enum validator restricted to the provided enum, and
        optionally the provided validator.

        :param title: Name of the yaml key
        :param enum: Values to restrict the field to.
        :param item_validator: Validator to apply to the field values. Defaults to Str.
        :param optional: Whether the field is optional in the final schema. Defaults to False.
        :param default: Default value for the field. Defaults to None.
        :param description: Optional description defining the field.
        """
        super().__init__(
            title=title, optional=optional, default=default, description=description
        )
        self.enum = enum
        self.item_validator = (
            item_validator if item_validator is not None else validators.Str()
        )

        self.validator = validators.Enum(
            restricted_to=self.enum, item_validator=self.item_validator
        )


class IntField(Field):
    """Represents the yaml attribute with the integer data type."""

    validator = validators.Int()


class HexIntField(IntField):
    """Represents the yaml attribute with a hex int defined."""

    validator = validators.HexInt()


class StrField(Field):
    """Represents the yaml attribute with the string data type."""

    validator = validators.Str()


class DecimalField(Field):
    """Represents the yaml attribute with the decimal data type."""

    validator = validators.Decimal()


class FloatField(Field):
    """Represents the yaml attribute with the float data type."""

    validator = validators.Float()


class BoolField(Field):
    """Represents the yaml attribute with the bool data type."""

    validator = validators.Bool()


class ItemField(Field):
    """Represents the yaml attribute with a python builtin data type."""

    validator = (
        (IntField.validator | FloatField.validator) | BoolField.validator
    ) | StrField.validator


class NumberField(Field):
    """Represents the yaml attribute with either an integer or float data type."""

    validator = IntField.validator | FloatField.validator


class DateTimeField(Field):
    """Represents the yaml attribute to be parsed with dateutil."""

    validator = validators.Datetime()


class RegexField(StrField):
    """Validates field matches supplied regex."""

    def __init__(
        self,
        title: str,
        regex: str,
        optional: bool = False,
        description: Optional[str] = None,
    ) -> None:
        super().__init__(
            title=title, optional=optional, default=None, description=description
        )

        self.regex = regex
        self.validator = validators.Regex(regex)


class EmailField(StrField):
    """Validates field matches email regex."""

    validator = validators.Email()


class UrlField(StrField):
    """Validates field is valid URL."""

    validator = validators.Url()
