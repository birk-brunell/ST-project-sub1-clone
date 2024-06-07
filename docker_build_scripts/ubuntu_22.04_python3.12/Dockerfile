FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Remove existing Python
RUN apt-get update && apt-get remove -y python3 python3-pip

# Add deadsnakes PPA for additional Python versions
RUN apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && apt-get install -y python3.12 python3.12-distutils python3-pip

# Copy and install requirements
WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Copy the test suite file
COPY test_suite.py /app/

# Run tests and keep the container running for inspection
CMD ["sh", "-c", "cat /etc/os-release && python3.12 --version && ls -l /app && python3.12 -m unittest test_suite && exec bash"]
