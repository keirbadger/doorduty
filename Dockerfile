FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apk update && apk upgrade && \
    apk add --no-cache bash git

COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app


ENTRYPOINT [ "python", "-m", "doorduty" ]
#CMD [ "python", "__main__.py" ]
#CMD [ "bash" ]
