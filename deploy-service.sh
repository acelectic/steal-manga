cd api \
&& docker buildx build -f Dockerfile -t acelectic/steal-manga:api . \
&& docker push acelectic/steal-manga:api \
&& cd ..

docker-compose stop api \
&& docker-compose up -d api

cd web \
&& docker buildx build -f Dockerfile -t acelectic/steal-manga:web . \
&& docker push acelectic/steal-manga:web \
&& cd ..

docker-compose stop web \
&& docker-compose up -d web
