#! /bin/bash 


echo "Build Docker Image"
echo "########################################################################"

docker build -t projectx .

echo "Tag Docker Image"
echo "########################################################################"
docker tag projectx:latest registry.heroku.com/sparkling-star/web:latest

echo "Push to repo"
echo "########################################################################"
docker push registry.heroku.com/sparkling-star/web:latest

echo "Push to heroku repo"
echo "########################################################################"
heroku container:push web --app sparkling-star


echo "Release"
echo "########################################################################"
heroku container:release web --app sparkling-star
