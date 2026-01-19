FROM public.ecr.aws/lambda/python:3.11

# Install build dependencies for C-extensions (like pyswisseph)
RUN yum -y install gcc gcc-c++ make

# Copy requirements.txt
COPY src/requirements.txt ${LAMBDA_TASK_ROOT}

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy handler code
COPY src/handler.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "handler.lambda_handler" ]
