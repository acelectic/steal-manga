#!/usr/bin/env bash
source ./bash-flag-script.sh

cd api \
&& docker buildx build -f Dockerfile -t acelectic/steal-manga:api . \
&& cd ..


if [ $push_image ]:
then 
echo "push_image: $push_image"
docker push acelectic/steal-manga:api
fi


if [ $deploy_service ]:
then 
echo "deploy_service: $deploy_service"
docker compose stop api \
    && docker compose up -d --force-recreate api
fi

# && koyeb service redeploy steal-manga-web/api \
