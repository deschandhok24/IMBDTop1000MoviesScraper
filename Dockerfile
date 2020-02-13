FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3 python3-dev python3-pip
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENV PYTHONIOENCODING=utf-8
ENTRYPOINT ["python3"]
CMD ["app.py"]
