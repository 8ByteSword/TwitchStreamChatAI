import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from typing import Iterable, Union
import coloredlogs
from colorama import Fore, Style
from src.utils.logger_ansi_codes import ATTRIBUTES, COLORS, HIGHLIGHTS, RESET

def colored(
    text: str,
    color: Union[str, None] = None,
    on_color: Union[str, None] = None,
    attrs: Union[Iterable[str], None] = None,
) -> str:
    if text == "": return " "
    fmt_str = "\033[%dm%s"
    if color is not None:
        text = fmt_str % (COLORS[color], text)

    if on_color is not None:
        text = fmt_str % (HIGHLIGHTS[on_color], text)

    if attrs is not None:
        for attr in attrs:
            text = fmt_str % (ATTRIBUTES[attr], text)

    return text + RESET

class CustomFormatter(coloredlogs.ColoredFormatter):
    FORMATS = {
        logging.DEBUG: (f"[\033[1m%(asctime)s] [%(levelname)s{RESET}]\u001b[4m%(audit_path)s\u001b[0m%(message)s", {}),
        logging.INFO: (f"[\033[1m%(asctime)s] [%(levelname)s{RESET}]\u001b[4m%(audit_path)s\u001b[0m%(message)s", {}),
        logging.WARNING: (f"[\033[1m%(asctime)s] [%(levelname)s{RESET}]\u001b[4m%(audit_path)s\u001b[0m%(message)s", {}),
        logging.ERROR: (f"[\033[1m%(asctime)s] [%(levelname)s{RESET}]\u001b[4m%(audit_path)s\u001b[0m%(message)s", {}),
        logging.CRITICAL: (f"[\033[1m%(asctime)s] [%(levelname)s{RESET}]\u001b[4m%(audit_path)s\u001b[0m%(message)s", {})
    }

    COLOR_MAP = {
        logging.DEBUG: "cyan",
        logging.INFO: "green",
        logging.WARNING:"yellow",
        logging.ERROR: "red",
        logging.CRITICAL: "magenta",
    }

    def get_audit(self, record):
        try:
            return f"{record.audit_filename}:{record.audit_lineno}"
        except:
            return ""

    def format(self, record):
        fmt, kwargs = self.FORMATS.get(record.levelno)
        record.levelname = colored(record.levelname, color=self.COLOR_MAP.get(record.levelno))
        record.audit_path = colored(self.get_audit(record), color=self.COLOR_MAP.get(record.levelno), attrs=['underline'])
        if fmt:
            self._fmt = fmt
            self._style = logging.PercentStyle(fmt)
        if record.audit_path != "":
            record.audit_path = f" [{record.audit_path}] "

        return super().format(record, **kwargs)

class CustomLogger:

    @staticmethod
    def setup_custom_logging(logfile=None):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)

        formatter = CustomFormatter()
        ch.setFormatter(formatter)

        logger.addHandler(ch)

        if logfile:
            fh = RotatingFileHandler(logfile, maxBytes=10*1024*1024, backupCount=5)
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
