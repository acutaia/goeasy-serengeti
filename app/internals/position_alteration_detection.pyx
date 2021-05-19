#!python
#cython: language_level=3

"""
Haversine function

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
# Standard c++ library
from libc.math cimport sin, cos, asin, sqrt


# -------------------------------------------------------------------------------------------

# CONSTANTS
cdef double ITALY_LAT, ITALY_LON, PHI_ITALY, THETA_ITALY
cdef double SWEDEN_LAT, SWEDEN_LON, PHI_SWEDEN, THETA_SWEDEN
cdef str ITALY, SWEDEN
cdef long GPS_OFFSET,
cdef int LEAP_OFFSET
cdef long long GALILEO_OFFSET

# SATELLITE
GPS_OFFSET = 315964800000
LEAP_OFFSET = 18000
GALILEO_OFFSET = 935280000000

# ITALY
ITALY_LAT = 45.0781
ITALY_LON = 7.6761
PHI_ITALY = ITALY_LAT * 0.0174532925
THETA_ITALY = ITALY_LON * 0.0174532925
ITALY = "Italy"

# SWEDEN
SWEDEN_LAT = 59.3261
SWEDEN_LON = 18.0232
PHI_SWEDEN = SWEDEN_LAT * 0.0174532925
THETA_SWEDEN = SWEDEN_LON * 0.0174532925
SWEDEN = "Sweden"

# -------------------------------------------------------------------------------------------


def haversine(double lat, double lon) -> str:
    """Given a lat and lng returns the name of the nearest nation"""
    cdef double lat1, lng1, ph1, theta1
    cdef double dphi_italy, dtheta_italy, a_italy, italy_distance
    cdef double dphi_sweden, dtheta_sweden , a_sweden, sweden_distance

    lat1 = lat
    lng1 = lon

    ph1 = lat1 * 0.0174532925
    theta1 = lng1 * 0.0174532925

    dphi_italy = PHI_ITALY - ph1
    dphi_sweden = PHI_SWEDEN -ph1

    dtheta_italy = THETA_ITALY - theta1
    dtheta_sweden = THETA_SWEDEN - theta1

    a_italy = sin(dphi_italy/2)**2 +cos(ph1) * cos(PHI_ITALY) * sin(dtheta_italy/2)**2
    a_sweden = sin(dphi_sweden/2)**2 +cos(ph1) * cos(PHI_SWEDEN) * sin(dtheta_sweden/2)**2

    italy_distance = 2 * asin(sqrt(a_italy)) * 6367444.7
    sweden_distance = 2 * asin(sqrt(a_sweden)) * 6367444.7

    if italy_distance < sweden_distance:
        return ITALY

    return SWEDEN
