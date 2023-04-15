FROM python:3.7-slim
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r /app/api_yamdb/requirements.txt --no-cache-dir
COPY ./ /app
CMD python manage.py runserver 0:8000