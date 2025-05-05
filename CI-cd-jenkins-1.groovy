pipeline {
  agent {label 'devops'} 
  environment {
    SONAR_HOME= tool 'sonar'
  }
  stages {
    stage ('cleaning') {
      steps {
        cleanWs()
      }
    }
    stage ('cloning') {
      steps {
        git url: 'https://github.com/furkhan-2000/delete', branch: 'main'
      }
    }
    stage ('Dynamic Tagging') {
      steps {
        script {
          def commitHash= sh(
            script: "git rev-parse --short HEAD",
            returnStdout: true
          ).trim()
          env.IMAGE_TAG= commitHash 
        }
      }
    }
    stage ('Sonar Analysis') {
      parallel {
        stage ('SAST') {
          steps {
            withSonarQubeEnv('sonar') {
              sh "${SONAR_HOME}/bin/sonar-scanner -Dsonar.projectName= workouts -Dsonar.projectKey= workouts"
            }
          }
        }
        stage ('Quality Gates') {
          steps {
            timeout(time: 2, unit: 'MINUTES') {
              script {
                def qg = waitForQualityGate(abortPipeline: false) 
                if (qg.status != "OK") {
                  error "Quality gate Failed: ${qg.status}"
                }
              }
            } 
          }
        }
      }
    }
    stage ('owasp') {
      steps {
        timeout(time: 25, unit: 'MINUTES') {
          retry(2) {
            dependencyCheck(
              additionalArguments: '''
               --scan .
               --format XML
               --out ./
               --prettyPrint 
               ''',
               odcInstallation: 'owasp' )  }
               dependencyCheckPublisher pattern: 'dependency-check-report.xml'
          }
        }
      }
      stage ('trivy') {
        steps {
          sh "trivy fs /kubernetes --severity-check vuln,config"
        }
      }
      stage ('building') {
        steps {
          sh "docker compose up -d"
        }
      }
      stage ('authenticate & pushing') {
        steps {
          withCredentials([usernamePassword(
            credentialsId: 'dockerhubCred',
            usernameVariable: 'DOCKERHUB_USERNAME',
            passwordVariable: 'DOCKERHUB_PASSWORD'
          )]) {
            sh '''
            docker tag testing:${env.IMAGE_TAG} ${DOCKERHUB_USERNAME}/shark:${env.IMAGE_TAG} 
            docker login -u ${DOCKERHUB_USERNAME} -p ${DOCKERHUB_PASSWORD}
            docker push ${DOCKERHUB_USERNAME}/shark:${env.IMAGE_TAG} 
            '''
          }
        }
      }
    }
    post {
      success {
        build job: "CD-JOb",
        wait: false, 
        propagate: false,
        parameters: [string(name: 'IMAGE_TAG', value: "${env.IMAGE_TAG}")]
      }
      failure {
        mail to: "cisco@admin"
        subject: "pipeline created"
        body: "pipeline was unsuccessfull check logs ${env.BUILD_NUMBER} and ${env.BUILD_URL}"
      }
    }
  }
---
pipeline {
  agent {label 'jenkins'} 

  parameters {
    string(name: 'IMAGE_TAG', defaultValue: '', description: 'this is CI associated Image Tag')
  }
  environment {
    GIT_REPO= 'https://github.com/furkhan-2000/delete.git'
    DOCKER_IMAGE= 'furkhan2000/shark'
    DOCKER_TAG= "${params.IMAGE_TAG}"
    CD_DEPLOYMENT= 'dep'
  }
  stages {
    stage ('cleaning') {
      steps {
        cleanWs()
      }
    }
    stage ('Verify CI Output') {
      steps {
        script {
          if (!env.DOCKER_TAG) {
            error "Tag not found"
          }
          echo "Tag Found ${env.DOCKER_TAG}"
        }
      }
    }
    stage ('updating K8 deps') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'githubCred',
          usernameVariable: 'GITHUB_USERNAME',
          passwordVariable: 'GITHUB_PASSWORD'
        )]) {
          sh ''' 
          git clone ${GIT_REPO} manifests 
          cd manifests 
          sed -i "s|image: ${DOCKER_IMAGE}:.*|image: ${DOCKER_IMAGE}:${DOCKER_TAG}|g" /kubernetes/deployment.yaml
          git config user.name "ubama"
          git config user.email "support@cisco"
          git add /kubernetes/deployment.yaml
          git commit -m "updating K8-dep manifests" 
          git push https://${GITHUB_USERNAME}:${GITHUB_PASSWORD}@github.com/furkhan-2000/delete
          '''
        }
      }
    }
    stage ('rollout-status') {
      steps {
        script {
          def deploymentStatus = sh(
            script: "kubectl rollout status deployment/${env.CD_DEPLOYMENT} --timeout=90s"
            returnStatus: true 
          )
          if (deploymentStatus != 0) {
            echo "Deployment failed" 
            sh "kubectl rollout undo deployment/${env.CD_DEPLOYMENT}"
            def rolloutStatus = sh(
              script: "kubectl rollout status deployment/${env.CD_DEPLOYMENT} --timeout=90s",
              returnStatus: true 
            )
            if (rolloutStatus !=0) {
              error "Deployment failed manual intervention required"
            } else {
              error "Deployment failed, but rollback success."
            }
          } else {
            echo "Deployment is Healthy"
          }
        }
      }
    }
  }
  post {
    success {
      mail to: "team@cisco" 
      subject: "pipeline success"
      body: "hi team our CI/CD pipeline got success here is image: ${DOCKER_IMAGE}:${DOCKER_TAG}"
    }
    failure {
      mail to: "support@cisco" 
      subject: "pipeline failed" 
      body: "hi team pipeline failed please check and resolve this issue the no is ${env.BUILD_NUMBER} and logs : ${env.BUILD_URL}"
    }
  }
}
