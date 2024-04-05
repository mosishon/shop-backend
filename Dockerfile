FROM ubuntu:latest
RUN apt update 
RUN apt install -y python3.10
RUN apt install -y supervisor
RUN apt install -y python3-pip
EXPOSE 8000
RUN mkdir /app
COPY requirements.txt /app
RUN python3 -m pip install --no-cache-dir -r requirements.txt
COPY . /app
WORKDIR /app

CMD ["/usr/bin/supervisord","-c","supervisord.conf"]