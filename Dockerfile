FROM python:3.11.3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt 

RUN pip install --upgrade pip 

RUN pip install psycopg2-binary

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]