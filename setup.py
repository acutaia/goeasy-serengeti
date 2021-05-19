
"""
Building app.utilities.haversine module

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

from setuptools import setup, find_packages, Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension(
        "app.internals.position_alteration_detection",  # location of the resulting .so
        ["app/internals/position_alteration_detection.pyx"],
    )
]


setup(
    name="package",
    packages=find_packages(),
    cmdclass={"build_ext": build_ext},
    ext_modules=ext_modules,
)
