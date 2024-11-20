FROM node:20.11.0 AS build

WORKDIR /client

COPY package*.json .

RUN npm install

COPY . .

RUN npm run build

FROM nginx

COPY --from=build /client/build /usr/share/nginx/html