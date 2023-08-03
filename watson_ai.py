import os
import requests
from dotenv import load_dotenv
import auth

import test
import utility as util

load_dotenv()

## my_api_key = <YOUR_API_KEY>
my_api_key = os.getenv('API_KEY', None)
project_id = '5be0dcae-7678-4c17-98fb-1e6ed95ecb11'
# project_id = '5be0dcae-7678-4c17-98fb-1e6ed95ecb11'

model_t5 = 'google/flan-t5-xxl'
model_ul2 = 'google/flan-ul2'

def format_input(input_text):
    # input = 'Summarise\n\nInput:\nHello World\n\nOutput:\n'
    input = f'Summarise\n\nInput:\n{input_text}\n\nOutput:\n'
    return input

def send_to_watsonx(access_token, input):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token),
    }

    params = {
        'version': '2023-05-29',
    }

    json_data = {
        'model_id': model_ul2,
        'input': input,
        'parameters': {
            'decoding_method': 'greedy',
            'max_new_tokens': 700,
            'min_new_tokens': 20,
            'stop_sequences': [],
            'repetition_penalty': 1.29,
        },
        'project_id': project_id,
    }
    # try:
    response = requests.post(
        'https://us-south.ml.cloud.ibm.com/ml/v1-beta/generation/text',
        params=params,
        headers=headers,
        json=json_data,
    )
    if response.status_code == 200:
        output_text = response.json()['results'][0]['generated_text'] 
        return output_text
    else:
        print(response.text)
        exit(1)
    # except KeyError: 
    #     return 'ERROR: token_quota_reached'
   
   

if __name__ == '__main__':

    access_token = auth.get_access_token(my_api_key)
    
    ## Command line input
    # text_input = format_input(input('Enter Input text:'))
    
    # Processing Local Text file
    # doc_text = test.get_doc_content()

    ## Processing box file
    docs = util.get_docs_from_box()
    print(f'Processing file: {docs[0]["filename"]} ... ')
    doc_text = util.read_pdf_content(docs[0]['download_url'])
    
    ## Prepare input Prompt
    input_prompt = test.prompt_pattern(doc_text) 

    ## Get Model Output
    # output = send_to_watsonx(access_token=access_token, input=text_input)
    output = send_to_watsonx(access_token=access_token, input=input_prompt)
    print(f'Output: {output}')

    print('Send message to Slack')
    # util.send_message(msg=f'Summary: {output}')

    # print(input_prompt)






