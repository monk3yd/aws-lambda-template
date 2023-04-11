#!/bin/bash

### Deploy docker image to AWS ECR repository.

# Variables
ACCOUNT_ID="923485256341"
REGION_NAME="us-east-1"
IMAGE_NAME="demo-image"
IMAGE_TAG="main"
# IMAGE_TAG="experimental"

# Login
aws ecr get-login-password --region ${REGION_NAME} | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${REGION_NAME}.amazonaws.com

# Build docker image
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

# Tag docker image to ECR (map)
docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${ACCOUNT_ID}.dkr.ecr.${REGION_NAME}.amazonaws.com/${IMAGE_NAME}:${IMAGE_TAG}

# Push docker image to ECR
docker push ${ACCOUNT_ID}.dkr.ecr.${REGION_NAME}.amazonaws.com/${IMAGE_NAME}:${IMAGE_TAG}

echo ${ACCOUNT_ID}.dkr.ecr.${REGION_NAME}.amazonaws.com/${IMAGE_NAME}:${IMAGE_TAG} > scripts/data/ecr_repo.txt
