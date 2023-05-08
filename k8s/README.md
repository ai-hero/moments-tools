# Kubernetes object specifications


## Description

This directory contains the Kubernetes yaml specifications for the 3 components that make up this application. The `server`, the `logger` and the `ui`.

Simple way to deploy these in a K8s cluster would be to simply go a components directory and run `kubectl apply -f .`

The `logger` requires AWS access credentials. These should be made available separately as a secret called `aws-credentials`.

The yamls were mainly generated using `kompose`. Some of the components that weren't required were removed and the names of the deployments were modified.