# utils/validators.py
import json
from pydantic import validator
from ipaddress import ip_address
import re

def json_validator(*fields):
    def wrapper(cls, value):
        if value is not None:
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                raise ValueError(f"Invalid format. Expected a JSON string.")
        return value
    return validator(*fields, pre=True, allow_reuse=True)(wrapper)


def split_str_validator(*fields, separator=','):
    def wrapper(cls, value):
        if value is not None and isinstance(value, str):
            return [item.strip() for item in value.split(separator)]
        return value
    return validator(*fields, pre=True, allow_reuse=True)(wrapper)

def ip_address_validator(*fields):
    def wrapper(cls, v):
        if v is not None:
            try:
                # This will validate both IPv4 and IPv6 addresses
                ip_address(v)
            except ValueError:
                raise ValueError("Invalid IP address")
        return v
    return validator(*fields, allow_reuse=True)(wrapper)

def mac_address_validator(field):
    def wrapper(cls, v):
        if v is not None and not re.match("[0-9a-f]{2}(?::[0-9a-f]{2}){5}$", v.lower()):
            raise ValueError(f"Invalid MAC address for field {field}")
        return v
    return validator(field, allow_reuse=True)(wrapper)

# This is a temporary validator until we figure out how to handle the sensor_source_info column in the database
def json_or_int_validator(*fields):
    def wrapper(cls, value):
        if value is not None:
            # If it's a string, assume it's a JSON string and try to parse it
            if isinstance(value, str):
                try:
                    # Attempt to parse the string as JSON
                    return json.loads(value)
                except json.JSONDecodeError:
                    raise ValueError(f"Invalid JSON format for string input.")
            elif not isinstance(value, (int, dict, list, float, bool, type(None))):
                # If it's not a string, int, dict, list, float, bool, or None, it's invalid
                raise ValueError(f"Invalid type. Value must be an integer, a JSON string, or a JSON-compatible type.")
        return value

    return validator(*fields, pre=True, allow_reuse=True)(wrapper)
