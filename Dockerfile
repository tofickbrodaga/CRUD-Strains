FROM python:3.10.13

WORKDIR /CRUD-Strains

COPY app.py .
COPY requirements.txt .

RUN pip install -r requirements.txt