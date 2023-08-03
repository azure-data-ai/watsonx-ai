

import os
from dotenv import load_dotenv

from genai.model import Credentials, Model
from genai.schemas import GenerateParams

load_dotenv()

my_api_key = os.getenv('GENAI_KEY', None)
my_api_endpoint = os.getenv('GENAI_API', None)

creds = Credentials(api_key=my_api_key, api_endpoint=my_api_endpoint)

# print(cred)

# Instantiate the GENAI Proxy Object
params = GenerateParams(
    decoding_method="sample",
    max_new_tokens=10,
    min_new_tokens=1,
    stream=False,
    temperature=0.7,
    top_k=50,
    top_p=1,
)

# model object
model = Model("google/flan-ul2", params=params, credentials=creds)

### -- Async Example ----------#########        
# greeting = "Hello! How are you?"
# lots_of_greetings = [greeting] * 1000
# num_of_greetings = len(lots_of_greetings)
# num_said_greetings = 0
# greeting1 = "Hello! How are you?"

# # yields batch of results that are produced asynchronously and in parallel
# for result in model.generate_async(lots_of_greetings):
#     if result is not None:
#         num_said_greetings += 1
#         print(f"[Progress {str(float(num_said_greetings/num_of_greetings)*100)}%]")
#         print(f"\t {result.input_text} --> {result.generated_text}")



###- Sync Example ########


greeting1 = "Hello! How are you?"
greeting2 = "I am fine and you?"

# Call generate function
responses = model.generate_as_completed([greeting1, greeting2] * 4)
for response in responses:
    print(f"Generated text: {response.generated_text}")

