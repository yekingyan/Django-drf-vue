FROM node:10.13-alpine as builder
WORKDIR /app
ADD . /app
RUN yarn install && yarn run build --prod

FROM nginx:1.15-alpine
WORKDIR /opt/www/html
COPY --from=0 /app/dist /opt/www/html
COPY ./deploy/nginx.conf /etc/nginx
EXPOSE 8080
