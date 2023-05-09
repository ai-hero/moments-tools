# Used for local development
build:
	docker build .

run: 
	docker compose up --remove-orphans --build run 

test: 
	docker compose run --build test 

docker-push:
	docker buildx build --push --platform linux/amd64 . -t rparundekar/llmhackathon-logger:latest