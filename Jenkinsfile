pipeline {
  agent any

  options {
    timestamps()
    disableConcurrentBuilds()
  }

  environment {
    VENV = "${WORKSPACE}/.venv"
    PYTHONUNBUFFERED = "1"
  }

  stages {

    stage('Checkout') {
      steps {
        // pulls from GitHub (configured in Jenkins job)
        checkout scm
      }
    }

    stage('Setup Python venv') {
      steps {
        sh '''
          python3 --version
          python3 -m venv .venv
          . .venv/bin/activate
          python -m pip install --upgrade pip
        '''
      }
    }

    stage('Install dependencies') {
      steps {
        sh '''
          . .venv/bin/activate
          pip install -r requirements.txt
          pip install pytest pytest-cov
        '''
      }
    }

    stage('Unit Tests (pytest)') {
      steps {
        sh '''
          . .venv/bin/activate
          mkdir -p reports
          pytest -q --junitxml=reports/junit.xml
        '''
        junit 'reports/junit.xml'
      }
    }

    stage('Build (package artifact)') {
      steps {
        sh '''
          mkdir -p dist
          tar --exclude=.venv --exclude=dist --exclude=reports -czf dist/flaskapp-${BUILD_NUMBER}.tgz .
        '''
        archiveArtifacts artifacts: 'dist/*.tgz', fingerprint: true
      }
    }

    stage('Deploy (simulate)') {
      steps {
        sh '''
          rm -rf /tmp/flaskapp_target
          mkdir -p /tmp/flaskapp_target
          tar -xzf dist/flaskapp-${BUILD_NUMBER}.tgz -C /tmp/flaskapp_target

          # “simulate restart”
          date > /tmp/flaskapp_target/DEPLOYED_AT.txt
          echo "Deploy complete. Simulated restart done."
        '''
      }
    }
  }

  post {
    always {
      cleanWs()
    }
  }
}
