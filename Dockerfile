# Base images 基础镜像
FROM python:3.8.13-bullseye
#MAINTAINER 维护者信息
MAINTAINER ranYlra
# 设置语言
ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8
#指定工作目录，若无，则自动创建
WORKDIR /root/app

COPY /requirements/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#EXPOSE 映射端口
EXPOSE 9000 9001
COPY ./app /code/app
CMD ["uvicon","app.main:app","--host","0.0.0.0","--port","80"]
