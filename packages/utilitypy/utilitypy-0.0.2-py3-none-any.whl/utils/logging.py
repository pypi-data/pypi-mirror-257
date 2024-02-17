import logging as _logging
import os as _os


def init_logger(file=True, stdout=False, path=None, level="debug", file_level="debug", stream_level="debug", format=None, name=None, mode="w"):
    '''The `init_logger` function initializes a logger with options to log to a file and/or output to
    stdout.

    Parameters
    ----------
    file, optional
        A boolean value indicating whether to enable logging to a file. If set to True, a file handler will
    be created and added to the logger. If set to False, no file handler will be created.
    stdout, optional
        A boolean value indicating whether to enable logging to the console (stdout). If set to True, log
    messages will be displayed on the console. If set to False, log messages will not be displayed on
    the console.
    path
        The `path` parameter is used to specify the file path where the log file will be created. If no
    path is provided, the log file will be created in the "log" directory with the name "runtime.log".
    level, optional
        The "level" parameter determines the logging level for the logger. It accepts values such as
    "debug", "info", "warning", "error", and "critical". The logger will only log messages that have a
    level equal to or higher than the specified level.
    file_level, optional
        The `file_level` parameter determines the logging level for the file handler. It specifies the
    minimum severity level of log messages that will be written to the log file.
    stream_level, optional
        The `stream_level` parameter determines the logging level for the stream handler, which outputs log
    messages to the console (stdout). The available levels are:
    format
        The format parameter is a string that specifies the format of the log messages. It uses
    placeholders to include various information in the log message, such as the timestamp, log level,
    function name, file path, line number, and the log message itself. The default format is
    '%(asctime)s | %(
    name
        The name parameter is used to specify the name of the logger. It is an optional parameter and if
    not provided, a default name will be assigned to the logger.
    mode, optional
        The "mode" parameter specifies the mode in which the log file is opened. It determines whether the
    file is opened for writing, appending, or other operations. The default value is "w", which means
    the file is opened in write mode, and any existing content in the file is overwritten.

    Returns
    -------
        a logger object.

    '''
    file_handler = None
    stream_handler = None

    # Create a logger
    level = getattr(_logging, level.upper())
    logger = _logging.getLogger(name)
    logger.setLevel(level)


    # Create a formatter
    formatter = _logging.Formatter(format or '%(levelname)s  | %(asctime)s | (%(funcName)s) - %(pathname)s, line %(lineno)d | %(message)s')

    if file:
        # Create a file handler
        if path is None:
            path = _os.path.join("log", "runtime.log")
            _os.makedirs("log", exist_ok=True)

        file_level = getattr(_logging, file_level.upper())
        file_handler = _logging.FileHandler(path, mode=mode)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(file_level)
        logger.addHandler(file_handler)

    if stdout:
        # Create a stream handler to output to stdout
        stream_level = getattr(_logging, stream_level.upper())
        stream_handler = _logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(stream_level)
        logger.addHandler(stream_handler)

    return logger
