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

# Standard Library
import logging

# Third Party
from gunicorn.app.base import BaseApplication

# Internal
from app.main import app
from app.config import get_gunicorn_settings

# -------------------------------------------------------------------------------


class StandaloneApplication(BaseApplication):
    """Our Gunicorn application."""

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

# -------------------------------------------------------------------------------


if __name__ == '__main__':
    settings = get_gunicorn_settings()

    options = {
        "bind": "0.0.0.0",
        "workers": (settings.cores_number * 2) + 1,
        "keepalive": settings.keep_alive,
        "loglevel": settings.loglevel,
        "accesslog": "-",
        "errorlog": "-",
        "worker_class": "uvicorn.workers.UvicornWorker",
    }

    StandaloneApplication(app, options).run()
