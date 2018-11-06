FROM python:3.5

COPY ./requirements.txt /tmp/r.txt
RUN pip install -r /tmp/r.txt

CMD ["python"]
