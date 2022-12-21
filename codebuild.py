# Prepare Codebuild for Codepipeline

import boto3


def main():
    # Instantiate codebuild client
    client = boto3.client("codebuild", region_name=AWS_REGION_NAME)

    # Codebuild configurations
    github_repo_url = "https://github.com/monk3yd/aws-lambda-template.git" 
    repo_name = github_repo_url.split("/")[-1].split(".")[0]

    source = {
        "type": "GITHUB",
        "location": github_repo_url,
        "gitCloneDepth": 1,
        "gitSubmodulesConfig": {"fetchSubmodules": False},
        "reportBuildStatus": True,
        "sourceIdentifier": f"{repo_name}_github_source",
    }

    artifacts = {
        "type": "NO_ARTIFACTS",
        "overrideArtifactName": False,
        "artifactIdentifier": f"{repo_name}_artifact",
    }

    cache = {
        "type": "LOCAL",
        "modes": ["LOCAL_DOCKER_LAYER_CACHE", "LOCAL_SOURCE_CACHE"],
    }

    environment = {
        "type": "LINUX_CONTAINER",
        "image": "aws/codebuild/standard:6.0",
        "computeType": "BUILD_GENERAL1_SMALL",
        # "environmentVariables": [
        #     {
        #         "name": "string",
        #         "value": "string",
        #         "type": "PLAINTEXT"|"PARAMETER_STORE"|"SECRETS_MANAGER"
        #     },
        # ],
        "privilegedMode": True,
    }

    codebuild_rol = "arn:aws:iam::963485456147:policy/CodebuildCICD"

    logs = {
        "cloudWatchLogs": {
            "status": "ENABLED",
            "groupName": f"{repo_name}_log_group",
            # "streamName": "deploy_cicd_test_flow"
        },
        "s3Logs": {
            "status": "DISABLED",
            "encryptionDisabled": False,
            "bucketOwnerAccess": "NONE",
        },
    }

    build_project_name = f"{repo_name}_build"
    description = "codebuild project - build docker container" 
    source_version = "main"

    # Create codebuild project
    try:
        response = client.create_project(
            name=build_project_name,
            description=description,
            source=source,
            sourceVersion=source_version,
            artifacts=artifacts,
            cache=cache,
            environment=environment,
            serviceRole=codebuild_rol,
            timeoutInMinutes=60,
            queuedTimeoutInMinutes=120,
            badgeEnabled=False,
            logsConfig=logs,
        )
        print(response)

    # Start new (docker) build
    except client.exceptions.ResourceAlreadyExistsException:
        # if args.codebuild:
        response = client.start_build(
            projectName=build_project_name,
            sourceVersion=source_version,
        )

        # Print the build ID
        print(response["build"]["id"])


if __name__ == "__main__":
    main()
