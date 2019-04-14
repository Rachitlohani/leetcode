### Kubernetes has three Object Types you should know about:

Object|Purpose
---|---
Pods | runs one or more closely related containers
Services | sets up networking in a Kubernetes cluster
Deployment | Maintains a set of identical pods, ensuring that they have the correct config and that the right number of them exist.


### Pods
1.Runs a single set of containers
2.Good for one-off dev purposes
3.Rarely used directly in production

### Deployment
1. Runs a set of identical pods
2. Monitors the state of each pod, updating as necessary
3. Good for dev
4. Good for production

So, instead of struggling with error messages such as the following, just stick with deployment object. 

`Forbidden: pod updates may not change fields other than spec.containers[*].image`
