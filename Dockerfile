FROM apache/airflow:2.9.1-python3.10

# Set the working directory
WORKDIR /opt/airflow

# Switch to root user to install dependencies
USER root

# Install git
RUN apt-get update && apt-get install -y git

# Switch back to airflow user
USER airflow

# Copy requirements.txt
COPY requirements.txt /opt/airflow/requirements.txt

# Install pip dependencies as airflow user
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

# Copy the rest of your codebase
COPY . /opt/airflow
