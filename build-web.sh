#!/usr/bin/env bash
source ./bash-flag-script.sh

cd web \
&& docker buildx build -f Dockerfile -t acelectic/steal-manga:web . \
&& cd ..

if [ $push_image ];
then 
echo "push_image: $push_image"
docker push acelectic/steal-manga:web
fi


if [ $deploy_service ];
then 
echo "deploy_service: $deploy_service"
docker-compose stop web \
    && docker-compose up -d --force-recreate web
fi

# && koyeb service redeploy steal-manga-web/web \