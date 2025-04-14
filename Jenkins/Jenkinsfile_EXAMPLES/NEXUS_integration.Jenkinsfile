pipeline {
    agent any

    environment {
	    NEXUS_USER = 'admin'
        NEXUS_PASSWORD = credentials('NEXUS_PASSWORD')
        
    }

    stages {
        stage('Pull_image') {
            steps {
                echo "Trying to login on Nexus docker repository"
                sh "docker login -u ${NEXUS_USER} -p ${NEXUS_PASSWORD} 127.0.0.1:8123"
				sh "docker pull 127.0.0.1:8123/keeper-tester:latest"
            }
			steps {
			    sh 'docker run -d 127.0.0.1:8123/keeper-tester:latest echo "Hello! I am $(uname)"'
			}
        }
    }

}
