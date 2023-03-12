FROM python:3.8

ARG PROJECT_DIRNAME=codes

RUN mkdir /${PROJECT_DIRNAME}
WORKDIR /${PROJECT_DIRNAME}

COPY . /${PROJECT_DIRNAME}

RUN pip3 install --no-cache-dir -r requirements.txt -i https://pypi.douban.com/simple/

CMD sh docker-entrypoint.sh
