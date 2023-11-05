#!/bin/bash


usage() { 
    echo "Usage: $0 
    [-w for web] 
    [-a for api] 
    [-n for api-nestjs]
    [-p for push image to docker hub]" 1>&2; exit 1; 
}


while getopts "wanp" option; do
  case $option in
    w)
      deploy_web=true
      ;;
    a)
      deploy_api=true
      ;;
    n)
      deploy_api_nestjs=true
      ;;
    p)
      push_image=true
      ;;
    *)
      usage
      ;;
  esac
done

if [ -z "${deploy_web}" ] && [ -z "${deploy_api}" ] && [ -z "${deploy_api_nestjs}" ]; then
    usage
fi


if [ $deploy_api ]; then 
    cd api \
    && docker buildx build -f Dockerfile -t acelectic/steal-manga:api . \
    && cd ..

    if [ $push_image ]; then docker push acelectic/steal-manga:api 
    fi

    docker-compose stop api \
    && docker-compose up -d --force-recreate api
fi

if [ $deploy_web ]; then 
    cd web \
    && docker buildx build -f Dockerfile -t acelectic/steal-manga:web . \
    && cd ..

    if [ $push_image ]; then docker push acelectic/steal-manga:web 
    fi

    docker-compose stop web \
    && docker-compose up -d --force-recreate web
fi

if [ $deploy_api_nestjs ]; then 
    cd api-nestjs \
    && docker buildx build -f Dockerfile -t acelectic/steal-manga:api-nestjs . \
    && cd ..

    if [ $push_image ]; then
     push acelectic/steal-manga:api-nestjs 
    fi

    docker-compose stop api_nestjs \
    && docker-compose up -d --force-recreate api_nestjs
fi



