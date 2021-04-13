#!/usr/bin/env python3
"""
Gunicorn App main entry point

:author: Angelo Cutaia
:copyright: Copyright 2021, Angelo Cutaia
:version: 1.0.0

..

    Copyright 2021 Angelo Cutaia

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

# Third Party
from gunicorn.app.base import BaseApplication
from pydantic import BaseSettings

# Internal
from app.main import app

# -------------------------------------------------------------------------------


class GunicornSettings(BaseSettings):
    log_level: str
    cores_number: int
    keep_alive: int
    server_port: int
    max_requests: int
    max_requests_jitter: int
    timeout: int

    class Config:
        env_file = ".env"


# -------------------------------------------------------------------------------


class StandaloneApplication(BaseApplication):
    """Our Gunicorn application."""

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


# -------------------------------------------------------------------------------


if __name__ == "__main__":
    settings = GunicornSettings()

    options = {
        "bind": f"0.0.0.0:{settings.server_port}",
        "workers": (settings.cores_number * 2) + 1,
        "keepalive": settings.keep_alive,
        "loglevel": settings.log_level,
        "accesslog": "-",
        "errorlog": "-",
        "max_requests": settings.max_requests,
        "max_requests_jitter": settings.max_requests_jitter,
        "timeout": settings.timeout,
        "worker_class": "uvicorn.workers.UvicornWorker",
    }

    StandaloneApplication(app, options).run()
