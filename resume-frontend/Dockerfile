# Development stage
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --legacy-peer-deps
COPY . .
EXPOSE 3000
ENV VITE_HOST=0.0.0.0
CMD ["npm", "run", "dev"]
