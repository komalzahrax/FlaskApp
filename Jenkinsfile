pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Setup venv & Install') {
      steps {
        bat '''
          python -m venv venv
          call venv\\Scripts\\activate
          python -m pip install --upgrade pip
          if exist requirements.txt pip install -r requirements.txt
        '''
      }
    }

    stage('Basic Checks / Tests') {
      steps {
        bat '''
          call venv\\Scripts\\activate
          python -m compileall .
          if exist tests pytest -q
        '''
      }
    }
  }
}
