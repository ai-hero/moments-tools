# Starter-kit for the TribeAI LLM Hackathon

Open sourcing a few common LLM Tools for the hackathon so that you start from a baseline. Feel free to fork as needed. 

## Tools
### A Server.
Supports LangChain chat models, a chatbot using Langchain around Cohere, and OpenAI ChatGPT API (without LangChain).
### A Client.
A simple chat UI that talks with the above server. 

## Getting Started

### Starting the Server
- Make sure you have Docker installed and running.
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

## Production
Not suitable for production use. At the least, set the `ALLOW_OVERRIDE` flag in `response_factory.py` to `False` so that client side prompt changes will not override the server side prompt.
