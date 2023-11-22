FROM python:3.10-slim-bullseye

# * Make sure apt-get doesn't run in interactive mode.
# * Update system packages.
# * Pre-install some useful tools.
# * Minimize system package installation.
RUN export DEBIAN_FRONTEND=noninteractive && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y --no-install-recommends tini procps net-tools \
  build-essential git make zip && \
  apt-get -y clean && \
  rm -rf /var/lib/apt/lists/*


# Install requirements
WORKDIR /opt/dagster
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add repository code
COPY . .
RUN pip install --no-cache-dir --editable .

# Set $DAGSTER_HOME and ensure dagster instance and workspace YAML there
ENV DAGSTER_HOME=/opt/dagster
COPY dagster.yaml workspace.yaml $DAGSTER_HOME

WORKDIR $DAGSTER_HOME