FROM node:alpine
WORKDIR /app

# COPY the package.json file, update any deps and install them
COPY package.json .
RUN npm install

# copy the whole source folder(the dir is relative to the Dockerfile
COPY . .
CMD [ "npm", "run", "start" ]

FROM nginx
EXPOSE 80
COPY --from=builder /app/public /usr/share/nginx/html