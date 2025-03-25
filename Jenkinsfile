pipeline {
    agent any
    environment {
      SONAR_HOME = tool "sonar scanner"     // Must match the name in Global Tool Configuration
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checkout for github'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/ankesh5jan/FlaskJWT-Auth.git']])
            }
        }
        
        stage("SonarQube quality analysis"){
            steps{
                withSonarQubeEnv('sonar'){
                    sh "${SONAR_HOME}/bin/sonar-scanner -Dsonar.projectName=Auth-JWT-jenkins-webhook -Dsonar.projectKey=Auth-JWT-jenkins-webhook"
                }
            }
        }
        
        stage("Sonar quality gate scan"){
            steps{
                timeout(time: 2, unit: "MINUTES"){
                    waitForQualityGate abortPipeline: false
                }
            }
        }
        
        stage("Trivy file system scan"){
            steps{
                sh "trivy fs --format table -o trivy-fs-report.html ."
            }
        }
        
        stage('Build') {
            steps {
                echo 'Building the docker image'
                sh 'docker build -t auth-jwt .'
            }
        }
        stage('Push to docker hub') {
            steps {
                echo 'Pushing docker image on docker hub'
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'dockerHub', // ID of the Jenkins credential
                        usernameVariable: 'dockerHubUser',
                        passwordVariable: 'dockerHubPass'
                    )]) {
                        // Log in to Docker Hub securely
                        sh "echo '${env.dockerHubPass}' | docker login -u '${env.dockerHubUser}' --password-stdin"

                        // Tag the image before pushing
                        sh "docker tag auth-jwt ${env.dockerHubUser}/auth-jwt:latest"

                        // Push the image to Docker Hub
                        sh "docker push ${env.dockerHubUser}/auth-jwt:latest"

                        // Logout from Docker Hub (security best practice)
                        sh "docker logout"
                    }
                }
            }
        }
        stage('Deploy'){
            steps{
                echo 'Deploying the docker container'
             //   sh "docker run -p 5000:5000 -d ankesh236/auth-jwt:latest"
                sh "docker-compose down && docker-compose up -d"
            }
        }

    }
}
