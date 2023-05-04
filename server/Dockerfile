FROM python:3.11-slim-bullseye

RUN apt-get -y update && apt-get install -y --no-install-recommends build-essential  \
    wget nginx ca-certificates git \
    && pip install --upgrade pip setuptools \ 
    && rm -rf /var/lib/apt/lists/*

# Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.
ENV PYTHONUNBUFFERED=TRUE PYTHONDONTWRITEBYTECODE=TRUE PATH="/home/user/app:${PATH}" PYTHONPATH="/home/user/app:${PYTHONPATH}"

# Add non-root user
RUN groupadd -r user && useradd -r -g user user
RUN chown -R user /var/log/nginx /var/lib/nginx /tmp

# Create User Directory
RUN mkdir /home/user
RUN chown -R user /home/user
WORKDIR /home/user

# Install dependencies
COPY app/requirements.txt requirements.txt
RUN pip install -r requirements.txt    

# Set up the program in the image
COPY app /home/user/app
WORKDIR /home/user/app

# Code check
RUN pylint --disable=R,C ./**/*.py
RUN mypy --no-namespace-packages --ignore-missing-imports .

# Set entrypoint
ENTRYPOINT [ "sh", "./entrypoint" ]

# Port 8080, since we are not running as root user
EXPOSE 8080 

# Switch to non-root user.
USER user