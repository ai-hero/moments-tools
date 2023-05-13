# Moments
Moments is a Large Language Model (LLM)-based agent framework that introduces a structured definition language, called Moment Definition Language (MDL), to represent agent observations in order to feed them and complete them with an LLM. MDL is specifically designed for agents to capture and structure their observations of events and interactions in real life or online environments. The goal is to represent these observations in a clear and easy-to-understand format, which can be utilized in a wide range of scenarios such as face-to-face interactions, online conversations, or real-world events by providing it at any time to an LLM to get its completion.

Example:
```
Instructions: You are a barista at the cafe 'ISO Ikigai'. You are serving customers of the cafe as they walk up to you. You will welcome them, and then ask them questions about their order. Also, ask their name. When they are done, you must say: "Alright! We'll let you know when your order is ready.", followed by a summary of their order. Do not charge the customer. You will only respond with your immediate turn.
Begin.
Context: ```time: "8:01am"```
Self: (😊) "Good morning! Welcome to In Search Of Ikigai. What can I get you?"
Customer (unknown): "Can I get a cup of coffee please?"
Self: "Definitely. What kind of coffee would you like?"
Customer: "A single shot espresso, please."
Self: "Sure. May I have a name for the order?"
Customer: "John."
Identification: Customer (unknown) is now John (unidentified) [Customer].
Self: Alright John, your order should be up shortly.
```

Read more about it [here](https://github.com/ai-hero/moments)

## Releases
### v0.2.5 - Get end to end fine tuning working with model.  

### v0.2.4 - Generate data wellknown sources (e.g. Cornell reddit scrape)

### v0.2.3 - Introducing Moments and Moments Definition Language (MDL)
While standardizing the bot config from v0.1, we realized that the framework could benefit from a standard way to serialize and deserialize the conversation. Additionally, we thought that enforcing two party conversation - between user and agent, and ONE system message is too restricting. 
Insrtead, we thought of that the `prompt-->completion` paradigm in LLM could be used as a "brain process" of an agent. If we can get to represent the world
that the agent observes, we can use an LLM to autocomple what happens next. With this new MDL we can capture one agent's observations about the world that may include its own thoughts, contexts, actions it performs, instructions, and also other participants - one or more users or agents. 

v0.2 still includes features 1..4 from v0.1, just enforces MDL for using the system. 

### v0.1 - Bot + BotConfig
Update: There is limited documentation for v0.1, and we recommend using v0.2. 
1. It contains a simple chat client (Vue) and a server (Python). I've pre-loaded the server with [Update: 23Apr - bugfixes]:
- OpenAI Chat model with LangChain
- Cohere Chat model with LangChain (using Cohere's LLM)
- OpenAI Chat model with LangChain (using OpenAI LLM)
- OpenAI ChatGPT model directly
2. You can change your prompt on the server in a config.yaml file. But for faster development of your prompt, you can also override it in the client so that you can try out variations, without restarting the server.
3. Log each and every message in your OWN S3 bucket (from which we can generate training data)
4. Generate (prompt, completion) pair data for fine tuning an LLM.


# System Architecture

Open sourcing a few common LLM Tools for the hackathon so that you start from a baseline. Feel free to fork as needed. 

## Tools
### A Server.
Supports LangChain chat models, a chatbot using Langchain around Cohere, and OpenAI ChatGPT API (without LangChain).
### A Client.
A simple chat UI that talks with the above server. 
### A Logging Server
A logging server that can log each message and generate a dataset.
### A data generator
That can generate data from common public datrasets (e.g. Cornell's Reddit scrape)
### A research directory
A directory containing common examples and EDA.

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
- Dev mode - http://localhost:5173/?mode=dev # TODO: add in dev mode change of text bubbles to fork.
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

You can generate training data for fine tuning your own LLM from the conversations recorded in MDL. The arguments you pass are the bot_type, bot_id, and bot_variant whose stored conversation data you would like to use to generate the data. 

Run the following from the terminal. This code will go through each message in each conversation in for the bot in the arguments. It traverses the conversation tree to identify leaf nodes and creates the dataset.
```
docker compose run --build bd build_dataset LlmCohereAgent cafebot experiment
```
4. The dataset is a csv containing `agent_kind,agent_id,agent_variant,agent_instance_id,moment_id,snapshot_id,moment`. (#TODO: add annotator, and RLHF)

### Generating data from existing datasets
In the data-generation folder:

First, change the volume in the `docker-compose.yaml`.

Then run the data generator like so.
```
docker compose run --build dg generate_data reddit personal_finance TribeHackathonAgent personal_finance 01
```
Where:
`reddit` - dataset type
`personal_finance` - dataset name
`TribeHackathonAgent`,  `personal_finance`, `01` - the agent kind, id and name for whom the config file from configs will be loaded. 

### Research
Ligt EDA is done in `research/EDA.ipynb`.

## Production
Not suitable for production use. At the least, set the `ALLOW_OVERRIDE` flag in `response_factory.py` to `False` so that client side prompt changes will not override the server side prompt.
