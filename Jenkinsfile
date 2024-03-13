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
                    bat './venv/Scripts/activate'
                    bat 'pip install -r requirements.txt'
                }
            }
        }

        stage('Run tests') {
            steps {
                // Run Python unit tests
                script {
                    // sh 'export QT_QPA_PLATFORM=offscreen'
                    // sh 'Xvfb :99 &'
                    // sh 'export DISPLAY=:99'
                    bat '. venv/bin/activate && python -m pytest --verbose'
                }
            }
        }
    }
}
