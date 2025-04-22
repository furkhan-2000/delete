@Library("global") _
pipeline {
    agent any
    stages {
        stage('calling') {
            steps {
                script {
                    myecho()
                }
            }
        }
        stage('code') {
            steps {
                echo "This is a cloning process"
                gitclone("https://github.com/furkhan-2000/delete", "main")
            }
        }
        stage('build') {
            steps {
                echo "container down 😔😔successfully"
                sh "docker compose down"
                echo "container running 🥳🥳successfully"
                sh "docker compose up -d"
            }
        }
        stage('tagging & pushing') {
            steps {
                script {
                    docker_login("testing-web", "latest")
                }
            }
        }
        stage('deploy') {
            steps {
                echo "This is where we deploy, currently no deployment"
            }
        }
    }
}
