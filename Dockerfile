FROM python:3.7-alpine3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG aws_access_key
ARG aws_secret_access_key

ENV AWS_ACCESS_KEY=$aws_access_key
ENV AWS_SECRET_ACCESS_KEY=$aws_secret_access_key
ENV AWS_DEFAULT_REGION=us-east-1

ENTRYPOINT ["python", "ses-mail.py"]

