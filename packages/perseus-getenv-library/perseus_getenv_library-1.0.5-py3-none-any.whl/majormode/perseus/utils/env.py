# Copyright (C) 2021 Majormode.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
from datetime import date
from datetime import datetime
from os import PathLike
from uuid import UUID

from majormode.perseus.model import obj
from majormode.perseus.model.enum import Enum
from majormode.perseus.model.locale import Locale
from majormode.perseus.model.obj import Object
from majormode.perseus.model.version import Version
from majormode.perseus.model.date import ISO8601DateTime

from majormode.perseus.utils import cast
from majormode.perseus.utils import string_util
import dotenv


# List of supported data types.
DataType = Enum(
    'boolean',
    'date',
    'decimal',
    'dictionary',
    'email_address',
    'enumeration',
    'hexadecimal',
    'integer',
    'ipv4',
    'list',
    'locale',
    'macaddr',
    'object',
    'regex',
    'string',
    'time',
    'timestamp',
    'uri',
    'uuid',
    'version'
)


def __convert_to_boolean(value: str) -> bool:
    return cast.string_to_boolean(value, strict=True)


def __convert_to_date(value: str) -> date:
    return cast.string_to_date(value)


def __convert_to_decimal(value: str) -> float:
    return float(value)


def __convert_to_email_address(value) -> str:
    if not string_util.is_email_address(value):
        raise ValueError(f'Invalid email address "{value}"')
    return value.lowercase()


def __convert_to_enumeration(value: str, enumeration: Enum) -> Enum:
    if enumeration is None:
        raise ValueError(f"The argument 'enumeration' is required")
    return cast.string_to_enum(value, enumeration)


def __convert_to_integer(value: str) -> int:
    return cast.string_to_integer(value, strict=False)


def __convert_to_ipv4(value: str) -> list[int]:
    return cast.string_to_ipv4(value, strict=False)


def __convert_to_list(
        value: any,
        item_data_type: DataType = DataType.string,
        **kwargs) -> list[any]:
    return [
        __cast_value(item, data_type=item_data_type, **kwargs)
        for item in value.split(',')
        if item
    ]


def __convert_to_locale(value: str) -> Locale:
    return cast.string_to_locale(value, strict=False)


def __convert_to_macaddr(value: str) -> tuple[str]:
    return cast.string_to_macaddr(value)


def __convert_to_object(value: any, object_class: any = None) -> Object or list:
    return (object_class or obj.Object).from_json(value)


def __convert_to_string(value: any) -> str:
    return str(value)


def __convert_to_time(value: str) -> datetime:
    return cast.string_to_time(value)


def __convert_to_timestamp(value: str) -> ISO8601DateTime:
    return cast.string_to_timestamp(value)


def __convert_to_uuid(value: str) -> UUID:
    return cast.string_to_uuid(value)


def __convert_to_version(value: str) -> Version:
    return Version(value)


DATA_TYPE_CONVERTERS = {
    DataType.boolean: __convert_to_boolean,
    DataType.date: __convert_to_date,
    DataType.decimal: __convert_to_decimal,
    DataType.email_address: __convert_to_email_address,
    DataType.enumeration: __convert_to_enumeration,
    DataType.integer: __convert_to_integer,
    DataType.ipv4: __convert_to_ipv4,
    DataType.list: __convert_to_list,
    DataType.locale: __convert_to_locale,
    DataType.macaddr: __convert_to_macaddr,
    DataType.object: __convert_to_object,
    DataType.string: __convert_to_string,
    DataType.time: __convert_to_time,
    DataType.timestamp: __convert_to_timestamp,
    DataType.uuid: __convert_to_uuid,
    DataType.version: __convert_to_version,
}


def __cast_value(
        value,
        data_type=DataType.string,
        **kwargs):
    """
    Convert a value, more likely a string, to the specified data type


    :param value: The string to be converted to the specified data type.

    :param data_type: An item of `DataType` that indicates the data type
        to cast the value to.

    :param enumeration: A Python class inheriting from `Enum`.  The value
        passed to this function MUST be an item or a string representation
        of an item of this enumeration.

    :param item_data_type: An item of `DataType` that specifies the desired
        data type of every item of the value (a list).  The argument
        `data_type` MUST be `DataType.list`.

    :param object_class: A Python class used to instantiate a new object
        from the value (a JSON string representation). The argument
        `data_type` MUST be `object`.  This Python class MUST implement a
        static method `from_json` that returns an instance of this class
        providing a JSON expression.

        If this argument `object_class` is not defined, while the argument
        `data_type` is `object`, the function uses the class `Object` to
        instantiate a new object from the JSON string representation.


    :return: The value converted to the desired data type.


    :raise ValueError: If the argument ``data_type`` is 
        ``DataType.enumeration`` but the argument ``enumeration`` has not
        been passed to this function.

    :raise TypeError: If the argument `value` is not a valid string
        representation of the desired data type.
    """
    if data_type not in DataType:
        raise ValueError("The argument 'data_type' MUST be an item of the enumeration 'DataType'")

    converter = DATA_TYPE_CONVERTERS.get(data_type)
    if converter is None:
        raise NotImplementedError(f"No converter for data type '{data_type}")

    value = converter(value, **kwargs)

    return value


def getenv(
        name,
        data_type=DataType.string,
        default_value=None,
        is_required=True,
        **kwargs):
    """
    Return the value of an environment variable.


    :param name: Name of an environment variable.

    :param data_type: An item of `DataType` that indicates the data type
        to cast the value to.

    :param default_value: Default value to return when the environment
        variable doesn't exist.

    :param is_required: Indicate whether the environment variable MUST
        exist.  If the environment variable doesn't exist, while the
        argument `is_required` is `True` and the argument `default_value`
        is not passed, the function raises an exception.

    :param enumeration: A Python class inheriting from `Enum`.  The value
        passed to this function MUST be an item or a string representation
        of an item of this enumeration.

    :param item_data_type: An item of `DataType` that specifies the desired
        data type of every item of the value (a list).  The argument
        `data_type` MUST be `DataType.list`.

    :param object_class: A Python class used to instantiate a new object
        from the value (a JSON string representation). The argument
        `data_type` MUST be `object`.  This Python class MUST implement a
        static method `from_json` that returns an instance of this class
        providing a JSON expression.

        If this argument `object_class` is not defined, while the argument
        `data_type` is `object`, the function uses the class `Object` to
        instantiate a new object from the JSON string representation.


    :return: The value of the environment variable converted to the
        desired data type.


    :raise Error: If the environment variable doesn't exist.
    """
    value = os.getenv(name)

    if value:
        value = __cast_value(value, data_type=data_type, **kwargs)
    elif default_value is not None:
        value = __cast_value(default_value, data_type=data_type, **kwargs)
    elif is_required:
        raise Exception(f'The environment variable "{name}" is not defined')

    return value


def loadenv(env_path_file_name: str or PathLike) -> bool:
    """
    Load environment variables from the local file `.env`.


    :param env_path_file_name: Absolute or relative path to .env file.
    """
    return dotenv.load_dotenv(env_path_file_name or '.env')


def setenv(name: str, value: any) -> None:
    """
    Set an environment variable.


    :param name: The name of the environment variable to set.

    :param value: The value of the environment variable.
    """
    os.environ[name] = str(value)
