# Base images 基础镜像
FROM python:3.9
#MAINTAINER 维护者信息
MAINTAINER ranYlra
# 设置语言
ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8
#指定工作目录，若无，则自动创建
WORKDIR /code
# 拷贝requirements.txt
COPY ./requirements.txt /code/requirements.txt
# 更新pip
RUN pip3 install --upgrade pip
# 安装依赖
RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt
# 将项目拷贝出来
COPY ./app /code/app
# 运行
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8090"]
