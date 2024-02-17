from __future__ import annotations

import logging
import os
import re
import sys
from configparser import _UNSET, ConfigParser, NoOptionError
from pathlib import Path
from typing import TypeVar

from .text import skip_utf8_bom
from .types import convert

logger = logging.getLogger(__name__)

T = TypeVar('T')


def get_env_config(name: str, fallback: str = _UNSET, type: type[T] = str) -> T:
    """
    Get a configuration value from environment variables.
    """
    if name in os.environ:
        value = os.environ[name]

    else:
        if fallback is _UNSET:
            raise ConfigurationError(name, "environment variable")
        value = fallback
    
    if type != str:
        return convert(value, type)
    else:
        return value


def get_secret_config(name: str, fallback: str = _UNSET, type: type[T] = str):
    """
    Get a configuration value from secret files.
    """
    name = name.lower()

    value = None

    # For local and/or development environment
    if os.path.exists(f"secrets/{name}.txt"):
        value = _read_file_and_rstrip_newline(f"secrets/{name}.txt")

    if value is None and os.path.exists(f"secrets/misc.ini"): 
        value = _get_from_misc_env_file(f"secrets/misc.ini", name)
    
    # For production environment
    # See: https://docs.docker.com/compose/use-secrets/
    # NOTE: using a single "misc" env file allow to avoid passing all secrets individually in docker compose files.
    if value is None and os.path.exists(f"/run/secrets/{name}"):
        value = _read_file_and_rstrip_newline(f"/run/secrets/{name}")
    
    if value is None and os.path.exists(f"/run/secrets/misc"):
        value = _get_from_misc_env_file(f"/run/secrets/misc", name)

    if value is None:
        if fallback is _UNSET:
            raise ConfigurationError(name, "secret")
        value = fallback
        
    if type != str:
        return convert(value, type)
    else:
        return value


class ConfigurationError(Exception):
    def __init__(self, name: str, nature: str = "option"):
        if nature:
            message = f"{nature.capitalize()} {name} not configured."
            self.name = name
            self.nature = nature
        else:
            message = name
            self.name = None
            self.nature = None

        super().__init__(message)


def get_config_parser(prog: str) -> ExtendedConfigParser:
    """
    A function to search for configuration files in some common paths.
    """
    if not prog:
        raise ValueError("prog required")
        # NOTE: we should not try to determine prog here: this is too dangerous (invalid/fake configuration files could be loaded by mistake)

    parser = ExtendedConfigParser()

    parser.read([
        # System configuration
        Path(f'C:/ProgramData/{prog}/{prog}.conf' if sys.platform == 'win32' else f'/etc/{prog}/{prog}.conf').expanduser(),
        Path(f'C:/ProgramData/{prog}.conf' if sys.platform == 'win32' else f'/etc/{prog}.conf').expanduser(),
        # User configuration
        Path(f'~/.config/{prog}/{prog}.conf').expanduser(),
        Path(f'~/.config/{prog}.conf').expanduser(),
        # Local configuration
        "local.conf",
    ], encoding='utf-8')

    return parser


class ExtendedConfigParser(ConfigParser):
    def getsecret(self, section: str, option: str, *, raw=False, vars=None, fallback: str = _UNSET) -> str:
        """
        If option not found, will also try to read the value from:
        - A file named `secrets/{section}_{option}.txt` if exists (usefull for local/development environment).
        - A file named `/run/secrets/{section}_{option}` if exists (usefull for Docker secrets - see https://docs.docker.com/compose/use-secrets/).
        - The file indicated by option `{option}_file` (usefull for password files).
        """
        result = self.get(section, option, raw=raw, vars=vars, fallback=None)

        if result is not None:
            return result

        secret_name = f'{section}_{option}'.replace(':', '-')

        # try local secret
        secret_path = f'secrets/{secret_name}.txt'
        if os.path.exists(secret_path):
            return _read_file_and_rstrip_newline(secret_path)

        # try Docker-like secret
        secret_path = f'/run/secrets/{secret_name}'
        if os.path.exists(secret_path):
            return _read_file_and_rstrip_newline(secret_path)

        # try file
        path = self.get(section, f'{option}_file', raw=raw, vars=vars, fallback=None)
        if path is not None:
            return _read_file_and_rstrip_newline(path)
        
        if fallback is _UNSET:
            raise NoOptionError(option, section)
        else:
            return fallback


    def getlist(self, section: str, option: str, *, raw=False, vars=None, delimiter=None, fallback: list[str] = _UNSET) -> list[str]:
        values_str = self.get(section, option, raw=raw, vars=vars, fallback=fallback)
        if not isinstance(values_str, str):
            return values_str # fallback
        
        if delimiter:
            if not values_str:
                return []
            
            values = []
            for value in values_str.split(delimiter):
                value = value.strip()
                if not value:
                    continue
                values.append(value)

            return values
        else:
            return convert(values_str, list)


def _read_file_and_rstrip_newline(path: os.PathLike):
    with open(path, 'r', encoding='utf-8') as fp:
        skip_utf8_bom(fp)
        value = fp.read()
        return value.rstrip('\r\n')


_misc_files_content: dict[Path,dict[str,str]] = {}

def _get_from_misc_env_file(path: os.PathLike, key: str):
    if not isinstance(path, Path):
        path = Path(path)

    if not path in _misc_files_content:
        _misc_files_content[path] = parse_env_file(path, lower_keys=True)
                
    return _misc_files_content[path].get(key)


_env_assignment_regex = re.compile(r'^([A-Z0-9_]+)\s*=(.+)*$', re.IGNORECASE)

def parse_env_file(path: os.PathLike, *, lower_keys = False):
    data: dict[str, str] = {}

    with open(path, 'r', encoding='utf-8') as fp:
        skip_utf8_bom(fp)
        line_num = 0
        while line := fp.readline():
            line_num += 1
            line = re.sub(r'^\s*', '', line)
            line = re.sub(r'\s$', '', line)
            if line == '':
                continue # ignore empty lintes
            elif line.startswith('#'):
                continue # ignore comments
            elif m := _env_assignment_regex.match(line):
                key = m[1]
                value = m[2].lstrip()
                if lower_keys:
                    key = key.lower()
                data[key] = value
            else:
                raise ConfigurationError(f"Cannot parse env file {path}. Offending line: {line_num}.", nature=None)
                # Do not display the offending line has it could reveal sensitive information.

    return data
