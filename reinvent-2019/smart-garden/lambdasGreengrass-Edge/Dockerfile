FROM python:2.7-slim

WORKDIR /app

#Install git
RUN apt-get update \
    && apt-get install -y git

RUN pip install git+git://github.com/rpedigoni/greengo.git#egg=greengo
RUN pip install awscli

COPY bash/device_buildAndDeploy.sh /app/install.sh
RUN chmod +x /app/install.sh
ENV AWS_DEFAULT_REGION us-east-1
ENV AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY

CMD ["./install.sh"]
