FROM node:gallium-alpine3.14
WORKDIR /app
ENV NODE_ENV=production

# copy application files
COPY app .
RUN npm install

CMD node server.js
EXPOSE 8080
