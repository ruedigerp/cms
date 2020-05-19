# FROM nginx:alpine
# COPY . /usr/share/nginx/html/

FROM cms-core:1.1
COPY . /app
WORKDIR /app
ENTRYPOINT ["python3"]
CMD ["app.py"]
