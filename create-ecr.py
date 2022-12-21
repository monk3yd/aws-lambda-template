import boto3
import json

# --- AWS ---
ACCOUNT_ID = "963485456147"
REGION_NAME = "us-east-1"
ecr_repository_name = "lambda_template_container"

# Create an ECR client
client = boto3.client("ecr", region_name=REGION_NAME)

# Create ECR repository
response = client.create_repository(repositoryName=ecr_repository_name)
repository = response["repository"]

# Convert datetime into str
repository["createdAt"] = repository["createdAt"].strftime("%m/%d/%Y, %H:%M:%S")

# Save repository data
with open("ecr_repo_data.json", "w") as file:
    file.write(json.dumps(repository, indent=4))
