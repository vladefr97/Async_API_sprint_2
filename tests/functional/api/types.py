from typing import Awaitable, Callable, Dict, Union

AsyncGET = Callable[[str, Dict[str, Union[str, float]]], Awaitable]
