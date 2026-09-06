// Jenkins pipeline for the Flask backend.
// Configure a Jenkins "Pipeline" job pointing at this repository with
// "Script Path" = Jenkinsfile, and enable the GitHub webhook trigger below
// (requires the GitHub / GitHub Integration plugin).

pipeline {
    agent any

    triggers {
        // Fires the pipeline automatically when GitHub sends a push webhook to
        // http://<jenkins-host>:8080/github-webhook/
        githubPush()
    }

    environment {
        APP_DIR      = '/home/ubuntu/apps/flask-backend'
        PM2_APP_NAME = 'flask-backend'
        APP_PORT     = '5000'
    }

    stages {
        stage('Checkout') {
            steps {
                // Jenkins fills this in automatically for a "Pipeline script from SCM" job.
                // Left explicit here too so the file also works as a standalone Pipeline job.
                git branch: 'main', url: 'https://github.com/<your-username>/flask-backend.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests/ --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }

        // Optional Enhancement (assignment item 17): pull a secret from Jenkins
        // Credentials instead of hardcoding it. Create a "Secret text" credential
        // named "flask-api-key" under Manage Jenkins > Credentials, then uncomment:
        //
        // stage('Load Secrets') {
        //     steps {
        //         withCredentials([string(credentialsId: 'flask-api-key', variable: 'API_KEY')]) {
        //             sh 'echo "API key loaded securely (value is masked in the log)"'
        //         }
        //     }
        // }

        stage('Deploy') {
            steps {
                sh '''
                    mkdir -p "$APP_DIR"
                    rsync -a --delete --exclude venv --exclude .git --exclude tests ./ "$APP_DIR"/

                    cd "$APP_DIR"
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt

                    pm2 delete "$PM2_APP_NAME" || true
                    PORT=$APP_PORT pm2 start app.py --name "$PM2_APP_NAME" --interpreter "$APP_DIR/venv/bin/python3"
                    pm2 save
                '''
            }
        }
    }

    post {
        success {
            echo "Flask backend built, tested, and deployed successfully (build #${env.BUILD_NUMBER})."
        }
        failure {
            echo "Flask backend pipeline failed (build #${env.BUILD_NUMBER}) - check the stage logs above."
        }
    }
}
