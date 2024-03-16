FROM jenkins/jenkins

USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv libglib2.0-0 libsm6 libxrender1 libxext6 xvfb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
USER jenkins
