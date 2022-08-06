from typing import Callable

import time
from datetime import datetime
from functools import wraps

from config import logger


def backoff(start_sleep_time: float = 0.1, factor: int = 2, border_sleep_time: float = 1) -> Callable:
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)
    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep = start_sleep_time
            retries = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except BaseException as err:
                    logger.info(f"Unexpected {err=}, {type(err)=}")
                    if sleep >= border_sleep_time:
                        logger.info(f"{datetime.now()} Maximum wait time exceeded")
                        break
                    else:
                        time.sleep(sleep)
                        sleep = start_sleep_time * (factor**retries)
                        retries += 1

        return inner

    return func_wrapper
