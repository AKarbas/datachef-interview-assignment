FROM python:3.8.3

ENV PYTHONUNBUFFERED 1
WORKDIR /webapp

COPY ./requirements.pip ./
RUN pip install --no-cache-dir -r requirements.pip

COPY ./ ./

CMD ["./manage.py", "runserver", "0.0.0.0:8000"]

expose 8000

