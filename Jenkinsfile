@Library('shared') _
pipeline {
    agent any  
    environment {
        SONAR_HOME = tool 'sonar'
    }
    stages {
        stage("cloning git") {
            steps {
                script {
                    gitclone("https://github.com/furkhan-2000/delete.git", "main")
                }
            }
        }
        stage("sonarQube Quality Analysis") {
            steps {
                withSonarQubeEnv('sonar') {
                    sh "${SONAR_HOME}/bin/sonar-scanner -Dsonar.projectName=workouts -Dsonar.projectKey=workouts"
                }
            }
        }
        stage("Sonar Quality Gates") {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: false
                }
            }
        }
        stage("Owasp Dependency-Check") {
            steps {
              script {
                  owaspdepcheck()
              }
            }
        }
        stage("trivy fs scan") {
            steps {
                sh 'trivy fs --format table -o trivy-fs-report.html .'
            }
        }
        stage("deployment") {
            steps {
                sh "docker compose down --rmi all && docker compose up -d"
            }
        }  
        stage("pushing docker image") {
            steps {
                script {
                    docker_login('jenkins-testing-web','latest')
                }
            }
        }
    }
}
