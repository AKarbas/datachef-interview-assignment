FROM python:3.8.3

ENV PYTHONUNBUFFERED 1
WORKDIR /webapp

RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
 && chmod +x wait-for-it.sh

COPY ./requirements.pip ./
RUN pip install --no-cache-dir -r requirements.pip

COPY ./ ./
COPY ./webapp/dockerized_settings.py ./webapp/settings.py

ENTRYPOINT ["./entrypoint.sh"]

EXPOSE 8000

