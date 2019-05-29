FROM python:3.7-slim-stretch

# Update to latest packages and add build-essential and python-dev
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
            build-essential=12.3 \
            python-dev=2.7.13-2 && \
    rm -fr /var/lib/apt/lists/*

# Install Dumb Init
RUN pip install dumb-init==1.2.2

# Install required packages.
COPY test-requirements.txt /tmp/
RUN pip install -r /tmp/test-requirements.txt

# Create non-root user
RUN useradd --create-home app
USER app
WORKDIR /home/app

# Copy the code
COPY . /home/app

RUN pip install --user -e .

RUN touch fake.db

# Use Dumb Init's entrypoint.
ENTRYPOINT ["dumb-init", "--"]
