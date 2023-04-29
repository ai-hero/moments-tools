# Used for local development
build:
	docker build .

run: 
	docker compose up --remove-orphans --build run 

test: 
	docker compose run --remove-orphans --build test 

build_dataset: 
	docker compose run --remove-orphans --build bd $(ARGS)
