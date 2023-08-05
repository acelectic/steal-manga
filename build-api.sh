cd api \
&& docker buildx build -f Dockerfile.api.prod -t acelectic/steal-manga:api . \
&& docker push acelectic/steal-manga:api \
&& koyeb service redeploy steal-manga-web/api \
&& cd ..