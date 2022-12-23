FROM public.ecr.aws/docker/library/ubuntu:latest
# FROM public.ecr.aws/ubuntu/ubuntu:22.04

RUN apt-get update
RUN apt-get install -y \
    python3 \
    python3-pip

ARG FUNCTION_DIR="/home/app/"

RUN mkdir -p ${FUNCTION_DIR}

COPY ./handler/requirements.txt ${FUNCTION_DIR}
RUN pip3 install -r ${FUNCTION_DIR}/requirements.txt

# Copy function code
COPY ./handler/app.py ${FUNCTION_DIR}

# Install Lambda Runtime Interface Client for Python
RUN python3 -m pip install awslambdaric --target ${FUNCTION_DIR}

WORKDIR ${FUNCTION_DIR}

# (Optional) Add Lambda Runtime Interface Emulator and use a script in the ENTRYPOINT for simpler local runs
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
COPY entrypoint.sh /
RUN chmod 755 /usr/bin/aws-lambda-rie /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

CMD [ "app.lambda_handler" ]
