FROM python:3.7

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /app

WORKDIR /app

ENTRYPOINT ["bash", "entrypoint.sh"]
