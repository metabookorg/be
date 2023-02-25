# build image
docker build -t metabook .
# build container
docker run --rm -p 1312:1312 -e HOST=0.0.0.0 --name=metabook_app metabook