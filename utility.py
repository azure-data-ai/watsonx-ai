import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from boxsdk import OAuth2, Client
from dotenv import load_dotenv

import requests
import io
import PyPDF2

load_dotenv()

SLACK_TOKEN = os.getenv('SLACK_TOKEN', None)
BOX_CLIENT_ID = os.getenv('BOX_CLIENT_ID', None)
BOX_CLIENT_SECRET = os.getenv('BOX_CLIENT_SECRET', None)
BOX_ACCESS_TOKEN = os.getenv('BOX_ACCESS_TOKEN', None)


# Slack ==
def send_message(msg):
    client = WebClient(token=SLACK_TOKEN)
    client.chat_postMessage(channel="#hackathon", text=msg)


#BOX ===
def get_docs_from_box():
    auth = OAuth2(
        client_id=BOX_CLIENT_ID,
        client_secret=BOX_CLIENT_SECRET,
        access_token=BOX_ACCESS_TOKEN,     # developer token
    ) 
    client = Client(auth)
    # user = client.user().get()  # get user
    # root_folder = client.root_folder().get()   ## get items in root folder
    # items = root_folder.get_items()
    # search_term = 'rfp'  # file part, if common naming convension
    # items = client.search().query(search_term, result_type = 'file', file_extensions=['pdf'])
    ## List the file
    contracts = client.folder(folder_id=219978270295).get_items()
    docs = []
    for item in contracts:
        # print(item.id, item.name, item.type)
        docs.append({'filename': item.name, 'download_url': client.file(item.id).get_download_url()}) #Get download url for pdf
    # url = client.file(1261013162916).get_download_url()
    return docs


def read_pdf_content(url):
    ## To Read from local dir
    # pdfFileObj = open('/Users/rahulsingh/Downloads/Watsonx/Employment Contract_1.pdf', 'rb') #read-binary mode
    # pdfReader = PyPDF2.PdfReader(pdfFileObj)

    ## To read from Box folder
    response = requests.get(url=url)
    streamObj = io.BytesIO(response.content)
    pdfReader = PyPDF2.PdfReader(streamObj)

    # print(len(pdfReader.pages))  # number of pages
    content = ''
    for i in range(0, len(pdfReader.pages)):
        # Iterate page-wise and create page object
        pageObj = pdfReader.pages[i]
        extracted_text = pageObj.extract_text()
        # print(f'page: {i} => {extracted_text}')
        content = content + ' ' + extracted_text
    #extract text
    return content


if __name__ == '__main__':
    docs = get_docs_from_box()
    # print(docs)

     # text = read_pdf_content(url)
    # summary = model.summarize(text)
    # print(f'===>> {text}')
    # Send message
    # send_message(msg=f'Summary: {text}')

    # docs = get_docs_from_box()
    # print(docs[0]['filename'])
    # text = read_pdf_content(docs[0]['download_url'])

    # print(text)