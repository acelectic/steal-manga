cd api \
&& docker buildx build -f Dockerfile -t acelectic/steal-manga:api . \
&& docker push acelectic/steal-manga:api \
&& cd ..

# koyeb service resume api/steal-manga-api 
# koyeb service redeploy api/steal-manga-api 


