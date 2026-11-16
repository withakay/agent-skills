# AKS and Kubernetes

Use this source only when the target runs on AKS or Kubernetes and cluster-level evidence can answer a gap left by Azure Monitor.

## Search process

1. Confirm the Azure subscription, AKS cluster, Kubernetes context, namespace, workload, container, and environment before reading data.
2. Prefer Azure Monitor Container Insights when it contains the required history. Common tables include `ContainerLogV2`, `KubePodInventory`, `KubeEvents`, `InsightsMetrics`, and `Perf`; inspect the workspace schema first.
3. Use direct Kubernetes access for current or retained cluster data only. Check authorization before reading pod logs.
4. Inspect workload status, Kubernetes events, current logs, and previous container logs. Filter by namespace, labels, container, time, and error text.
5. Correlate restarts, evictions, probe failures, throttling, scheduling failures, and rollout changes with the target deployment.

Read-only examples:

```bash
kubectl config current-context
kubectl auth can-i get pods --namespace <namespace>
kubectl auth can-i get pods/log --namespace <namespace>
kubectl get pods --namespace <namespace> --selector <labels>
kubectl logs --namespace <namespace> <pod> --container <container> --since=<duration>
kubectl logs --namespace <namespace> <pod> --container <container> --previous --since=<duration>
kubectl get events --namespace <namespace> --sort-by=.metadata.creationTimestamp
```

## Strong evidence

- Repeated OOM kills, evictions, probe failures, or restarts immediately before a defensive change.
- Container logs with the same error text or trace ID as the target path.
- Rollout history or pod metadata that establishes the deployed version.
- Container Insights trends that align resource pressure or failures with the change window.

## Limits and safety

- Pod logs and events often have short retention. State the retention window.
- Pod names and replica counts change. Query the workload and labels, not one remembered pod.
- Direct cluster state mainly describes the present. Do not use it as historical evidence without retained timestamps.
- Do not use `kubectl exec`, port forwarding, debug containers, scaling, rollout changes, or any mutating command.
- Do not return secrets, environment values, customer payloads, or unredacted personal data from logs.

## Return

Return the cluster and namespace at a safe level, workload and container, query or command, UTC time range, compact findings, relevant pod or trace identifiers, retention limits, and evidence strength.
