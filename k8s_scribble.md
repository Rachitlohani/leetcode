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
1.Runs a set of identical pods
*Monitors the state of each pod, updating as necessary
*Good for dev
*Good for production
*And I would agree with other answers, forget about Pods and just use Deployment. Why? Look at the second bullet point, it monitors the state of each pod, updating as necessary.

So, instead of struggling with error messages such as this one:

`Forbidden: pod updates may not change fields other than spec.containers[*].image`
