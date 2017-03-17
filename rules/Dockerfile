FROM ubuntu:14.04

RUN apt-get -qq update

RUN apt-get install -y -qq python3 python3-pip
RUN pip3 install uwsgi
RUN mkdir /etc/uwsgi
COPY ./config/uwsgi.ini /etc/uwsgi

COPY ./api/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

RUN apt-get install -y -qq nginx
RUN rm /etc/nginx/nginx.conf
COPY ./config/nginx.conf etc/nginx/nginx.conf
RUN useradd -ms /bin/bash nginx

RUN apt-get install -y -qq supervisor
RUN rm /etc/supervisor/supervisord.conf
COPY ./config/supervisor /etc/supervisor

EXPOSE 80
CMD ["/usr/bin/supervisord"]
