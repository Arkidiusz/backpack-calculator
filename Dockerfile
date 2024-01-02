# Container for the Jenkins instance

# Use the official Jenkins image as the base image
FROM jenkins/jenkins

# Switch to the root user for administrative tasks
USER root

# Install essential packages and Python
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Switch back to the Jenkins user
USER jenkins