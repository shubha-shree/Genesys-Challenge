import os, json, uuid, base64, boto3

USERNAME = os.environ["BASIC_USER"]
PASSWORD = os.environ["BASIC_PASS"]
QUEUE_URL = os.environ["QUEUE_URL"]

# USERNAME = "admin"
# PASSWORD = "secret"
# QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/302263080337/AsyncJobQueue"

sqs = boto3.client("sqs")

def lambda_handler(event, context):
    auth = event.get("headers", {}).get("Authorization", "")
    if not validate_auth(auth):
        return {"statusCode": 401, "body": "Unauthorized"}

    try:
        body = json.loads(event["body"])
        job_id = str(uuid.uuid4())
        print(f"body: {body}, job_id: {job_id}")
        sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=json.dumps({"job_id": job_id, "content": body["content"]}))
        return {
            "statusCode": 200,
            "body": json.dumps({"job_id": job_id, "status": "queued"})
        }
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}

#Authentication
def validate_auth(auth):
    if not auth.startswith("Basic "): return False
    user_pass = base64.b64decode(auth.split()[1]).decode()
    user, pwd = user_pass.split(":", 1)
    return user == USERNAME and pwd == PASSWORD
