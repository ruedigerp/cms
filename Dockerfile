# FROM nginx:alpine
# COPY . /usr/share/nginx/html/

# FROM python:2.7
FROM cms-core:1.0
COPY . /app
WORKDIR /app
# RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
