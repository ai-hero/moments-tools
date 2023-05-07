# Used for local development
build:
	docker build .

run: 
	docker compose up --remove-orphans --build run 

test: 
	docker compose run --build test 

docker:
	docker build . -t registry.gitlab.com/shri_javadekar/scratch/llmhackathon-server:latest

docker-push: docker
	docker push registry.gitlab.com/shri_javadekar/scratch/llmhackathon-server:latest
