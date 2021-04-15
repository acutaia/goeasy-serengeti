# Set base image (host OS)
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /serengeti

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN apt-get update && apt-get install gcc -y && apt-get clean
RUN pip3 install --no-cache-dir -r requirements.txt


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