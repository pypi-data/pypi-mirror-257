import typing
from concurrent import futures

import grpc
from grpc_health.v1 import health_pb2_grpc

from int_connector_lib.broker import Broker
from int_connector_lib.health import HealthServicer
from int_connector_lib.proto import (
    grpc_broker_pb2_grpc,
    source_pb2_grpc,
)
from int_connector_lib.source import BaseSource, Source, StreamingSource


class Server:
    """Wrapper for grpc.Server functionality."""

    def __init__(self: typing.Self, max_workers: int) -> None:
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    def add_base_source_servicer(self: typing.Self, base_source: BaseSource) -> None:
        """Register a BaseSourceServicer against the server."""
        source_pb2_grpc.add_BaseSourceServicer_to_server(base_source, self._server)

    def add_source_servicer(self: typing.Self, source: Source) -> None:
        """Register a SourceServicer against the server."""
        source_pb2_grpc.add_SourceServicer_to_server(source, self._server)

    def add_streaming_source_servicer(self: typing.Self, source: StreamingSource) -> None:
        """Register a SourceServicer against the server."""
        source_pb2_grpc.add_StreamingSourceServicer_to_server(source, self._server)

    def add_broker_servicer(self: typing.Self, broker: Broker) -> None:
        """Register a GRPCBrokerServicer against the server."""
        grpc_broker_pb2_grpc.add_GRPCBrokerServicer_to_server(broker, self._server)

    def add_health_servicer(self: typing.Self, health: HealthServicer) -> None:
        """Register a HealthServicer against the server."""
        health_pb2_grpc.add_HealthServicer_to_server(health, self._server)

    def __getattr__(self, attr: str):  # noqa: ANN101, ANN204
        """Expose internal server methods."""
        return getattr(self._server, attr)
