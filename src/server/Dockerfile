FROM python:3.9.15-slim-buster

RUN apt-get update
RUN apt-get install -y libhdf5-dev pkg-config gcc
RUN python -m pip install --upgrade pip

WORKDIR /app
RUN mkdir src
COPY src/cvrp /app/src/cvrp
COPY src/server /app/src/server

COPY requirements.txt .
RUN pip3 install -r requirements.txt

EXPOSE 5000
CMD ["python3", "-m", "src.server.main" ]