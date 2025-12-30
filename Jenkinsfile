pipeline {
  agent any

  options {
    timestamps()
    disableConcurrentBuilds()
  }

  environment {
    VENV = "${WORKSPACE}\\.venv"
    PYTHONUNBUFFERED = "1"
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python venv') {
      steps {
        bat """
          python --version
          python -m venv .venv
          call .venv\\Scripts\\activate
          python -m pip install --upgrade pip
        """
      }
    }

    stage('Install dependencies') {
      steps {
        bat """
          call .venv\\Scripts\\activate
          pip install -r requirements.txt
          pip install pytest pytest-cov
        """
      }
    }

    stage('Unit Tests (pytest)') {
      steps {
        bat """
          call .venv\\Scripts\\activate
          set PYTHONPATH=%WORKSPACE%
          if not exist reports mkdir reports
          python -m pytest -q --junitxml=reports\\junit.xml
        """
      }
      post {
        always {
          junit 'reports/junit.xml'
        }
      }
    }

    stage('Build (package artifact)') {
      steps {
        bat """
          if not exist dist mkdir dist
          powershell -NoProfile -Command ^
            "Compress-Archive -Path * -DestinationPath dist\\flaskapp-%BUILD_NUMBER%.zip -Force"
        """
        archiveArtifacts artifacts: 'dist/*.zip', fingerprint: true
      }
    }

    stage('Deploy (simulate)') {
      steps {
        bat """
          if exist C:\\tmp\\flaskapp_target rmdir /S /Q C:\\tmp\\flaskapp_target
          mkdir C:\\tmp\\flaskapp_target
          powershell -NoProfile -Command ^
            "Expand-Archive -Path dist\\flaskapp-%BUILD_NUMBER%.zip -DestinationPath C:\\tmp\\flaskapp_target -Force"
          echo %DATE% %TIME% > C:\\tmp\\flaskapp_target\\DEPLOYED_AT.txt
          echo Deploy simulation complete.
        """
      }
    }
  }

  post {
    always {
      cleanWs()
    }
  }
}
