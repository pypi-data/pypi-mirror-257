import os,sys
import json
from multillm.BaseLLM import BaseLLM
from multillm.Prompt import Prompt
import requests

""" Google vertexai imports """
import vertexai
from vertexai.preview.language_models import TextGenerationModel
from vertexai.preview.language_models import ChatModel, InputOutputTextPair
from anthropic import AnthropicVertex


# Google ANTHROPIC interface
"""
The CLAUDE class extends the BaseModel class and overrides the get_response() method, providing an implementation.
The get_response() method takes a response parameter and returns the content of the first response in the given response object.
"""
class CLAUDE(BaseLLM):
    

    #implement here
    def __init__ (self, **kwargs):

       
        # add values here directly or if kwargs are specified they are taken from the config file
        defaults  = {
            "class_name" : "CLAUDE",
            "model" : "chat-bison@001",
            "credentials" : "key.json"
        }
        #if kwargs:
        # super().__init__(kwargs)
        #else:
        #    super().__init__(defaults)

        
    
    # Get Text
    def get_content(self, response):
        """
        Anthropic response: {
    "id": "msg_0187fAnrkoF8HbKm1Pi6jthf",
    "content": [
        {
        "text": "Here is a sample C function to test TCP sockets:\n\n```c\n#include <stdio.h> \n#include <stdlib.h>\n#include <string.h>\n#include <sys/types.h>\n#include <sys/socket.h>\n#include <netinet/in.h>\n#include <arpa/inet.h>\n\nvoid test_tcp_socket()\n{\n  int socket_fd;\n  struct sockaddr_in server_address;\n\n  // Create socket file descriptor\n  socket_fd = socket(AF_INET, SOCK_STREAM, 0);\n  if(socket_fd < 0) {\n    perror(\"Error opening socket\");\n    exit(1);\n  }\n\n  // Initialize server address \n  memset(&server_address, 0, sizeof(server_address));  \n  server_address.sin_family = AF_INET;\n  server_address.sin_addr.s_addr = inet_addr(\"127.0.0.1\"); // Server IP address \n  server_address.sin_port = htons(5000); // Server port\n\n  // Connect to server\n  if(connect(socket_fd, (struct sockaddr*) &server_address, sizeof(server_address)) < 0){\n    perror(\"Connection failed\");\n    exit(1);\n  }\n\n  printf(\"Connected to the server!\\n\");\n\n  close(socket_fd);\n}\n```\n\nThis function creates a TCP client socket, connects to a server listening on localhost port 5000, and prints a success message if connection is successful. It closes the socket afterwards.",
        "type": "text"
        }
    ],
    "model": "claude-instant-1.2",
    """
        resp = response
        #sys.stdout = sys.__stdout__
    
        """ Get the text from the response of an LLM """
        try:
            if self.is_code(str(resp)):
                print("{0} response: {1}" .format(self.__class__.__name__,str(resp)))
                return str(resp), True
            else:
                #print('CLAUDE is not code')
                print("{0} response: {1}" .format(self.__class__.__name__,str(resp)))
                return str(resp), False
        except Exception as e:
            #print("error is_code() {0}" .format(str(e)))
            return('CLAUDE response failed {}'.format(e))


    def get_response1(self, prompt: Prompt, taskid=None, convid = None):
    
    
        """Predict using a Large Language Model."""
        project_id = "verifai-ml-training"
        location = "us-central1"
        
        """ Get credentials file set in the config, and set appropriate variables for your model """
        if not os.path.exists(self.credentials):
            print("({0}) error:  credential file doesn't exist" .format(self.__class__.__name__))
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials
        """
        vertexai.init(project=project_id, location=location)
        print('model {0}' .format(self.model))
        chat_model = ChatModel.from_pretrained(self.model)
        "client_id" =  "xxxxxx",
        "client_secret": "xxxx",
        "quota_project_id": "verifai-ml-training",
        "refresh_token": "1//06LRKjz4n1BBHCgYIARAAGAYSNgF-L9Ir2oB1-gO0hIjXcbMVVgrpYLSTtoxGLhT8DB7MsfmOkSNsh1gcaLkKP9PxBVxOJmT1pw",
        "type": "authorized_user"
        """ 
        try:
            with open(self.credentials, 'r') as file:
                # Load the JSON data from the file
                cred = json.load(file)
                print('cred: {0}' .format(cred))
            
        except Exception as e:
            print('(multi_llm) error: could not load credentials {0} : {1}' .format(self.credentials,str(e)))
            return
        
        parameters = {
            "max_output_tokens" :  1024,
            "top_p" :  0.8,
            "top_k" :  40,
            "temperature" : 0.2
        }
        url = "https://us-central1-aiplatform.googleapis.com/v1/projects/" + cred['quota_project_id'] + "/locations/us-central1/publishers/google/models/chat-bison:predict"
        """ If context file exists, use it """
        context = ""
        if prompt.context:
            context = prompt.get_context()

        """ Create a Chat_model """        

        payload = {
        "instances": [{
            "context":  context,
            
            "messages": [
            { 
                "author": "user",
                "content": prompt.get_string(),
            }],
        }],
        "parameters": parameters
        }

        try:
            """ Call API """
            headers = {"Authorization": "Bearer " + cred['refresh_token'], "Content-Type" :  "application/json", 'accept': "application/json"}
            

            response = requests.post(url, data=json.dumps(payload),headers=headers)
            print("CLAUDE Response: {0}" .format(response.text))
            data = response.json()
            
        except Exception as e:
            print('error calling CLAUDE: {0}' .format(str(e)))

        if not response:
            return response
        else: 
            content, is_code = self.get_content(response)
            if content and taskid:
                self.publish_to_redis(content, taskid)
            return(content), is_code 

    


    def get_response(self, prompt: Prompt, taskid=None, convid = None):
        
        
        """Predict using a Large Language Model."""
        project_id = "verifai-ml-training"
        location = "us-central1"
        
        """ Get credentials file set in the config, and set appropriate variables for your model """
        if not os.path.exists(self.credentials):
            print("({0}) error:  credential file doesn't exist" .format(self.__class__.__name__))
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials

        vertexai.init(project=project_id, location=location)
        print('model {0}' .format(self.model))

        client = AnthropicVertex(region="us-central1", project_id=project_id)

        """ If context file exists, use it """
        parameters = {
             "max_output_tokens" :  1024,
             "top_p" :  0.8,
             "top_k" :  40,
            "temperature" : 0.2
        }
        context = ""
        if prompt.context:
            context = prompt.get_context()

        try:
            response = client.messages.create(   
                    max_tokens=1024,
                    messages=[ {
                    "role": "user",
                    "content": prompt.get_string(),
                }
                ],
            model="claude-instant-1p2",
            )
        except Exception as e:
              print('error calling CLAUDE: {0}' .format(str(e)))

        #response = self.get_content(response.model_dump_json(indent=2))
        resp = response.model_dump_json()
        res = json.loads(resp)
        """ getting res["content"][0]["text"] """
        c = res["content"]
        d = c[0]
        resp = d["text"]

        response = self.get_content(resp)


        if not response:
            return None, None
        else: 
            content, is_code = self.get_content(response)
            if content and taskid:
                self.publish_to_redis(content, taskid)
            return(content), is_code

