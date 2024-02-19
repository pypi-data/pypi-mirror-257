"""Logging trace formater """

import logging

from opentelemetry import trace


class TraceFormatter(logging.Formatter):
    """
    Formatter class to include trace information in log records.

    Methods:
        format(record): Formats the log record with trace information.
    """

    def format(self, record):
        """
        Formats the log record with trace information.

        Args:
            record (logging.LogRecord): Log record to be formatted.

        Returns:
            str: Formatted log message including trace information.
        """
        current_span = trace.get_current_span()

        trace_id = current_span.get_span_context().trace_id if current_span else None
        record.trace_id = hex(trace_id) if trace_id else ""

        return super().format(record)
