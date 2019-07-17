FROM python:3.6-jessie
WORKDIR /python-app
ADD requirements.txt /python-app/requirements.txt
RUN pip install -r /python-app/requirements.txt
ADD . /python-app
RUN chmod 777 /python-app/main.py
CMD ["python", "main.py"]
