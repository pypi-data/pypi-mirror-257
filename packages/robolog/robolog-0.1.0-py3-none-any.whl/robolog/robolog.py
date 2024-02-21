import os
import logging
import colorlog
from datetime import datetime
import logging
from typing import Dict


def get_logger(
    logger_name: str = "robolog",
    file_dir: str = "logs",
    stdo_lvl: int = logging.DEBUG,
    file_lvl: int = logging.DEBUG,
    use_file: bool = True,
    use_stdo: bool = True,
    use_colors: bool = True,
    file_name: str = None,
    stamp_fmt: str = "%Y%m",
    colors: Dict[str, str] = None,
    stdo_fmt: str = None,
    file_fmt: str = None,
    use_compact: bool = False,
    file_ext: str = "csv",
    date_fmt: str = "%H:%M:%S",
) -> logging.Logger:
    """
    Configure and return a logger instance with specified settings.

    Args:
    - logger_name (str): Name of the logger (default is "robolog").
    - file_dir (str): Directory to store log files (default is "logs").
    - stdo_lvl (int): Logging level in standard output (default is logging.DEBUG).
    - file_lvl (int): Logging level in file (default is logging.DEBUG).
    - use_file (bool): Flag to enable or disable file logging (default is True).
    - use_stdo (bool): Flag to enable or disable standard output logging (default is True).
    - use_colors (bool): Flag to enable or disable colored output (default is True).
    - file_name (str): Static file name for log files, if not provided, it is generated.
    - file_stamp (str): Timestamp format for log file names (default is "%Y%m").
    - colors (Dict[str, str]): Mapping of log level to color codes (default is None, using predefined colors).
    - stdo_fmt (str): Log format for standard output logs (default is detailed format).
    - file_fmt (str): Log format for file logs (default is CSV-like format).
    - use_compact (bool): Predefined shorter standard output line (default is False).
    - file_ext (str): File extension for log files (default is ".csv").
    - date_fmt (str): Timestamp format for standard output logs (default is "%H:%M:%S").

    Returns:
    - logging.Logger: Configured logger instance.

    Note:
    This function avoids duplicating loggers and sets the root logging level from default WARNING to DEBUG.
    """

    # Avoid duplicating loggers:
    if logger_name in logging.Logger.manager.loggerDict:
        return logging.getLogger(logger_name)

    # Set root logging lvl from default WARNING to DEBUG
    logging.getLogger().setLevel(logging.DEBUG)
    logger = logging.getLogger(logger_name)

    file_handler = None
    stdo_handler = None

    if use_file:
        _create_directory(file_dir)
        file_name = _get_file_name(file_name, stamp_fmt, file_ext)
        file_formatter = _get_file_formatter(file_fmt)
        file_handler = _get_file_handler(file_dir, file_name, file_lvl, file_formatter)
        logger.addHandler(file_handler)

    if use_stdo:
        color_fmt = _get_color_fmt(use_compact, stdo_fmt)
        stdo_formatter = _get_stdo_formatter(use_colors, colors, color_fmt, date_fmt)
        stdo_handler = _get_stdo_handler(stdo_lvl, stdo_formatter)
        logger.addHandler(stdo_handler)

    logger.propagate = True
    return logger


def _get_file_name(file_name, stamp_fmt, file_ext):
    now_stamp: str = f"{datetime.now():{stamp_fmt}}"
    if not file_name:
        return f"robologs_{now_stamp}.{file_ext}"
    return file_name


def _create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def _get_file_formatter(fmt_file):
    fmt = '{asctime};{levelname};{filename};{funcName};{lineno};"{message:s}"'
    if fmt_file:
        fmt = fmt_file
    formatter = logging.Formatter(fmt, style="{")
    return formatter


def _get_file_handler(dir_name, file_name, level_file, formatter):

    full_pth = os.path.join(dir_name, file_name)
    file_handler = logging.FileHandler(full_pth)
    file_handler.setLevel(level_file)
    file_handler.setFormatter(formatter)
    return file_handler


def _get_color_fmt(compact_stdo, fmt_stdo):
    fmt = "[{levelname:^7s}]({asctime})[{filename:^25}]({lineno:^3}) :: {message:s}"

    if compact_stdo:
        fmt = "[{levelname[0]}] ({asctime}) [{filename}]({lineno}): {message:s}"

    if fmt_stdo:
        fmt = fmt_stdo
    return "{log_color}" + fmt


def _get_stdo_formatter(use_colors, colors, color_fmt, date_format):

    colors = _get_colors(colors)
    if not use_colors:
        colors = {}
    stdo_formatter = colorlog.ColoredFormatter(
        color_fmt, style="{", log_colors=colors, datefmt=date_format
    )
    return stdo_formatter


def _get_colors(colors):
    default_colors = {
        "DEBUG": "white",
        "INFO": "bold_white",
        "WARNING": "bold_yellow",
        "ERROR": "bold_red",
    }

    if not colors:
        colors = default_colors
    return colors


def _get_stdo_handler(level, stdo_formatter):
    stdo_handler = colorlog.StreamHandler()
    stdo_handler.setLevel(level)
    stdo_handler.setFormatter(stdo_formatter)
    return stdo_handler


if __name__ == "__main__":

    CONFIG = {
        "logger_name": "dupal",
        "colors": {"INFO": "blue", "WARNING": "green", "ERROR": "purple"},
        "use_compact": False,
        "use_colors": True,
        "file_name": None,
        "file_ext": "txt",
        "stdo_fmt": None,  #     "[{levelname:^7s}] :: {message:s}"
        "stdo_lvl": logging.WARNING,
        "file_lvl": logging.ERROR,
    }

    log = get_logger(**CONFIG)
    log = get_logger(**CONFIG)

    log.debug("TEST DEBUG")
    log.info("TEST INFO")
    log.warning("TEST WARNING")
    log.error("TEST ERROR")
