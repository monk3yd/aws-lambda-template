#!/bin/bash

### Create ECR repository in AWS.

# Variables
ACCOUNT_ID="134284459147"
REGION_NAME="us-east-1"
ECR_NAME="github-to-lambda"  # Use project name

# Login
aws ecr get-login-password --region ${REGION_NAME} | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${REGION_NAME}.amazonaws.com

# Create ECR (Elastic Container Registry)
aws ecr create-repository  --region ${REGION_NAME} --repository-name ${ECR_NAME} --image-tag-mutability MUTABLE --image-scanning-configuration scanOnPush=false
