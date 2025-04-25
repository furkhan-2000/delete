@Library('shared') _
pipeline {
    agent any
    environment {
        SONAR_HOME = tool 'sonar'
    }
    stages {
        stage('git clone') {
            steps {
                script {
                gitclone('https://github.com/furkhan-2000/delete.git', 'main')
                }
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonar') {
                    sh """
                      ${SONAR_HOME}/bin/sonar-scanner \
                        -Dsonar.projectName=workouts \
                        -Dsonar.projectKey=workouts
                    """
                }
            }
        }
        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: false
                }
            }
        }
        stage('OWASP Dependency Check') {
            steps {
                dependencyCheck additionalArguments: '--scan ./', odcInstallation: 'owasp'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }
        stage('Trivy FS Scan') {
            steps {
                sh 'trivy fs --format table -o trivy-fs-report.html .'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker compose down --rmi all && docker compose up -d'
            }
        }
        stage('Push to Docker Hub') {
            steps {
                script {
               sh 'docker_login('testing-web', 'latest')'
                }
            }
        }
    }
}
