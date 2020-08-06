FROM python:3.8-buster

WORKDIR /be

ADD ./app /be

RUN pip install uwsgi
RUN pip install -r requirements.txt;

CMD ["uwsgi", "uwsgi.ini"]