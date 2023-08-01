import json
import requests

from loguru import logger


def lambda_handler(event=dict(), context=dict()):
    # Cross Origin Resource Share (CORS) headers
    headers = {
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        "Content-Type": "application/json"
    }

    logger.debug(f"Event: {event}")
    variable_1 = event["key1"]
    variable_2 = event["key2"]

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
# lambda_response = lambda_handler(event=json.dumps(payload))
# print(f"Lambda response {type(lambda_response)}: {lambda_response}")
