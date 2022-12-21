import json
import requests


def lambda_handler(event=dict(), context=dict()):
    # Cross Origin Resource Share (CORS) headers
    headers = {
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        "Content-Type": "application/json"
    }

    # body = json.loads(event["body"])

    try:
        ip = requests.get("http://checkip.amazonaws.com/")
    except requests.RequestException as error:
        # Send some context about this error to Lambda Logs
        print(error)

        raise error

    # 200OK lambda response
    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps({
            "message": "hello world",
            "location": ip.text.replace("\n", "")
        }),
    }


# --- Local ---
# payload = {
#     "key1": "value1",
#     "key2": "value2"
# }
# event = {
#     "body": json.dumps(payload)
# }
# lambda_response = lambda_handler(event=event)
# print(f"Lambda response {type(lambda_response)}: {lambda_response}")
