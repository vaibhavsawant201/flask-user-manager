pipeline {
    agent any

    environment {
        AWS_REGION = "us-east-1"           // change if needed
        ECR_REPO = "flask-user-manager"     // your ECR repo name
        IMAGE_TAG = "latest"
        SONARQUBE = "SonarQubeServer"       // same as in Jenkins config
        DOCKER_HUB_CRED = "dockerhub"       // credential ID in Jenkins
        AWS_CRED = "aws"                    // credential ID in Jenkins
    }

    stages {

        stage('Code Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/vaibhavsawant201/flask-user-manager.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $ECR_REPO:$IMAGE_TAG .'
                }
            }
        }

        stage('Trivy Scan') {
            steps {
                script {
                    // If Trivy is not installed globally, use docker
                    sh '''
                    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                    aquasec/trivy image $ECR_REPO:$IMAGE_TAG > trivy-scan.txt || true
                    cat trivy-scan.txt
                    '''
                }
            }
        }

        stage('SonarQube Analysis') {
            environment {
                scannerHome = tool 'SonarScanner'  // name configured in Jenkins tools
            }
            steps {
                withSonarQubeEnv('SonarQubeServer') {
                    sh '''
                    $scannerHome/bin/sonar-scanner \
                      -Dsonar.projectKey=flask-user-manager \
                      -Dsonar.sources=. \
                      -Dsonar.host.url=http://54.85.14.197:9000 \
                      -Dsonar.login=${SONAR_TOKEN}
                    '''
                }
            }
        }

        stage('Push to ECR') {
            steps {
                withAWS(credentials: 'aws', region: "${AWS_REGION}") {
                    script {
                        sh '''
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin 547091556711.dkr.ecr.${AWS_REGION}.amazonaws.com
                        docker tag $ECR_REPO:$IMAGE_TAG 547091556711.dkr.ecr.${AWS_REGION}.amazonaws.com/$ECR_REPO:$IMAGE_TAG
                        docker push 547091556711.dkr.ecr.${AWS_REGION}.amazonaws.com/$ECR_REPO:$IMAGE_TAG
                        '''
                    }
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                withAWS(credentials: 'aws', region: "${AWS_REGION}") {
                    script {
                        sh '''
                        aws eks update-kubeconfig --region ${AWS_REGION} --name flask-user-manager
                        kubectl apply -f k8s/deployment.yaml
                        kubectl apply -f k8s/service.yaml
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'
        }
    }
}
