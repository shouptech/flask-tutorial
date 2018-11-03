FROM python:3

ADD . /app/

WORKDIR /app

RUN pip install -e .
RUN pip install waitress

CMD ["waitress-serve", "--call", "flaskr:create_app"]
