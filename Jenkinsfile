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
                echo "This is a code process"
                gitclone("https://github.com/furkhan-2000/delete", "main")
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
                script {
                    docker_login("testing-web", "latest")
                }
            }
        }
        stage('deploy') {
            steps {
                echo "This is where we deploy, no deployment"
            }
        }
    }
}
