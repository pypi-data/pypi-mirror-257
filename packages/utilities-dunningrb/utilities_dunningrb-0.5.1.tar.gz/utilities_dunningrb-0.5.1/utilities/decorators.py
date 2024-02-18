"""This module defines decorators.
"""

import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)


def timing(func):
    """A timing decorator. Writes statements to the log.

    Use:
        from decorators.timing import timing

        @timing
        def my_method():
            [do something]

    For a decorated method, two statements will be written to the log at INFO level:
        (1) A timestamp when the method is started.
        (2) A timestamp when the method ends along with duration in seconds.

    Example log entries:

    INFO:: Function main started at 2024-02-01 20:31:01.455775.
    (other log statements....)
    INFO:: Function main ended at 2024-02-01 20:31:01.456583 with duration 0.001 seconds
    """

    def wrapper(*args, **kwargs):
        name = f"Function {func.__name__}"
        started_at = f"started at {datetime.now()}"
        logger.info(f"{name} {started_at}.")

        clock_start = time.time()
        result = func(*args, **kwargs)
        clock_end = time.time()

        finished_at = f"finished at {datetime.now()}"
        with_duration = f"with duration {(clock_end - clock_start):.3f} seconds"
        logger.info(f"{name} {finished_at} {with_duration}.")

        return result

    return wrapper
