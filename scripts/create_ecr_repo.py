# Choose the AWS region and pick a name for the ECR repository

import boto3
import json

from loguru import logger


def main():
    # --- AWS ---
    REGION_NAME = "us-east-1"
    ECR_NAME = "lambda-template"  # Use project name

    # Create an ECR client
    client = boto3.client("ecr", region_name=REGION_NAME)

    # Create ECR repository
    response = client.create_repository(repositoryName=ECR_NAME)
    repository = response["repository"]

    # Convert datetime into str
    repository["createdAt"] = repository["createdAt"].strftime("%m/%d/%Y, %H:%M:%S")

    print(repository)

    # Save repository data
    with open("scripts/data/ecr_repo.json", "w") as file:
        file.write(json.dumps(repository, indent=4))


if __name__ == "__main__":
    main()
