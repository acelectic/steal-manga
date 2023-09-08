cd web \
&& docker buildx build -f Dockerfile -t acelectic/steal-manga:web . \
&& docker push acelectic/steal-manga:web \
&& cd ..

# && koyeb service redeploy steal-manga-web/web \