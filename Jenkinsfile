pipeline {
    agent any

    environment{
        VENV_DIR = 'venv'
        GCP_PROJECT = "moonlit-vine-464915-u5"
        GLCOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
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
    }
}

