# FROM nginx:alpine
# COPY . /usr/share/nginx/html/

FROM python:2.7
RUN mkdir /app
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
# ENTRYPOINT ["python"]
# CMD ["app.py"]
