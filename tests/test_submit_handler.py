import json, base64
import sys
import os
import submit_handler

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../lambdas/submit_handler')))

def test_auth_success():
    auth = base64.b64encode(b"admin:secret").decode()
    event = {
        "headers": { "Authorization": f"Basic {auth}" },
        "body": json.dumps({ "content": "test payload" })
    }
    response = submit_handler.lambda_handler(event, None)
    assert response["statusCode"] == 200
    assert "job_id" in json.loads(response["body"])

def test_auth_failure():
    auth = base64.b64encode(b"bad:creds").decode()
    event = {
        "headers": { "Authorization": f"Basic {auth}" },
        "body": json.dumps({ "content": "test payload" })
    }
    response = submit_handler.lambda_handler(event, None)
    assert response["statusCode"] == 401
