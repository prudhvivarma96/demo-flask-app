pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds') // Jenkins credentials ID
        IMAGE_NAME = "prudhvivarma96/demo-flask-app"
        EC2_USER = "ubuntu"            // Replace with your EC2 SSH username
        EC2_HOST = "your.ec2.ip.addr"  // Replace with your EC2 public IP
        SSH_KEY_ID = "ec2-ssh-key"     // Jenkins stored SSH private key ID for EC2
        CONTAINER_NAME = "demo-flask-app"
        PORT = 5000
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
                    python3 -m venv venv --system-site-packages
                    . venv/bin/activate
                    pip install --upgrade pip --break-system-packages
                    pip install -r requirements.txt --break-system-packages
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
                sh "docker build -t $IMAGE_NAME:latest ."
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $IMAGE_NAME:latest
                    '''
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(credentials: ["${SSH_KEY_ID}"]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no $EC2_USER@$EC2_HOST \\
                        'docker pull $IMAGE_NAME:latest && \\
                         docker stop $CONTAINER_NAME || true && \\
                         docker rm $CONTAINER_NAME || true && \\
                         docker run -d --name $CONTAINER_NAME -p $PORT:5000 $IMAGE_NAME:latest'
                    """
                }
            }
        }
    }

    post {
        success {
            echo '✅ Build, push, and deploy completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Check logs for errors.'
        }
    }
}

