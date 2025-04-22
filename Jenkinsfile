@Library ("global") _
pipeline {
    agent any
    stages {
        stage ('calling') {
            steps {
                script {
                    myecho()
                }
            }
        }
        stage('code') {
            steps {
                echo "This is a code process"
                git url: "https://github.com/furkhan-2000/delete", branch: "main"
            }
        }
        stage('build') {
            steps {
                echo "This is building process"
                sh "docker compose up -d"
            }
        }
        stage('tagging & pushing') {
            steps {
                echo "This is where we tag and push our image"
                withCredentials([usernamePassword(
                    credentialsId: 'dockerHubCred',
                    usernameVariable: 'DOCKERHUB_USERNAME',
                    passwordVariable: 'DOCKERHUB_PASSWORD'
                )]) {
                    echo "This is tagging part"
                    sh "docker tag testing-web:latest ${DOCKERHUB_USERNAME}/shark:workouts"
                    sh "docker login -u ${DOCKERHUB_USERNAME} -p ${DOCKERHUB_PASSWORD}"
                    sh "docker push ${DOCKERHUB_USERNAME}/shark:workouts"
                }
            }
        }
        stage('deploy') {
            steps {
                echo "This is where we deploy, no deployemt"
            }
        }
    }
}