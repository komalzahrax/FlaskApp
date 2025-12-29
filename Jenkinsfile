pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python venv') {
      steps {
        bat '''
          python --version
          python -m venv venv
          call venv\\Scripts\\activate
          python -m pip install --upgrade pip
          if exist requirements.txt pip install -r requirements.txt
        '''
      }
    }

    stage('Sanity Check') {
      steps {
        bat '''
          call venv\\Scripts\\activate
          python -m compileall .
        '''
      }
    }
  }
}
