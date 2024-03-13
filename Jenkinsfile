pipeline {
    agent {
        label 'windows'
    }

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
                    bat 'python -m venv venv'
                    bat '.\\venv\\Scripts\\activate'
                    bat 'pip install -r requirements.txt'
                }
            }
        }

        stage('Run tests') {
            steps {
                // Run Python unit tests
                script {
                    bat 'python -m pytest --verbose'
                }
            }
        }
    }
}
