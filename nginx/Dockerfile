FROM nginx

RUN mkdir -p /app/staticfiles

COPY nginx.conf /etc/nginx/nginx.conf

COPY html/ /usr/share/nginx/html/

EXPOSE 8080