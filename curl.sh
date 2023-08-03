curl "https://us-south.ml.cloud.ibm.com/ml/v1-beta/generation/text?version=2023-05-29" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -d $'{
  "model_id": "google/flan-ul2",
  "input": "Hello World",
  "parameters": {
    "decoding_method": "greedy",
    "max_new_tokens": 700,
    "min_new_tokens": 20,
    "stop_sequences": [],
    "repetition_penalty": 1.29
  },
  "project_id": "5be0dcae-7678-4c17-98fb-1e6ed95ecb11"
}'