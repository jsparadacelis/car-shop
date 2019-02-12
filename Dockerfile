FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /car_shop
WORKDIR /car_shop
COPY requirements.txt /car_shop/
RUN pip install -r requirements.txt
COPY . /car_shop/