#!groovy


pipeline {
    agent any
    stages {
        stage("Build and up") {
            steps {
                sh "cp /home/jenkins/envs/musicapi.env .env"
                sh "docker compose up -d --build --remove-orphans"
            }
        }
    }
}
