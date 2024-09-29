import logging
import logging.handlers
import os
from pathlib import Path

_trace_installed = False


def initialize(logFilePath: str = ""):
    install_trace_logger()

    # logging.basicConfig(level=logging.DEBUG)
    # logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
    # logging.basicConfig(format='%(asctime)s %(message)s', filename='waterflowers.log', level=logging.INFO)

    if logFilePath != "" and not logFilePath.endswith("/"):
        logFilePath = logFilePath + "/"

    os.makedirs(Path(logFilePath), exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.handlers.TimedRotatingFileHandler(logFilePath + 'Scan2Pdf.log', when='midnight',
                                                      interval=1, backupCount=3, encoding=None, delay=False, utc=False,
                                                      atTime=None),
            logging.StreamHandler()
        ])


def install_trace_logger():
    global _trace_installed
    if _trace_installed:
        return
    level = logging.TRACE = logging.DEBUG - 5

    def log_logger(self, message, *args, **kwargs):
        if self.isEnabledFor(level):
            self._log(level, message, args, **kwargs)

    logging.getLoggerClass().trace = log_logger

    def log_root(msg, *args, **kwargs):
        logging.log(level, msg, *args, **kwargs)

    logging.addLevelName(level, "TRACE")
    logging.trace = log_root
    _trace_installed = True

