# Set base image (host OS)
FROM python:3.8.8-buster

# Set the working directory in the container
WORKDIR /serengeti

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt
RUN apt install python3-dev
RUN apt install build-essential

# Copy content of the application
COPY app/ ./app
COPY static/ ./static
COPY .env .
COPY server.py .
COPY setup.py .

# Build c extention
RUN python3 setup.py build_ext --inplace

# command to run on container start
CMD [ "python", "./server.py" ]
