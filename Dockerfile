# Set base image (host OS)
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /serengeti

# Copy content of the application file to the working directory
COPY .env requirements.txt server.py setup.py ./
COPY app/ ./app
COPY static/ ./static

# Install dependencies
RUN apt update && \
apt install gcc -y && \
apt clean  && \
pip install --no-cache-dir --upgrade pip && \
pip install --no-cache-dir -r requirements.txt && \
python3 setup.py build_ext --inplace

# command to run on container start
CMD [ "python3", "./server.py" ]