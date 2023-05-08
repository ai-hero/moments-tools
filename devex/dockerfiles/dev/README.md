# Using a container with pytorch.
First, run the server with port forwarding.
```
docker run -p 22:22 -it --rm rparundekar/devex-pytorch2:latest 
```

Then ssh into it with user `user` and password `password`.
```
ssh user@localhost
```

OR SSH into it with VSCode.

# Build and Push
```
docker build -t rparundekar/devex-pytorch2 -f Dockerfile.pytorch .
docker push rparundekar/devex-pytorch2:latest
```
