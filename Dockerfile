FROM public.ecr.aws/lambda/python:3.8

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
RUN yum update && \
    yum install -y git

COPY lambda.py ${LAMBDA_TASK_ROOT}
COPY engineer engineer
COPY aws aws

CMD [ "lambda.execute" ]