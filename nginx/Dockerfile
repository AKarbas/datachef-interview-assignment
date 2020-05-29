FROM nginx:1.17.10

RUN rm /etc/nginx/conf.d/default.conf
COPY ./static/ /static_files/
COPY ./webapp.conf /etc/nginx/conf.d/
