FROM node:alpine AS build

WORKDIR /client

COPY package*.json .

RUN npm install

COPY . .

RUN npm run build

FROM nginx

COPY --from=build /client/dist /usr/share/nginx/html