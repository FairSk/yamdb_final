FROM python:3.7-slim
WORKDIR mkdir /app
COPY /api_yamdb/requirements.txt /app/api_yamdb
RUN pip3 install -r /app/api_yamdb/requirements.txt
WORKDIR /app/api_yamdb/
CMD python manage.py runserver 0:8000