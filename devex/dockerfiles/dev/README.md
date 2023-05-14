# Using a container with pytorch.
First, run the server with port forwarding.
```
kubectl port-forward svc/devbox 8022:22
```

Then ssh into it with user `user` and password `password`.
```
ssh user@localhost -p 8022
```

OR SSH into it with VSCode.

# Build and Push
```
docker build -t rparundekar/devex-pytorch2 -f Dockerfile.pytorch .
docker push rparundekar/devex-pytorch2:latest
```


