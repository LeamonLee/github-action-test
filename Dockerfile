FROM python:3.9-slim

COPY ./src /app/src
COPY ./requirements.txt /app
WORKDIR /app

RUN pip3 --no-cache-dir --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org install -r requirements.txt

WORKDIR /app/src

# 設定時區
ENV TZ=Asia/Taipei
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD ["python", "run.py"]
# ENTRYPOINT /bin/sh