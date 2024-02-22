import typing
from enum import Enum

import grpc

from int_connector_lib.proto import (
    manager_pb2,
    manager_pb2_grpc,
)
from int_connector_lib.protobuf import Empty


class DataFormat(Enum):  # noqa: D101
    FORMAT_UNKNOWN = manager_pb2.Format.FORMAT_UNKNOWN
    FORMAT_STRING = manager_pb2.Format.FORMAT_STRING
    FORMAT_JSON = manager_pb2.Format.FORMAT_JSON
    FORMAT_PARQUET = manager_pb2.Format.FORMAT_PARQUET


class Manager:
    """Wrapper for ManagerStub."""

    def __init__(self: typing.Self, channel: grpc.Channel) -> None:
        self.mgr = manager_pb2_grpc.ManagerStub(channel)

    def send_data(self: typing.Self, source_id: str, data_format: DataFormat, data: bytes) -> Empty:
        """Send data to manager."""
        self.mgr.SendData(
            manager_pb2.SendDataRequest(
                id=source_id,
                format=data_format.value,
                data=data,
            ),
        )

    def send_file(self: typing.Self, source_id: str, data_format: DataFormat, path: str) -> Empty:
        """Send data to manager."""
        self.mgr.SendFile(
            manager_pb2.SendFileRequest(
                id=source_id,
                format=data_format.value,
                path=path,
            ),
        )
