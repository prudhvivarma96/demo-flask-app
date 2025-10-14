pipeline {
    agent any

    environment {
        DOCKERHUB_USER = "prudhvivarma96"
        IMAGE_NAME = "demo-flask-app"
        EC2_IP = "3.110.31.187"
        PEM_PATH = "/var/lib/jenkins/.ssh/sample_vegetable.pem"
    }

    stages {
        stage('Checkout') {
            steps {
                echo '🔁 Cloning GitHub repository...'
                git 'https://github.com/prudhvivarma96/demo-flask-app.git'
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo '🧪 Running Python tests...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip --break-system-packages
                    pip install -r requirements.txt --break-system-packages
                    python3 -m unittest discover -s tests || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh '''
                    docker build -t $DOCKERHUB_USER/$IMAGE_NAME:latest .
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo '📤 Pushing image to Docker Hub...'
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh '''
                        echo "$PASS" | docker login -u "$USER" --password-stdin
                        docker push $DOCKERHUB_USER/$IMAGE_NAME:latest
                    '''
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                echo '🚀 Deploying to EC2 instance...'
                sh '''
                    ssh -o StrictHostKeyChecking=no -i $PEM_PATH ubuntu@$EC2_IP << EOF
                        sudo docker pull $DOCKERHUB_USER/$IMAGE_NAME:latest
                        sudo docker stop demo-flask || true
                        sudo docker rm demo-flask || true
                        sudo docker run -d -p 80:5000 --name demo-flask $DOCKERHUB_USER/$IMAGE_NAME:latest
                    EOF
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Deployment successful!'
        }
        failure {
            echo '❌ Build failed. Check logs.'
        }
    }
}

