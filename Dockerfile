FROM python:3.6

WORKDIR /usr/src/basicpaymentapi

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "manage.py runserver" ]