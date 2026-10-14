pipeline {
  agent any

  environment {
    SONAR_HOST_URL = 'http://demo-control-plane:30900'
    IMAGE          = "demo-app:${env.BUILD_NUMBER}"
  }

  options { timestamps(); timeout(time: 20, unit: 'MINUTES') }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Test') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          pip install -r requirements.txt
          pytest --cov=app --cov-report=xml --junitxml=junit.xml
        '''
      }
      post { always { junit 'junit.xml' } }
    }

    stage('SonarQube Scan + Quality Gate') {
      steps {
        withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
          sh '''
            sonar-scanner \
              -Dsonar.host.url=$SONAR_HOST_URL \
              -Dsonar.token=$SONAR_TOKEN \
              -Dsonar.qualitygate.wait=true \
              -Dsonar.qualitygate.timeout=300
          '''
        }
      }
    }

    stage('Build Image') {
      steps {
        sh '''
          docker build -t $IMAGE .
          kind load docker-image $IMAGE --name demo
        '''
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
          sh '''
            kubectl apply -f k8s.yaml
            kubectl set image deployment/demo-app demo-app=$IMAGE
            kubectl rollout status deployment/demo-app --timeout=120s
          '''
        }
      }
    }
  }
}
