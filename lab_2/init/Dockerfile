FROM python:3.12
WORKDIR /init

RUN pip install faker psycopg2-binary

COPY . /init

ENTRYPOINT ["bash", "-c", "python3 upload_script.py"]