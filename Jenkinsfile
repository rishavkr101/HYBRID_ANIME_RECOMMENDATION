pipeline {
    agent any

    environment{
        VENV_DIR = 'venv'
        GCP_PROJECT = "moonlit-vine-464915-u5"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        KUBECTL_AUTH_PLUGIN = "/usr/lib/google-cloud-sdk/bin"
    }


    stages{

        stage("Cloning from Github...."){
            steps{
                script{
                    echo 'Cloning from Github...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token2', url: 'https://github.com/rishavkr101/HYBRID_ANIME_RECOMMENDATION.git']])
                }
            }
        }

        stage("Making a Virtual environment...."){
            steps{
                script{
                    echo 'Making a Virtual environment...'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    pip install dvc
                    '''
                }
            }
        }


        stage('DVC Pull'){
            steps{
                withCredentials([file(credentialsId:"gcp-key2", variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'DVC PILL....'
                        sh '''
                        . ${VENV_DIR}/bin/activate
                        dvc pull
                        '''
                    }
                }
            }
        }

        stage('Build and Push Image to GCR'){
            steps{
                withCredentials([file(credentialsId:"gcp-key2", variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Build and Push Image to GCR'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet
                        docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .
                        docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                        '''
                    }
                }
            }
        }

        stage('Deploying to kubernetes..'){
            steps{
                withCredentials([file(credentialsId:"gcp-key2", variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Deploying to kubernetes..'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}:${KUBECTL_AUTH_PLUGIN}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud container clusters get-credentials ml-app-cluster --region us-central1
                        kubectl apply -f deployment.yaml
                        '''
                    }
                }
            }
        }



    }
}

