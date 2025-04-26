pipeline {
    agent any 
    environment {
        SONAR_HOME = tool "sonar"
    }
    stages {
        stage ("git-cloning") {
            steps {
                git url: "https://github.com/furkhan-2000/delete.git", branch: "main"
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
                dependencyCheck additionalArguments: '--scan .', odcInstallation: 'owasp' 
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
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
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhubCred',
                    usernameVariable: 'DOCKERHUB_USERNAME',
                    passwordVariable: 'DOCKERHUB_PASSWORD')]) {
                        sh "docker tag jenkins-testing-web:latest ${DOCKERHUB_USERNAME}/shark:testing-web"
                        sh "docker login -u ${DOCKERHUB_USERNAME} -p ${DOCKERHUB_PASSWORD}"
                        sh "docker push ${DOCKERHUB_USERNAME}/shark:testing-web"
                    }
            }
        }
    }
}
