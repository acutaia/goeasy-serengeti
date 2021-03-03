# Set base image (host OS)
FROM ubuntu:20.04

# Set the working directory in the container
WORKDIR /serengeti

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN apt update

RUN apt install build-essential -y
RUN apt install python3.8-dev -y
RUN apt install python3-pip -y

RUN pip3 install pip --upgrade
RUN pip3 install -r requirements.txt


# Copy content of the application
COPY app/ ./app
COPY static/ ./static
COPY .env .
COPY server.py .
COPY setup.py .

# Build c extention
RUN python3 setup.py build_ext --inplace

# command to run on container start
CMD [ "python3", "./server.py" ]