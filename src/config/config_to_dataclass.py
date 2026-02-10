import configparser
import dataclasses
from typing import get_args, get_origin, Literal


def config_to_dataclass[T](config_path: str, overrides: list[str], dataclass_type: type[T]) -> T:
    """Read a .cfg file and optional CLI overrides into a dataclass instance."""
    parser = configparser.ConfigParser()
    parser.read(config_path)
    section = "config"

    override_dict: dict[str, str] = {}
    for item in overrides:
        key, value = item.split("=", 1)
        override_dict[key.strip()] = value.strip()

    kwargs: dict = {}
    for field in dataclasses.fields(dataclass_type):
        # CLI overrides take precedence
        if field.name in override_dict:
            raw = override_dict[field.name]
        elif parser.has_option(section, field.name):
            raw = None  # will use typed getter below
        else:
            continue  # use dataclass default

        field_type = field.type

        # Handle Literal types
        origin = get_origin(field_type)
        if origin is Literal:
            value = override_dict[field.name] if raw is not None else parser.get(section, field.name)
            allowed = get_args(field_type)
            if value not in allowed:
                raise ValueError(f"Invalid value '{value}' for {field.name}. Allowed: {allowed}")
            kwargs[field.name] = value
        elif field_type is bool or field_type == "bool":
            if raw is not None:
                kwargs[field.name] = raw.lower() in ("true", "yes", "1")
            else:
                kwargs[field.name] = parser.getboolean(section, field.name)
        elif field_type is int or field_type == "int":
            if raw is not None:
                kwargs[field.name] = int(raw)
            else:
                kwargs[field.name] = parser.getint(section, field.name)
        elif field_type is float or field_type == "float":
            if raw is not None:
                kwargs[field.name] = float(raw)
            else:
                kwargs[field.name] = parser.getfloat(section, field.name)
        else:
            if raw is not None:
                kwargs[field.name] = raw
            else:
                kwargs[field.name] = parser.get(section, field.name)

    return dataclass_type(**kwargs)
