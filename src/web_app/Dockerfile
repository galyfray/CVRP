FROM node:16-alpine AS build

WORKDIR /app
COPY ./src/web_app .

RUN npm ci
RUN npm run build

FROM nginx:1.23

COPY --from=build /app/build/ /usr/share/nginx/html
COPY --from=build /app/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
ENTRYPOINT ["nginx", "-g", "daemon off;"]