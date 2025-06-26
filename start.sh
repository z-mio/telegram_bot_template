CONTAINER_NAME=tg-bot-template  # bot 容器名称
docker build -t $CONTAINER_NAME .
docker rm -f $CONTAINER_NAME || true
docker run -d  --restart=always --name $CONTAINER_NAME $CONTAINER_NAME
docker logs -f $CONTAINER_NAME
