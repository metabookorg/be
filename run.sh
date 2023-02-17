# build image
docker build -t metabook .
# build container
docker run --rm -p 1312:1312 --name=metabook_app metabook