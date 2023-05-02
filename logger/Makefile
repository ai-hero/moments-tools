# Used for local development
build:
	docker build .

run: 
	docker compose up --remove-orphans --build run 

test: 
	docker compose run --build test 

build_dataset: 
	docker compose run --build bd build_dataset $(ARGS)
