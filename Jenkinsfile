node {
  def app
  stage('Clone Repository') { // for display purposes
    checkout scm          
  }
  def customImage
  docker.withRegistry('https://reg.llharpy.com') {
    stage('Build'){
      customImage = docker.build("reg.llharpy.com/calculator:${env.BUILD_ID}")
    }

    stage('Test'){
      customImage.inside{
        def status = sh(script:"nose2 2> testoutput.txt", returnStatus: true)
        if(status != 0){
          def msg = readFile("testoutput.txt").trim()
          slackSend baseUrl:'https://globenet.slack.com/services/hooks/jenkins-ci/' , token: '9uVPCr3qCxZTyGz2symRKiiF', message:"reg.llharpy.com/calculator:${env.BUILD_ID} failed Test stage with msg: ${msg}"
          currentBuild.result = "FAILED"
          exit status
        }
        
      }
      
    }
    stage('Push'){
      customImage.push()
      sh "docker rmi ${customImage.id}"
    }
    stage('Deploy'){
      
      sh "docker -H 192.168.0.10 stop haruno_calculator || true"
      sh "docker -H 192.168.0.10 run -d --rm -p 8080:8080 --name haruno_calculator reg.llharpy.com/calculator:${env.BUILD_ID}"
    }
    stage('Notify Slack'){

      slackSend baseUrl:'https://globenet.slack.com/services/hooks/jenkins-ci/' , token: '9uVPCr3qCxZTyGz2symRKiiF', message:"reg.llharpy.com/calculator:${env.BUILD_ID} successfully deployed"
    }
  }
   

}