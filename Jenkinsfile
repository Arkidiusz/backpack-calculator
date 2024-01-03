pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout source code from version control
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                // Install Python dependencies using a virtual environment
                script {
                    sh 'python3 -m venv venv'
                    sh '. venv/bin/activate && pip install -r requirements.txt'
                }
            }
        }

        stage('Run tests') {
            steps {
                // Run Python unit tests
                script {
                    echo "Current Directory: ${pwd()}"
                    sh '. venv/bin/activate && pytest test'
                }
            }
        }
    }
}
