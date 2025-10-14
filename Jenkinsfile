pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds') // Jenkins credentials ID
        IMAGE_NAME = "prudhvivarma96/demo-flask-app"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/prudhvivarma96/demo-flask-app.git'
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    if [ -d "tests" ]; then
                        python3 -m unittest discover -s tests
                    else
                        echo "No tests directory found, skipping..."
                    fi
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:latest .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $IMAGE_NAME:latest
                    '''
                }
            }
        }
    }

    post {
        success {
            echo '✅ Build and push successful!'
        }
        failure {
            echo '❌ Build failed. Check logs.'
        }
    }
}

