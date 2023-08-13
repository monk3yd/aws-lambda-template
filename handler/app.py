import json
import requests

from loguru import logger

# Cross Origin Resource Share (CORS) headers
CORS = {
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
    "Content-Type": "application/json"
}

def lambda_handler(event=dict(), context=dict()):
    logger.debug(f"Event: {event}")

    variable_1 = event["key1"]
    variable_2 = event["key2"]

    try:
        ip = requests.get("http://checkip.amazonaws.com/")
    except requests.RequestException as error:
        # Send some context about this error to Lambda Logs
        logger.error(error)

        raise error

    # 200OK lambda response
    return {
        "statusCode": 200,
        "headers": CORS,
        "body": json.dumps({
            "message": "hello world",
            "location": ip.text.replace("\n", "")
        }),
    }


# --- Local ---
# if __name__ == "__main__":
#     payload = {
#         "key1": "value1",
#         "key2": "value2"
#     }
    # lambda_response = lambda_handler(event=json.dumps(payload))
    # lambda_response = lambda_handler(event=payload)
    # logger.info(f"Lambda response {type(lambda_response)}: {lambda_response}")
