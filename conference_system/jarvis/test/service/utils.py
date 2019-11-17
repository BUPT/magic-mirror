"""
File: utils.py
Author: Duan-JM
Email: vincent.duan95@outlook.com
Github: https://github.com/Duan-JM
Description:
    Define some common use functions
"""
import sys


from loguru import logger

def init_logger():
    """
    params: save_path (string): where to save the log

    return logger
    """
    def success_filter(record):
        return record["level"].no == logger.level("SUCCESS").no

    def normal_filter(record):
        return record["level"].no == logger.level("INFO").no

    def debug_filter(record):
        return record["level"].no == logger.level("DEBUG").no

    def critical_filter(record):
        return record["level"].no == logger.level("CRITICAL").no

    def color_fmt(color1, color2):
        fmt = f"<{color1}>" + "{time:YYYY-MM-DD at HH:mm:ss} " + f"</{color1}>"\
            + "| {level} | " + f"<{color2}>" + "{message}" + f"</{color2}>"

        return fmt

    logger.configure(
        handlers=[
            dict(sink=sys.stderr, format=color_fmt("green", "cyan"), filter=normal_filter),
            dict(sink=sys.stderr, format=color_fmt("cyan", "red"), filter=success_filter),
            dict(sink=sys.stderr, format=color_fmt("blue", "yellow"), filter=debug_filter),
            dict(sink=sys.stderr, format=color_fmt("blue", "red"), filter=critical_filter),
        ]
    )

    return logger
