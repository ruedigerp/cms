# FROM nginx:alpine
# COPY . /usr/share/nginx/html/

FROM python:3.8
RUN mkdir /app
COPY requirements.txt /app/
WORKDIR /app
RUN pip3 install -r requirements.txt
# ENTRYPOINT ["python"]
# CMD ["app.py"]
