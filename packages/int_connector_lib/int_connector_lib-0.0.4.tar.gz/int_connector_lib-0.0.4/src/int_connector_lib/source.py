import logging
import typing
from collections import defaultdict

import grpc
import pydantic

from int_connector_lib import protobuf
from int_connector_lib.broker import Broker
from int_connector_lib.config import RunConfig, SourceConfig
from int_connector_lib.manager import Manager
from int_connector_lib.proto import (
    source_pb2,
    source_pb2_grpc,
)

P = typing.ParamSpec("P")


class BaseSource(source_pb2_grpc.BaseSourceServicer):
    """Implement grpc BaseSource for basic Source information."""

    def __init__(  # noqa: PLR0913
        self: typing.Self,
        logger: logging.Logger,
        run_config_class: type[RunConfig],
        source_config_class: type[SourceConfig] | None,
        source_type: str,
        source_version: str,
    ) -> None:
        self.logger = logger
        self.id = ""
        self.name = ""
        self.status = source_pb2.STATUS_UNKNOWN
        self.source_type = source_type
        self.source_version = source_version
        self._run_config_class = run_config_class
        self._source_config_class = source_config_class
        self.sources = {}

    def CheckConfig(
        self: typing.Self,
        request: source_pb2.ConfigMessage,
        context: grpc.ServicerContext,
    ) -> source_pb2.ValidationMessage:
        """Handle rpc.CheckConfig call."""
        self.logger.debug("CheckConfig called!")
        errors = defaultdict(list)
        for i, source in enumerate(request.SourcesConfig):
            self.logger.info(type(source))
            self.logger.info(source)
            try:
                self.sources[source.id] = self._source_config_class.from_source(source)
            except pydantic.ValidationError as e:
                for err in e.errors():
                    loc = ".".join(err["loc"])
                    errors[f"sources.{i}.{loc}"].append(err["msg"])

        for i, run in enumerate(request.RunsConfig):
            try:
                self._run_config_class.from_struct(run.source)
            except pydantic.ValidationError as e:
                for err in e.errors():
                    loc = ".".join(err["loc"])
                    errors[f"runs.{i}.config.{loc}"].append(err["msg"])

        if errors:
            return source_pb2.ValidationMessage(
                valid=False,
                errors=[
                    source_pb2.ValidationError(
                        location=location,
                        message=error,
                    )
                    for location, errors_ in errors.items()
                    for error in errors_
                ],
            )
        return source_pb2.ValidationMessage(valid=True)

    def Start(self: typing.Self, request: source_pb2.StartRequest, context: grpc.ServicerContext) -> protobuf.Empty:
        """Handle rpc.Start call."""
        self.logger.debug("Start called!")
        self.id = request.id
        self.name = request.name
        self.status = source_pb2.Status.STATUS_RUNNING
        return protobuf.Empty()

    def Stop(self: typing.Self, request: source_pb2.StopRequest, context: grpc.ServicerContext) -> protobuf.Empty:
        """Handle rpc.Stop call."""
        self.logger.debug("Stop called!")
        self.status = source_pb2.Status.STATUS_READY
        return protobuf.Empty()

    def GetStatus(
        self: typing.Self,
        request: protobuf.Empty,
        context: grpc.ServicerContext,
    ) -> source_pb2.StatusMessage:
        """Handle rpc.GetStatus call."""
        self.logger.debug("GetStatus called!")
        return source_pb2.StatusMessage(status=self.status)

    def GetDetails(
        self: typing.Self,
        request: protobuf.Empty,
        context: grpc.ServicerContext,
    ) -> source_pb2.DetailsMessage:
        """Handle rpc.GetDetails call."""
        self.logger.debug("Details called!")
        return source_pb2.DetailsMessage(id=self.id, type=self.source_type, version=self.source_version, name=self.name)


class Source(BaseSource):
    """Implement grpc Source to handle data transfer for plugin."""

    streaming: bool = False

    def __init__(self: typing.Self, broker: Broker, **kwargs: P.kwargs) -> None:
        super().__init__(**kwargs)
        self.broker = broker

    def get_data(
        self: typing.Self,
        manager: Manager,
        config: RunConfig,
    ) -> protobuf.Empty:
        """Perform actual get data based on configuration and send to provided Manager."""
        raise NotImplementedError

    def GetData(
        self: typing.Self,
        request: source_pb2.DataMessage,
        context: grpc.ServicerContext,
    ) -> protobuf.Empty:
        """Handle rpc.GetData call."""
        self.logger.debug("Data called!")
        channel = self.broker.Dial(request.manager)
        mgr = Manager(channel)

        config = self._run_config_class.from_struct(request.source)

        return self.get_data(mgr, config)


class StreamingSource(BaseSource):
    """Implement grpc StreamingSource to handle streaming data transfer for plugin."""

    streaming: bool = True

    def __init__(self: typing.Self, broker: Broker, **kwargs: P.kwargs) -> None:
        super().__init__(**kwargs)
        self.broker = broker
        self.streams = {}

    def start_stream(
        self: typing.Self,
        manager: Manager,
        config: RunConfig,
    ) -> str:
        """Perform actual get data based on configuration and send to provided Manager."""
        raise NotImplementedError

    def StartStream(
        self: typing.Self,
        request: source_pb2.DataMessage,
        context: grpc.ServicerContext,
    ) -> source_pb2.StartedStreamMessage:
        """Handle rpc.StartStream call."""
        self.logger.debug("StartStream called!")
        channel = self.broker.Dial(request.manager)
        mgr = Manager(channel)

        config = self._run_config_class.from_struct(request.source)

        stream_id = self.start_stream(mgr, config)

        return source_pb2.StartedStreamMessage(
            ID=stream_id,
        )

    def stop_stream(
        self: typing.Self,
        stream_id: str,
    ) -> protobuf.Empty:
        """Stop a running stream."""
        raise NotImplementedError

    def StopStream(
        self: typing.Self,
        request: source_pb2.StopStreamMessage,
        context: grpc.ServicerContext,
    ) -> protobuf.Empty:
        """Handle rpc.StopStream call."""
        self.logger.debug("StopStream called!")
        return self.stop_stream(stream_id=request.ID)
