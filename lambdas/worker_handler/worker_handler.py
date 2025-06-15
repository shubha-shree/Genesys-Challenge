import json, logging

def lambda_handler(event, context):
    for record in event["Records"]:
        body = json.loads(record["body"])
        job_id = body["job_id"]
        content = body["content"]
        print(f"Processing job: {job_id} -> content: {content}")
