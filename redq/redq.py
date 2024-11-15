from collections import namedtuple
from functools import wraps
from queue import Queue
from typing import Callable, Deque

import logging

logger = logging.getLogger(__name__)

function_notation = namedtuple("function_notation", ["function", "args", "kwargs"])

taks_queue: Deque = Queue(maxsize=3)


class EnqueueError(Exception):
    """Raised when the queue is full"""


def redq(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            taks_queue.append(function_notation(func, args, kwargs))
            logger.info(f"Task added to queue: {func.__name__}")
            return taks_queue

        except Exception:
            msg = f"Error adding task to queue: {func.__name__}"
            logger.error(msg)
            raise EnqueueError(msg)

    return wrapper
