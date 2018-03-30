node {      // non-declarative pipeline
    def customImage         // 'customImage' variable declaration to refer to image built from Docker
    stage('Clone Repository') {     // declare a stage
        checkout scm        // this takes no actions at all
    }

    docker.withRegistry('https://reg.llharpy.com') {        // change docker registry from DockerHub to local registry

        docker.withServer('tcp://172.17.0.1:2375'){     // utilize remote host Docker
            stage('Build'){

                // build Docker image from Dockerfile in the root of the repository
                customImage = docker.build("reg.llharpy.com/calculator:${env.BRANCH_NAME}_${env.BUILD_ID}")
            }
            stage('Test'){

                // access the shell of built image
                customImage.inside{

                    // run shell command with return status code ( 0: success, Otherwise: failure)
                    def status = sh(script:"nose2 2> testoutput.txt", returnStatus: true)

                    // check if the shell finished with failure or seccess code. In this casem it captures failure.
                    if(status != 0){

                        // read text from a file, eliminate white spaces and store in the 'msg' variable. 
                        def msg = readFile("testoutput.txt").trim()

                        // send Slack notification
                        // to access environment variable like ${env.BRANH_NAME}, it is important to use "string" instead of 'string'.
                        // Or else, the string string would not be translated to the actual value. 
                        slackSend baseUrl:'https://globenet.slack.com/services/hooks/jenkins-ci/' , token: '9uVPCr3qCxZTyGz2symRKiiF', message:"reg.llharpy.com/calculator:${env.BRANCH_NAME}_${env.BUILD_ID} failed Test stage with msg: ${msg}"
                        currentBuild.result = "FAILED"
                        
                        // call for exit with status code from shell
                        exit status
                    }
                }
            }
            stage('Push'){

                // push customImage to registry (https://reg.llharpy.com)
                customImage.push()

                // run shell command to remove Docker image
                sh "docker rmi ${customImage.id}"
            }
            stage('Deploy'){

                // run shell command to stop any existing application on the remote Docker host
                // " || true " is required to ignore failure
                sh "docker -H 192.168.0.10 stop haruno_calculator || true"

                // run shell command to start current build of application on the remote Docker host
                sh "docker -H 192.168.0.10 run -d --rm -p 8080:8080 --name haruno_calculator reg.llharpy.com/calculator:${env.BRANCH_NAME}_${env.BUILD_ID}"
            }
            stage('Notify Slack'){

                // send Slack notification after overall success.
                slackSend baseUrl:'https://globenet.slack.com/services/hooks/jenkins-ci/' , token: '9uVPCr3qCxZTyGz2symRKiiF', message:"reg.llharpy.com/calculator:${env.BRANCH_NAME}_${env.BUILD_ID} successfully deployed"
            }
        }
    }
}