@Library('shared') _
pipeline {
    agent any 
    environment {
        SONAR_HOME = tool "sonar"
    }
    stages {
        stage ("git-cloning") {
            steps {
                script {
                gitclone("https://github.com/furkhan-2000/delete.git", "main")
                }
            }
        }
        stage ("sonarQube Quality Analysis") {
            steps {
               withSonarQubeEnv('sonar') {
                   sh "${SONAR_HOME}/bin/sonar-scanner -Dsonar.projectName=Workouts -Dsonar.projectKey=Workouts"
               }   
            }
        }
        stage ("sonar Quality Gates") {
            steps {
                timeout(time:2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: false
                }
            }
        }
        stage ("owasp Dependency-Check") {
            steps {
               script {
                   owaspdepcheck()
               }
            }
        }
        stage ("trivy fs scan") {
            steps {
                sh "trivy fs --format table -o trivy-fs-report.html ."
            }
        }
        stage ("building image") {
            steps {
                sh "docker compose up -d"
            }
        }
        stage ("pushing image to docker") {
            steps {
                script {
                   docker_login('testing-web', 'latest') 
                }
            }
        }
    }
}
