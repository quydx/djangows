FROM python:3
MAINTAINER locvu "locvx1234@gmail.com"
ENV PYTHONUNBUFFERD 1
RUN mkdir /code
RUN mkdir /code/db
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
