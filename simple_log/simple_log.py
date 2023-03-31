from contextlib import contextmanager
import logging
from logging import Handler, LogRecord


class SimpleLog(list[LogRecord]):
    def _get_for_level(self, level: int) -> list[LogRecord]:
        # TODO: store each level's item indices for faster list generation
        return [r for r in self if r.levelno == level]

    @property
    def debugs(self) -> list[LogRecord]:
        return self._get_for_level(logging.DEBUG)

    @property
    def infos(self) -> list[LogRecord]:
        return self._get_for_level(logging.INFO)

    @property
    def warnings(self) -> list[LogRecord]:
        return self._get_for_level(logging.WARNING)

    @property
    def errors(self) -> list[LogRecord]:
        return self._get_for_level(logging.ERROR)

    @property
    def criticals(self) -> list[LogRecord]:
        return self._get_for_level(logging.CRITICAL)


class ListHandler(Handler):
    log: SimpleLog

    def __init__(self) -> None:
        self.log = SimpleLog()
        super().__init__(logging.NOTSET)

    def emit(self, record: LogRecord) -> None:
        # TODO: handle multithreading/multiprocessing (see todo in README)

        # store the formatted message on the record
        record.msg_formatted = self.format(record)
        self.log.append(record)


def add_log_to_logger(name: str) -> SimpleLog:
    # TODO: Does this make sense? Document usage if so. Main concern is that
    #  it might make more sense to pass in a logger instead of name, but then
    #  it's not consistent with redirect_logger_to_log. Does that matter?
    logger = logging.getLogger(name)
    list_handler = ListHandler()
    logger.addHandler(list_handler)
    return list_handler.log


@contextmanager
def redirect_logger_to_log(name: str) -> SimpleLog:
    logger = logging.getLogger(name)
    original_handlers = logger.handlers
    original_propagate = logger.propagate

    list_handler = ListHandler()
    if root_handlers := logging.root.handlers:
        list_handler.formatter = root_handlers[0].formatter

    try:
        for handler in original_handlers:
            logger.removeHandler(handler)
        logger.addHandler(list_handler)
        logger.propagate = False

        yield list_handler.log

    finally:
        logger.propagate = original_propagate
        logger.removeHandler(list_handler)
        for handler in original_handlers:
            logger.addHandler(handler)
