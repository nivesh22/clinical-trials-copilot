pipeline {
  agent any
  options { timestamps() }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Backend Setup') {
      steps {
        sh 'python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt'
      }
    }
    stage('Backend Lint/Test') {
      steps {
        sh '. .venv/bin/activate && ruff check && pytest --junitxml=test-results/py-tests.xml'
      }
      post { always { junit 'test-results/py-tests.xml' } }
    }
    stage('Frontend Setup') {
      steps {
        dir('ui') {
          sh 'npm ci || npm i'
        }
      }
    }
    stage('Frontend Lint/Test') {
      steps {
        dir('ui') {
          sh 'npm run lint || true'
          sh 'npm run typecheck || true'
          sh 'npm test -- --run || true'
        }
      }
    }
    stage('Build Images') {
      steps {
        sh 'docker build -t ctc-api -f docker/Dockerfile.app .'
        sh 'docker build -t ctc-ui -f docker/Dockerfile.ui ui'
      }
    }
    stage('Compose Integration') {
      steps {
        sh 'docker compose -f docker/docker-compose.yml up -d --build'
        sh 'sleep 5'
        sh 'curl -f http://localhost:8000/healthz'
        sh 'curl -f http://localhost:3000'
        sh 'curl -s -X POST http://localhost:3000/api/ask -H "Content-Type: application/json" -d "{\"question\":\"hi\"}"'
      }
      post {
        always {
          sh 'docker compose -f docker/docker-compose.yml down -v'
        }
      }
    }
  }
}

