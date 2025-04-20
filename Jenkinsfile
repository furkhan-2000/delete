@Library("firstLib") _
pipeline {
    agent { label 'slave' }
    stages {
        stage ('random') {
            steps {
                script{
                    snippets()
                }
            }
        }
        
        stage('code') {
            steps {
                script {
                   gitclone("https://github.com/furkhan-2000/delete", "main") 
                }
            }
        }
        stage('build') {
            steps {
                echo "this is building process"
                sh " docker compose down && docker compose up -d"
                echo "hi you have first down the container, and this is new container"
            }
        }
        stage('pushing image to docker-hub') {
            steps {
                script {
                   docker_push("testing-web", "latest", "furkhan2000") 
                }
            }
        }
        stage('deploy') {
            steps {
                echo 'this is deployment stage'
            }
        }
    }
}
