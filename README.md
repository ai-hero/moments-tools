# Starter-kit for the TribeAI LLM Hackathon

Open sourcing a few common LLM Tools for the hackathon so that you start from a baseline. Feel free to fork as needed. 

## Tools
### A Server.
Supports LangChain chat models, a chatbot using Langchain around Cohere, and OpenAI ChatGPT API (without LangChain).
### A Client.
A simple chat UI that talks with the above server. 
### A Logging Server
A logging server that can log each message and generate a dataset.

## Getting Started
- Make sure you have Docker+Docker Compose installed and running (e.g. you'll see the whale icon on the top right of your Mac).

### Creating a network so services can talk to each other
```
docker network create llm-tools
```

### Starting the Chat Server
- Go inside the `serve/` folder.
- You need to create an `.env` file here, and add your API Keys (the ones you want to use):
```
OPENAI_API_KEY=<<YOUR_OPENAI_API_KEY>>
COHERE_API_KEY=<<YOUR_COHERE_API_KEY>>
```
- Start the server:
```
make run
```
- The server will come up at http://localhost:8080
- To change the default cafe example to something else, copy a config from the `configs` folder and rename it to `{bot_type}-{bot_id}-{bot-variant}.yaml`. Then, change the `bot_type`, `bot_id`, and `bot_variant` fields in the config. Change the other fields as needed.


### Starting the Client
- Make sure you have node and npm installed.
- Go inside the `ui/` folder and first install dependencies
```
npm i
```
- Then start the dev server
```
npm run dev
```
- The server will come up at http://localhost:5173
- For fast iteration, we allow you to dynamically change the prompt client side. This allows you to change the prompt config from a constant in the `ChatUI.vue` file. As soon as you save the file (+ reload) we override the config from the server in each interaction and use the one that the client sent instead. Then, change the `bot_type`, `bot_id`, and `bot_variant` fields in the config. Change the other fields as needed.
- Don't forget to update your server side prompt and set `ALLOW_OVERRIDE` flag in  `response_factory.py` to `False` after development. 

### Starting the Logger
- Go inside the `logger/` folder.
- You need to create an `.env` file here, and add your API Keys (the ones you want to use):
```
S3_URL=s3.amazonaws.com
S3_SECURE=true
S3_REGION_NAME=us-east-1
S3_ACCESS_KEY=<<S3_ACCESS_KEY>>
S3_SECRET_KEY=<<S3_SECRET_KEY>>
DATA_BUCKET=llm-tools-data
```
Change these values as you see fit. Make sure the bucket exists in AWS.

- Start the server:
```
make run
```
- The server will come up at http://localhost:8081

### Generating training data from the logger
As a server, the logger records each conversation message that the server sends to it. 

You can generate training data for fine tuning your own LLM from the conversations recorded. The arguments you pass are the bot_type, bot_id, and bot_variant whose stored conversation data you would like to use to generate the data.

1. Make sure you change the `app/helpers/configs/dataset_generator.yaml` with instructions, etc. for your target bot config.
2. Make sure you change bot_config.py to generate the write text serialization.  (#TODO: make a class for each bot)
3. Then run the following from the terminal. This code will go through each message in each conversation in for the bot in the arguments. It traverses the conversation tree to identify leaf nodes and creates the dataset.
```
docker compose run --build bd build_dataset chatopenai cafe experiment
```
4. The dataset is a csv containing `conversation_id, message_id, conversation`. (#TODO: add annotator, and RLHF)

## Production
Not suitable for production use. At the least, set the `ALLOW_OVERRIDE` flag in `response_factory.py` to `False` so that client side prompt changes will not override the server side prompt.
