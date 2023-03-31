import logging
from logging import Handler, Logger, LogRecord


class SimpleLog(list[LogRecord]):
    def _filter(self, level: int) -> list[LogRecord]:
        return [r for r in self if r.levelno == level]

    @property
    def debugs(self) -> list[LogRecord]:
        return self._filter(logging.DEBUG)

    @property
    def infos(self) -> list[LogRecord]:
        return self._filter(logging.INFO)

    @property
    def warnings(self) -> list[LogRecord]:
        return self._filter(logging.WARNING)

    @property
    def errors(self) -> list[LogRecord]:
        return self._filter(logging.ERROR)

    @property
    def criticals(self) -> list[LogRecord]:
        return self._filter(logging.CRITICAL)


class ListHandler(Handler):
    log: SimpleLog

    def __init__(self) -> None:
        self.log = SimpleLog()
        super().__init__()

    def emit(self, record: LogRecord) -> None:
        self.log.append(record)


def capture_logging(logger: Logger) -> SimpleLog:
    if any([not isinstance(h, ListHandler) for h in logger.handlers]):
        logger.warn(
            'Logger has other handlers than ListHandler;'
            ' logging may still be emitted.'
        )

    handler = ListHandler()
    logger.addHandler(handler)
    return handler.log
