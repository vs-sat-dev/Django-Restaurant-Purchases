FROM python:3.10.4-alpine
WORKDIR /usr/src/app
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt
COPY entrypoint.sh ./
ENTRYPOINT ["sh", "entrypoint.sh"]