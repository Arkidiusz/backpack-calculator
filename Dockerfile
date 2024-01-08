# Use the official Jenkins image as the base image
FROM jenkins/jenkins

# Switch to the root user for administrative tasks
USER root

# Install necessary packages for Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch back to the Jenkins user
USER jenkins
