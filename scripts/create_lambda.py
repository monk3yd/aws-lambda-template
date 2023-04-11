### Create Lambda using boto3

import boto3
import json
import os

from loguru import logger


# ------------- AWS Settings ----------------

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Determines the source from where the lambda function will take its code and dependencies
# local : uploads source zip file from local system when creating lambda
# s3 : use prestored source zip file within S3  # test 200OK
# ecr : use docker image saved within ECR repository
WORKFLOW: str = "ecr"

LAMBDA_NAME = "lambda-template"
LAMBDA_RUNTIME = "python3.11"
LAMBDA_HANDLER = "handler.app"
LAMBDA_TIMEOUT = 300  # 5min


# ======================================


def main():
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="us-east-1",
    )

    iam_client = session.client("iam")
    lambda_client = session.client("lambda")

    # Import IAM role for basic lambda execution
    role = iam_client.get_role(RoleName="LambdaBasicExecution")

    if WORKFLOW == "local":
        # Upload directly zip code and dependencies
        with open("lambda.zip", "rb") as file:
            zipped_code = file.read()

        # upload zip file stored locally when creating lambda
        workflow_config = {"Code": {"ZipFile": zipped_code}, "PackageType": "Zip"}

    if WORKFLOW == "s3":
        # use zip file stored in S3 when creating lambda
        workflow_config = {
            "Code": {
                "S3Bucket": "roilab",
                "S3Key": "source/spider-api-manager-lambda.zip",
            },
            "PackageType": "Zip",
        }

    if WORKFLOW == "ecr":
        # use ECR docker image for building container for lambda function
        uri = ""
        workflow_config = {"Code": {"ImageUri": uri}, "PackageType": "Image"}

    basic_config = {
        "FunctionName": LAMBDA_NAME,
        "Runtime": LAMBDA_RUNTIME,
        "Role": role["Role"]["Arn"],
        "Handler": LAMBDA_HANDLER,
        "Timeout": LAMBDA_TIMEOUT,  # Maximum allowable timeout
        # Set up Lambda function environment variables
        # "Environment": {
        #     "Variables": {"Name": "helloWorldLambda", "Environment": "prod"}
        # },
    }

    # Merge
    lambda_configuration = basic_config | workflow_config

    response = lambda_client.create_function(**lambda_configuration)
    logger.info(f"Lambda creation response: {response}")

    with open("data/lambda.json", "w") as file:
        file.write(json.dumps(response))


if __name__ == "__main__":
    main()


## References
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/create_function.html
# https://hands-on.cloud/boto3-lambda-tutorial/
# https://stackoverflow.com/questions/67710230/how-to-deploy-aws-lambda-with-boto3-and-docker
