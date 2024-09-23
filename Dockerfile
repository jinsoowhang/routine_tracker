FROM python:3.9.1

# Install required Python packages, including python-dotenv
RUN pip install pandas gspread oauth2client sqlalchemy psycopg2 python-dotenv

# Set the working directory
WORKDIR /app

# Copy all the files into the container
COPY . /app

ENTRYPOINT [ "python", "main.py" ]