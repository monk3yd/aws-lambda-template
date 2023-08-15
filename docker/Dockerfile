# Python Docker Image

# Using an alternative base image (python) with the runtime interface client (awslambdaric)
# https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-instructions

# Define custom function directory
ARG FUNCTION_DIR="/monk3yd/"

FROM python:3.11 as build-image

# Include global arg in this stage of the build
ARG FUNCTION_DIR
RUN mkdir -p ${FUNCTION_DIR}

# create a dedicated group and user
RUN groupadd -r monk3yd && useradd -g monk3yd monk3yd

# set ownership and permissions
RUN chown -R monk3yd:monk3yd ${FUNCTION_DIR}

# change to non-root user (some images already have a generic user)
USER monk3yd

# Copy function code
COPY ./handler/* ${FUNCTION_DIR}

# Install the function's dependencies
RUN pip install \
    --target ${FUNCTION_DIR} \
        awslambdaric

# Use a slim version of the base Python image to reduce the final image size
FROM python:3.11-slim

# Set environment variables
ENV KEY=RFTL
# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

COPY requirements.txt ${FUNCTION_DIR}
RUN pip install -r ${FUNCTION_DIR}/requirements.txt

# Set runtime interface client as default command for the container runtime
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]

# Pass the name of the function handler as an argument to the runtime
CMD [ "main.lambda_handler" ]
