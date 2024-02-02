import os
import requests
import socket
import dotenv

from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.utilities import BingSearchAPIWrapper
from langchain.agents import load_tools
from langchain.chains import RetrievalQA
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.utilities import TextRequestsWrapper

dotenv.load_dotenv()

##############################################
# liang wang, 20240118, 2.0 version, windows only
# Setting up the deployment name

os.environ["BING_SUBSCRIPTION_KEY"] = "<xxx>"
os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"

os.environ["OPENAI_API_KEY"] = "<xxx>"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://<xxx>.openai.azure.com"
os.environ["OPENAI_API_VERSION"] = "2023-05-15"

deployment = "gpt35"
# The base URL for your Azure OpenAI resource. e.g. "https://<your resource name>.openai.azure.com"
endpoint = "https://<xxx>.openai.azure.com"
# The API key for your Azure OpenAI resource.
api_key = "<xxx>"
##############################################

print("\n### Start ###")
print("\n### IP informations ###")

localhost = socket.gethostname()
ip = socket.gethostbyname(localhost)
pubip = requests.get('https://ifconfig.me')

print(localhost,"Private IP:", ip, "Public IP:", pubip.text, "\n")

print ("<xxx>.openai.azure.com", socket.gethostbyname("<xxx>.openai.azure.com"))
print ("<xxx>.blob.core.windows.net", socket.gethostbyname("<xxx>.blob.core.windows.net"))
print ("api.bing.microsoft.com", socket.gethostbyname("api.bing.microsoft.com"))


print("\n### Description  ###")
print("This app will help you to lookup the internal laptop price by using latest exchange rate.")
productname="laptop3"

print(f"User input, productname: {productname}")

search = BingSearchAPIWrapper(k=1)
strsearchre = search.results("us yen rate",1)

print("\n### Bing Search result for 'us yen rate'  ###")

print (f"{strsearchre}\n")

print("\n### ChatOpenAI summarize the bing search result into simple format  ###")

chat = AzureChatOpenAI(
    openai_api_version="2023-05-15",
    azure_deployment="gpt35",
)
prompt = PromptTemplate(
    input_variables=["exchangedata"],
    template="regarding to this {exchangedata}, what is the current exchange rate for us dollar and japanese yen? please provide the output in this format: 1 us dollar  = 100 yen",
)
chain1 = LLMChain(llm=chat, prompt=prompt,verbose=True)
strexchangeresult=chain1.predict(exchangedata=strsearchre)

print (f"llmreply: {strexchangeresult}\n")

print("\n### Internal Document with product price information (chunked)  ###")

requests_tools = load_tools(["requests_all"])
requests = TextRequestsWrapper()

strinternaldata = requests.get("https://<xxx>")

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=100,
    chunk_overlap=10
)
texts = text_splitter.split_text(strinternaldata)


print (f"{texts}\n")

print("\n### qachain answer the japanese price by refering to the exchange data from ChatOpenAI output and the internal product database  ###")
strqapropmt=f"this is current exchange rate for us dollar and japanese yen: {strexchangeresult}, what is the internal employee price for {productname} in japanese yen, what is the percentage of discount when compared with normal price"

dosearch = FAISS.from_texts(
    texts=texts, 
    embedding=AzureOpenAIEmbeddings(azure_deployment="ada2", openai_api_version="2023-05-15"),
)

qa_chain = RetrievalQA.from_chain_type(
    chain_type="stuff",
    llm=chat,
    retriever=dosearch.as_retriever(),
)

print (f"propmt: {strqapropmt}\n")
print("llmreply:", qa_chain.run(f"{strqapropmt}\n"))

print("\n### end ###\n")
