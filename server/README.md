# Chat Server

The repo contains code for a basic container to serve Chat API with OpenAI.

# Serving the model using an HTTP endpoint.

## Pre-requisites

You'll need docker and docker-compose installed on your machine to use this. Also, don't forget to increase the memory and disk space allocated to it from docker preferences.

## Before running, we make sure tests work, run:

```
make test
```

## Running the Server locally while developing

To run the server not without detaching, we run:

```
make run
```

Use `ctrl+c` to stop the container.

### Logs

You can check the logs of the container using:

```
docker logs -f chat_server
```


# Hitting the predict endpoint

Docker compose exposes the container at `http://localhost:8080`.

## Using cURL

To get a prediction we run a cURL request:

```
curl -X POST http://localhost:8080/predict  \
    -H 'Content-Type: application/json'  \
    -d '{"text":"I am feeling great!","labels":["sad", "happy"]}'
```

You will see the JSON response like:

```
{
  "label": "happy",
  "score": 0.9991405010223389
}
```

## Using Python Requests Module

A predict request using the requests module can be made like this:

```
import httpx

...

request_obj = {
  "text": "I am feeling great!",
  "labels": ["sad", "happy"],
}
with httpx.Client(base_url=SERVER_URL) as client:
    resp = client.post("predict", json=request_obj)
    resp.raise_for_status()
    prediction = resp.json() # will be {'label': 'happy', 'score': 0.9991405010223389}

```
