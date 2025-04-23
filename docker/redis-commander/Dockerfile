FROM node:20-alpine

RUN npm install -g redis-commander

EXPOSE 8081

ENTRYPOINT ["sh", "-c"]
CMD ["redis-commander --redis-host=$REDIS_HOST --redis-port=$REDIS_PORT --redis-db=$REDIS_DB"]