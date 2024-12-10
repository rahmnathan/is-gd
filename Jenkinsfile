pipeline {
    agent {
        kubernetes {
            yaml """
kind: Pod
metadata:
  name: jenkins-agent
spec:
  containers:
  - name: jnlp
    image: rahmnathan/inbound-agent
    imagePullPolicy: Always
    tty: true
    volumeMounts:
      - name: docker
        mountPath: /var/run/docker.sock
    securityContext:
      runAsGroup: 998 # docker group on K8s node
      runAsUser: 1000 # jenkins user in container
  volumes:
    - name: docker
      hostPath:
        path: '/var/run/docker.sock'
"""
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout([$class           : 'GitSCM',
                          branches         : [[name: '*/main']],
                          extensions       : scm.extensions,
                          userRemoteConfigs: [[
                                                      url          : 'git@github.com:rahmnathan/is-gd.git',
                                                      credentialsId: 'Github-Git'
                                              ]]
                ])
            }
        }
        stage('Tag') {
            steps {
                script {
                    sh 'git config --global user.email "rahm.nathan@protonmail.com"'
                    sh 'git config --global user.name "rahmnathan"'
                    sshagent(credentials: ['Github-Git']) {
                        sh 'mkdir -p /home/jenkins/.ssh'
                        sh 'ssh-keyscan  github.com >> ~/.ssh/known_hosts'
                        sh "git tag ${BUILD_NUMBER}"
                        sh "git push origin tag ${BUILD_NUMBER}"
                    }
                }
            }
        }
        stage('Docker Build/Push') {
            environment {
                DOCKERHUB = credentials('Dockerhub')
            }
            steps {
                sh 'docker login -u="$DOCKERHUB_USR" -p="$DOCKERHUB_PSW"'
                sh "docker build -t rahmnathan/is-gd:${BUILD_NUMBER} ./src"
                sh "docker build -t rahmnathan/is-gd ./src"
                sh "docker push rahmnathan/is-gd:${BUILD_NUMBER}"
                sh "docker push rahmnathan/is-gd"
            }
        }
    }
}