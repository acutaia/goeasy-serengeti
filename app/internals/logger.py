"""
Logger package

:author: Angelo Cutaia
:copyright: Copyright 2021, LINKS Foundation
:version: 1.0.0

..

    Copyright 2021 LINKS Foundation

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

# Standard Library
import logging
from functools import lru_cache

# Third Party
from aiologger.loggers.json import JsonLogger, Logger, LogLevel
from pydantic import BaseSettings

# ---------------------------------------------------------------------


class LoggerSettings(BaseSettings):
    log_level: str

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_logger() -> Logger:
    """Instantiate app logger"""
    settings = LoggerSettings()
    # Configure uvicorn logger
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.setLevel(settings.log_level)
    return JsonLogger.with_default_handlers(
        name="serengeti",
        level=getattr(LogLevel, settings.log_level, LogLevel.DEBUG),
        serializer_kwargs={"indent": 4},
    )
