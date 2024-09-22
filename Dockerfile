FROM python:3.9.1

RUN pip install pandas gspread oauth2client sqlalchemy psycopg2

WORKDIR /app 
COPY . /app

ENTRYPOINT [ "python", "/app/main.py" ]