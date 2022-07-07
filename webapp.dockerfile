FROM node:12-buster as buildWeb
WORKDIR /workspace
COPY webui webui

WORKDIR /workspace/webui
RUN npm install
RUN npm run build:prod

FROM python:3.7

WORKDIR /workspace
COPY webapi webapi

WORKDIR /workspace/webapi
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install --upgrade pip
RUN pip3 install -U setuptools
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY --from=buildWeb /workspace/webui/dist/static static
COPY --from=buildWeb /workspace/webui/dist/index.html static/


EXPOSE 5000

ENTRYPOINT uvicorn app:app --host 0.0.0.0 --port 5000
