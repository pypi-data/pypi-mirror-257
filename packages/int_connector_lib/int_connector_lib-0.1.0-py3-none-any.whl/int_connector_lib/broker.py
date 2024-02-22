import logging
import time
import typing

import grpc

from int_connector_lib.proto import (
    grpc_broker_pb2,
    grpc_broker_pb2_grpc,
)

P = typing.ParamSpec("P")

TYPE = "dummy connector"
VERSION = "v0.0.1"


class Broker(grpc_broker_pb2_grpc.GRPCBroker):
    """Implement grpc Broker for bidirectional communication."""

    def __init__(self: typing.Self, logger: logging.Logger) -> None:
        self.logger = logger
        self._streams = {}

    @property
    def streams(self: typing.Self) -> dict:
        """Return internal stream store."""
        return self._streams

    def StartStream(
        self: typing.Self,
        request: grpc_broker_pb2.ConnInfo,  # RequestIterator
        context: grpc.ServicerContext,
    ) -> grpc_broker_pb2.ConnInfo:  # ResponseIterator
        """Handle rpc.StartStream call."""
        self.logger.debug("Start Stream")
        for r in request:
            self.logger.debug(r)
            self.streams[r.service_id] = r
            # TODO(edgy): Return accurate conn info, bidirectional seems to work regardess
            yield grpc_broker_pb2.ConnInfo()

    def Dial(self: typing.Self, service_id: int) -> grpc.Channel:
        """Implement Broker.Dial.

        Given a service_id, generate a grpc.Channel for the associated service.
        """
        while service_id not in self.streams:
            self.logger.debug("Waiting for stream %s.", service_id)
            time.sleep(0.1)
        self.logger.debug("Dialing %s", service_id)
        self.logger.debug(self.streams)
        conn_info = self.streams[service_id]
        self.logger.info("Dialing %s:%s", conn_info.network, conn_info.address)
        return grpc.insecure_channel(f"{conn_info.network}://{conn_info.address}")
