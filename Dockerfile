FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNDUFFERED 1

WORKDIR /my_app

RUN python -m pip install --upgrade pip
COPY ./requirements.txt /my_app/requirements.txt
RUN pip install -r /my_app/requirements.txt
COPY . /my_app

#EXPOSE 8000

#CMD ["python", "manage.py", "migrate"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
