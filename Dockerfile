FROM python:3.11

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ADD main.py /app/main.py
WORKDIR /workdir
ENTRYPOINT python3 /app/main.py
