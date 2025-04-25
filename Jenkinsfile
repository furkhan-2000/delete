pipeline {
    agent any 
    environment {
        SONAR_HOME = tool "sonar"
    }
    stages {
        stage ("git clone")  {
            steps {
                git url: "https://github.com/furkhan-2000/delete.git", branch: "main"
            }
        }
        stage ("soanrQube Quality Analysis") {
            steps {
                withSonarQubeEnv("sonar") {
                    sh "$SONAR_HOME/bin/sonar-scanner -Dsonar.projectName=workouts -Dsonar.projectKey=workouts"
                }
            }
        }
        stage ("sonar Qube Quality Gate") {
            steps {
                timeout(time: 2, unit: "MINUTES") {
                    waitForQualityGate abortPipeline: false 
                }
            }
        }
        stage ("OWASP") {
            steps {
                dependencyCheck additionalArguments: '--scan ./', odcInstallation: 'owasp'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }
        stage ("trivy file system scan") {
            steps {
                sh "trivy fs --format table -o trivy-fs-report.html ."
            }
        }
        stage ("Building image") {
            steps {
                sh "docker compose down --rmi all && docker compose up -d "
            }
        }
        stage ("push to DockerHub") {
            steps {
             withCredentials([usernamepassword(credentialsId: 'dockerhubCred',
                                               usernameVariable: 'DOCKERHUB_USERNAME',
                                               passwordVariable: 'DOCKERHUB_PASSWORD')]) {
             sh "docker tag testing-web:latest ${DOCKERHUB_USERNAME}/shark:workouts"
             sh "docker login -u ${DOCKERHUB_USERNAME} -p ${DOCKERHUB_PASSWORD}"
             sh "docker push $DOCKERHUB_USERNAME/shark:workouts"
    }
}
