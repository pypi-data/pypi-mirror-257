"""Open telemetry Trace manager  """
from typing import Any, List, Optional

from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor


class TraceManager:
    """
    Class to handle OpenTelemetry Tracer instances with a singleton pattern.

    Attributes:
        _instance (TraceManager): Singleton instance of TraceManager.
        tracer (opentelemetry.trace.Tracer): OpenTelemetry tracer instance.
        exporters (list): List of OpenTelemetry exporters.

    Methods:
        _initialize_tracer(): Initializes the OpenTelemetry Tracer.
        get_instance(): Retrieves the singleton instance of TraceManager.
        add_exporter(exporter): Adds an OpenTelemetry exporter to the TraceManager.
        remove_exporter(exporter): Removes an OpenTelemetry exporter from the TraceManager.
        configure_exporters(): Configures the exporters for the TraceManager.
    """

    _instance: Optional["TraceManager"] = None
    exporters: List[Any]
    tracer: Any

    def __new__(cls) -> "TraceManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.tracer = cls._instance._initialize_tracer()
            cls._instance.exporters = []
        return cls._instance

    def _initialize_tracer(self):
        # Configure OpenTelemetry Tracer Provider
        tracer_provider = TracerProvider(resource=Resource.create({SERVICE_NAME: "processor"}))
        trace.set_tracer_provider(tracer_provider)

        # Create a Console exporter
        span_console_processor = SimpleSpanProcessor(ConsoleSpanExporter())

        tracer_provider.add_span_processor(span_console_processor)

        return trace.get_tracer(__name__)

    @classmethod
    def get_instance(cls):
        """
        Retrieves the singleton instance of TraceManager
        """
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def add_exporter(self, exporter):
        """
        Adds an OpenTelemetry exporter to the TraceManager.

        Args:
            exporter: OpenTelemetry exporter to be added.
        """
        if exporter not in self.exporters:
            self.exporters.append(exporter)

    def remove_exporter(self, exporter):
        """
        Removes an OpenTelemetry exporter from the TraceManager.

        Args:
            exporter: OpenTelemetry exporter to be removed.
        """
        if exporter in self.exporters:
            self.exporters.remove(exporter)
