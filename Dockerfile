FROM python:3.10.4-alpine
WORKDIR ./
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requrements.txt