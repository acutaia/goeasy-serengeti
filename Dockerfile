# `python-base` sets up all our shared environment variables
FROM python:3.9-slim as python-base
LABEL manteiner = "Angelo Cutaia <angeloxx92@hotmail.it>"

    # python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=1000 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.1.6 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# `builder-base` stage is used to build deps + create our virtual environment
FROM python-base as builder-base
LABEL stage=builder

# obtain all the needed dependencies for building
RUN apt update && apt upgrade -y
RUN apt install curl -y && apt install build-essential -y
RUN apt install python3-dev -y
RUN python -m pip install pip --upgrade
RUN pip install Cython
RUN apt install cargo -y
RUN pip install maturin

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev --no-root

# cleaning
RUN rm poetry.lock && rm pyproject.toml

# `builder-cython` stage is used to build cython extension and prepare the directory
FROM python-base as builder-cython
LABEL stage=builder

# update python dependencies
RUN apt update && apt upgrade -y
RUN apt install build-essential -y
RUN python -m pip install pip --upgrade
RUN pip install Cython

# set working dir
WORKDIR /build

# copy
COPY app/ ./app
COPY .env server.py setup.py ./
COPY static/ ./static

# build
RUN python setup.py build_ext --inplace

# cleaning
RUN rm setup.py && \
   rm app/internals/position_alteration_detection.pyx && \
   rm app/internals/position_alteration_detection.c

# Copy
RUN mkdir serengeti && \
    cp -r app serengeti && \
    cp -r static serengeti && \
    cp .env serengeti && \
    cp server.py serengeti

# `production` image used for runtime
FROM python-base as production

# Copy python path and compiled code
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY --from=builder-cython build/serengeti /serengeti

# Set the working directory in the container
WORKDIR /serengeti

# command to run on container start
CMD [ "python", "./server.py" ]