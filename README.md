# Dinner Bell

Get notified when a deployment reaches a Ready state. 

## Usage
Create Namespace
```
kubectl create namespace dinner-bell
```
Create Secret with SLACK_TOKEN
```
kubectl create secret generic -n dinner-bell dinner-bell --from-literal=SLACK_TOKEN=$SLACK_TOKEN
```
Create the Deployment
```
kubectl apply -f deploy/
```

Now just add the `dinner-bell.io/slack-channel` annotation to any deployment you want to be notified about 
```
...
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: awesome-app
  annotations:
    dinner-bell.io/slack-channel: devoops
...
```

# Optional annotations:

| Annotation                    | Description                                       | Example                         |
|-------------------------------|---------------------------------------------------|---------------------------------|
| dinner-bell.io/custom-message | Append a custom message to the default message    | Visit Me at https://foo.bar.baz |
| dinner-bell.io/slack-channel  | Channel to send messagees to. bot must be invited | general                         |
|                               |                                                   |                                 |

# Environment Variables

| Variable                      | Description                                       | Default      | Required         |
|-------------------------------|---------------------------------------------------|--------------|------------------|
| SLACK_TOKEN                   |  Slack Bot Token                                  |  None        | Yes              |
| TIMEOUT_SECONDS               |  How long to wait for a deployment to be healthy  |  90          | No               |
| SLACK_USERNAME                |  Username to masquerade as                        |  dinner-bell | No               |