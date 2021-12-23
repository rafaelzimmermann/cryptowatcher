FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:1.21.4
RUN rm /etc/nginx/conf.d/default.conf
COPY --from=build-stage /app/dist /usr/share/nginx/public
COPY nginx/nginx.conf /etc/nginx/conf.d