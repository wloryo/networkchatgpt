
import openai
import socket
import dotenv

dotenv.load_dotenv()

##############################################
# liang wang, 20231213, 2.0 version, windows only
# Setting up the deployment name
deployment = "gpt35"
# The base URL for your Azure OpenAI resource. e.g. "https://<your resource name>.openai.azure.com"
endpoint = "https://<xxx>.openai.azure.com"
# The API key for your Azure OpenAI resource.
api_key = "<xxx>"
##############################################

print ("start")
print ("<xxx>.openai.azure.com", socket.gethostbyname("<xxx>.openai.azure.com"))
print ("<xxx>.search.windows.net", socket.gethostbyname("<xxx>.search.windows.net"))

client = openai.AzureOpenAI(
    base_url=f"{endpoint}/openai/deployments/{deployment}/extensions",
    api_key=api_key,
    api_version="2023-08-01-preview",
)

question = "Cat likes fish, it that true?"
print (question)
completion = client.chat.completions.create(
    model=deployment,
    messages=[
        {
            "role": "user",
            "content": question,
        },
    ],
    extra_body={
        "dataSources": [
            {
                "type": "AzureCognitiveSearch",
                "parameters": {
                    "endpoint": "https://<xxx>.search.windows.net",
                    "key": "<xxx>",
                    "indexName": "openaiowndata-index"
                }
            }
        ]
    }
)
print(f"{completion.choices[0].message.role}: {completion.choices[0].message.content}")