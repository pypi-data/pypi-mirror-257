"""
This module contains functions for creating serialized data in all supported formats.

Each function takes a Python dictionary, serializes the data, and writes it 
to a TextStream object. Optionally, a file can be created with the  contents
of that TextStream if the dumper function is provided with a file path, which
can be either a Path or a str object.

If your project uses file formats other than the ones supported here, you can
add support for them by having your own python dumpers.py module and creating an
environment variable `DUMPERS_MODULE` that points to its dotted path.

Contrary to the loaders module, there's no mechanism for automatically detecting
which dumper function to use. A caller must be explicit about the dumper function
for the desired serialization format.
"""

import configparser
import io
import json
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Union

import toml
import yaml

from pydantic_wrangler.exceptions import PydanticWranglerDumperError


def stream_dumper(dump_func: Callable[..., None]):
    def standard_dumper_func(
        data: Dict[Any, Any],
        file_path: Optional[Union[Path, str]] = None,
        *args,
        **kwargs
    ) -> io.StringIO:
        """Decorator to dump data to a stream and optionally to a file.

        Args:
            data (Dict[Any, Any]): The data to be written to the serialized stream.
            file_path (Optional[Union[Path, str]], optional): The path to the
            file where the serialized data will be written. If provided, the data
            will be written to the specified file. If not provided, the data
            will only be written to the stream. Defaults to None.

        Returns:
            io.StringIO: The stream containing the written serialized data.

        Raises:
            PydanticWranglerDumperError: If any exception occurs while dumping the data.
        """
        try:
            stream = io.StringIO()
            dump_func(data, stream, *args, **kwargs)

            if file_path is not None:
                with open(file_path, "w") as file:
                    file.write(stream.getvalue())

            stream.seek(0)
            return stream
        except Exception as e:
            raise PydanticWranglerDumperError(str(e))

    return standard_dumper_func


@stream_dumper
def json_dumper(
    data: Dict[Any, Any], stream: io.StringIO, *args, **kwargs
) -> io.StringIO:
    """Writes data to a JSON stream and optionally to a file."""
    json.dump(data, stream, *args, **kwargs)


@stream_dumper
def yaml_dumper(data: Dict[Any, Any], stream: io.StringIO) -> io.StringIO:
    """Writes data to a YAML stream and optionally to a file.."""
    yaml.dump(data, stream)


@stream_dumper
def ini_dumper(data: Dict[Any, Any], stream: io.StringIO) -> io.StringIO:
    """Writes data to an INI stream."""
    config = configparser.ConfigParser()
    config.read_dict(data)
    config.write(stream)


@stream_dumper
def toml_dumper(data: Dict[Any, Any], stream: io.StringIO) -> io.StringIO:
    """Writes data to a TOML stream."""
    toml.dump(data, stream)
