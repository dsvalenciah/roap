FROM nginx:alpine
COPY nginx-site.conf /etc/nginx/conf.d/default.conf
RUN mkdir /app
ADD ./build /app/ui
