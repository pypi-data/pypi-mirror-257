import logging
import typing

import pydantic
from google.protobuf.struct_pb2 import Struct

from int_connector_lib.proto.source_pb2 import DataSource

T = typing.TypeVar("T", bound=pydantic.BaseModel)
logger = logging.getLogger(__name__)


def nested_struct_to_nested_dict(struct: Struct) -> dict:
    """Convert a Struct into a dict, handling nested Struct data."""
    ret = {}
    for k, v in struct.items():
        if isinstance(v, Struct):
            v = nested_struct_to_nested_dict(v)  # noqa: PLW2901
        ret[k] = v
    return ret


class RunConfig(pydantic.BaseModel):
    """Base config model to handle grpc config structs."""

    @classmethod
    def from_struct(cls: type[T], struct: Struct) -> T:
        """Convert google protobuf.Struct to a config object."""
        data = nested_struct_to_nested_dict(struct)
        return cls(**data)


class SourceConfig(pydantic.BaseModel):
    """Base class for Source configs."""

    id: str
    name: str
    config: dict

    @classmethod
    def from_source(cls: type[T], source: DataSource) -> T:
        """Convert google protobuf.Struct to a config object."""
        config = nested_struct_to_nested_dict(source.config)
        return cls(id=source.id, name=source.name, config=config)
