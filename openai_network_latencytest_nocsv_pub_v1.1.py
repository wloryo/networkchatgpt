import json
import os
import openai
import requests
import time
import pprint
import datetime
import socket
import numpy

##############################################
# liang wang, 20230601, 1.1.0 version
# Setting up the deployment name
deployment_name = "<your input>"
# The base URL for your Azure OpenAI resource. e.g. "https://<your resource name>.openai.azure.com"
openai_api_base = "https://<your input>.openai.azure.com"
# The API key for your Azure OpenAI resource.
openai_api_key = "<your input>"
# Example prompt for request payload
prompt = "how are you"
# number of test cases to run
numberoftest = 10
# Currently OPENAI API have the following versions available: 2022-12-01. All versions follow the YYYY-MM-DD date structure.
openai_api_version = "2022-12-01"
##############################################

devicename = socket.gethostname()
ip = socket.gethostbyname(devicename)
peip = socket.getaddrinfo("yosemite-openai.openai.azure.com",443)

# Request URL
api_url = f"{openai_api_base}/openai/deployments/{deployment_name}/completions?api-version={openai_api_version}"

print("question : ", prompt)

# Json payload
# To know more about the parameters, checkout this documentation: https://learn.microsoft.com/en-us/azure/cognitive-services/openai/reference
json_data = {
  "prompt": prompt,
  "temperature":0,
  "max_tokens": 30
}

# Including the api-key in HTTP headers
headers =  {"api-key": openai_api_key}

try:
    # Request for creating a completion for the provided prompt and parameters
    nowdatetime = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    print("time utc : ", nowdatetime)
    print("open AI endpoint : IP ", peip, " FQDN ", openai_api_base)
    print("IP for this VM : ", ip)
    print("total test cases : ", numberoftest)
    rarray = numpy.zeros(0)
    for num in range(numberoftest):
        startdatetime = datetime.datetime.utcnow().strftime('%m%d_%H:%M:%S')
        start = time.time()
        response = requests.post(api_url, json=json_data, headers=headers)
        responsetime = str((time.time() - start))
        enddatetime = datetime.datetime.utcnow().strftime('%m%d_%H:%M:%S')
        completion = response.json()
        rarray = numpy.append(rarray,float(responsetime))

        textresult = completion['choices'][0]['text']
        print(num+1, responsetime,startdatetime, enddatetime, ip, peip, prompt, textresult)
    
    
    print("p50: ",numpy.percentile(rarray, 50) )
    print("p80: ",numpy.percentile(rarray, 80) )
    print("p90: ",numpy.percentile(rarray, 90) )
    print("p95: ",numpy.percentile(rarray, 95) )
    print("p98: ",numpy.percentile(rarray, 98) )
    print("p99: ",numpy.percentile(rarray, 99) )
    print("average: ",numpy.average(rarray))

    print("completed")
    # Here indicating if the response is filtered
    if completion['choices'][0]['finish_reason'] == "content_filter":
        print("The generated content is filtered.")
except:
    print("An exception has occurred. \n")
    print("Error Message:", completion['error']['message'])
