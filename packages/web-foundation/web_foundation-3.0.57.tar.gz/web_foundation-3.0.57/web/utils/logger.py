import logging
import sys

from loguru import logger
from pydantic import BaseModel, conint


class FileLoggerSettings(BaseModel):
    log_file: str
    rotation_trigger: str  # "500 MB"  "12:00" "1 week" "10 days"
    compression: str  # "zip"
    retention: str


class LoggerSettings(FileLoggerSettings):
    log_level: conint(ge=0, le=50) = 20  # 10 - DEBUG, 20 - INFO, 30 - WARNING, 40 - ERROR, 50 - CRITICAL
    log_sql: bool = False
    socket_port: int = None  # use when multiprocessing of transports is true


class LogsHandler(logging.Handler):
    def __init__(self, file_log_settings: FileLoggerSettings | None):
        super().__init__()
        if file_log_settings:
            logger.add(file_log_settings.log_file, rotation=file_log_settings.rotation_trigger,
                       compression=file_log_settings.compression, retention=file_log_settings.retention)

    def emit(self, record):
        logger_opt = logger.opt(depth=10, exception=record.exc_info)
        try:
            logger_opt.log(record.levelname, record.getMessage())
        except Exception as exx:
            logger.warning(f"LOGGER {record.name} ERROR {exx}")
            pass


def setup_loggers(file_log_settings: FileLoggerSettings | None = None):
    handler = LogsHandler(file_log_settings)
    for logger_name, logger_obj in logging.root.manager.loggerDict.items():
        logging.getLogger(logger_name).handlers.clear()
        logging.getLogger(logger_name).handlers = [handler]
        # logging.basicConfig(handlers=[handler], level=0, force=True)


def configure_loggers(conf: LoggerSettings | None = None, log_sql: bool = False) -> None:
    from pygments import highlight
    from pygments.formatters.terminal import TerminalFormatter
    from pygments.lexers.sql import PostgresLexer

    if conf:
        # loguru.logger.remove()
        logger.add(conf.log_file, enqueue=True, rotation=conf.rotation_trigger,
                   compression=conf.compression, retention=conf.retention)
        logger.add(conf.log_file.replace(".log", ".json"), enqueue=True, rotation=conf.rotation_trigger,
                   compression=conf.compression, retention=conf.retention, serialize=True)

    postgres = PostgresLexer()
    terminal_formatter = TerminalFormatter()

    class PygmentsFormatter(logging.Formatter):
        def __init__(
                self,
                fmt="{asctime} - {name}:{lineno} - {levelname} - {message}",
                datefmt="%H:%M:%S",
        ):
            self.datefmt = datefmt
            self.fmt = fmt
            logging.Formatter.__init__(self, None, datefmt)

        def format(self, record: logging.LogRecord):
            """Format the logging record with slq's syntax coloration."""
            own_records = {
                attr: val
                for attr, val in record.__dict__.items()
                if not attr.startswith("_")
            }
            message = record.getMessage()
            name = record.name
            asctime = self.formatTime(record, self.datefmt)

            if name == "tortoise.db_client":
                if (
                        record.levelname == "DEBUG"
                        and not message.startswith("Created connection pool")
                        and not message.startswith("Closed connection pool")
                ):
                    message = highlight(message, postgres, terminal_formatter).rstrip()

            own_records.update(
                {
                    "message": message,
                    "name": name,
                    "asctime": asctime,
                }
            )

            return self.fmt.format(**own_records)

    class ExtendedLoggerHandler(logging.StreamHandler):
        def emit(self, record: logging.LogRecord) -> None:
            _logger = logger.opt(depth=6)  # need for correct filepath
            try:
                msg = self.format(record)
                _logger.log(record.levelname, msg)
            except RecursionError:  # See issue 36272
                raise
            except Exception:
                self.handleError(record)

    if log_sql or (conf and conf.log_sql):
        tortoise_fmt = PygmentsFormatter(
            fmt="{asctime} - {name}:{lineno} - {levelname} - {message}",
            datefmt="%Y-%m-%d_%H:%M:%S",
        )
        # tortoise_fmt = logging.Formatter(
        #     fmt="{asctime} - {name}:{lineno} - {levelname} - {message}",
        #     style="{",
        #     datefmt="%Y-%m-%d_%H:%M:%S",
        # )
        tortoise_handler = ExtendedLoggerHandler(sys.stdout)
        tortoise_handler.setLevel(logging.DEBUG)
        tortoise_handler.setFormatter(tortoise_fmt)

        # will print debug sql
        # logger_db_client = logging.getLogger("tortoise.db_client")
        # logger_db_client.setLevel(logging.DEBUG)
        # logger_db_client.addHandler(sh)

        logger_tortoise = logging.getLogger("tortoise")
        logger_tortoise.setLevel(logging.DEBUG)
        logger_tortoise.addHandler(tortoise_handler)

    # logger_sanic_access = logging.getLogger("sanic.access")
    from sanic.log import LOGGING_CONFIG_DEFAULTS
    sanic_access_fmt = logging.Formatter(
        fmt=LOGGING_CONFIG_DEFAULTS["formatters"]["access"]["format"],
        datefmt=LOGGING_CONFIG_DEFAULTS["formatters"]["access"]["datefmt"],
    )
    sanic_gen_fmt = logging.Formatter(
        fmt=LOGGING_CONFIG_DEFAULTS["formatters"]["generic"]["format"],
        datefmt=LOGGING_CONFIG_DEFAULTS["formatters"]["generic"]["datefmt"],
    )
    sanic_access_handler = ExtendedLoggerHandler(sys.stdout)
    sanic_access_handler.setFormatter(sanic_access_fmt)
    logging.getLogger("sanic.access").handlers = [sanic_access_handler]

    sanic_console_handler = ExtendedLoggerHandler(sys.stdout)
    sanic_console_handler.setFormatter(sanic_gen_fmt)
    logging.getLogger("sanic.root").handlers = [sanic_console_handler]
    logging.getLogger("sanic.server").handlers = [sanic_console_handler]

    sanic_err_console_handler = ExtendedLoggerHandler(sys.stderr)
    sanic_err_console_handler.setFormatter(sanic_gen_fmt)
    logging.getLogger("sanic.error").handlers = [sanic_err_console_handler]

    logger_sanic = logging.getLogger("sanic")
