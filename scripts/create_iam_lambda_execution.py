### Create IAM Lambda execution role using boto3

import boto3
import json
import os

from loguru import logger


# ------------- AWS Settings ----------------

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# ======================================


def main():

    iam = boto3.client(
        "iam",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="us-east-1",
    )

    role_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole",
            }
        ]
    }

    response = iam.create_role(
        RoleName="LambdaBasicExecution",
        AssumeRolePolicyDocument=json.dumps(role_policy),
    )
    logger.info(f"IAM create role response: {response}")

    # Save role data
    with open("data/iam_role.json", "w") as file:
        file.write(json.dumps(response))


if __name__ == "__main__":
    main()
