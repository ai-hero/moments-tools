# Used for local development
build:
	docker build .

run: 
	HF_MODEL=${HF_MODEL} docker compose up --build run 

test: 
	HF_MODEL=${HF_MODEL} docker compose run --build test 