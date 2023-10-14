FROM node:18.18.1-bullseye

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci

COPY . .
