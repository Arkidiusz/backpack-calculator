pipeline {
    agent {
        docker {
            image 'python'
        }
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout your source code from version control
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                // Install Python dependencies using a virtual environment
                script {
                    sh 'python -m venv venv'
                    sh 'source venv/bin/activate && pip install -r requirements.txt'
                }
            }
        }

        stage('Run tests') {
            steps {
                // Run your Python unit tests
                script {
                    sh 'source venv/bin/activate && python -m unittest discover -s tests -p "test_*.py"'
                }
            }
        }
    }
}