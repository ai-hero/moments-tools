# Used for local development
build:
	docker build --build-arg HF_MODEL=${HF_MODEL} .

run: 
	HF_MODEL=${HF_MODEL} docker compose up --build run 

test: 
	HF_MODEL=${HF_MODEL} docker compose run --build test 