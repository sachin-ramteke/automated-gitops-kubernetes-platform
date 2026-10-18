# Automated GitOps Kubernetes Platform with ArgoCD & K3s

An enterprise-ready GitOps continuous delivery platform built on lightweight Kubernetes (K3s) orchestrated by ArgoCD. The platform implements declarative infrastructure and application lifecycle management, automated synchronization from GitHub, continuous drift detection, and automated self-healing.

---

## 🏇 System Architecture

```text
       +----------------------+
       |   Developer Git Push  |
       +-----------+-----------+
                  |
                  v
       +----------------------+
       |  GitHub Repository    | <----+
       |  (Single Source Truth)|      |
       +-----------+-----------+      | Continuous Monitoring &
                  |                  | Drift Detection
                  v                  |
       +----------------------+      |
       |  ArgoCD Controller    +------+
       +-----------+-----------+
                  |
     Declarative Sync / Self-Healing
                  |
                  v
       +---------------------------------------------+
       |           Kubernetes Cluster (K3s)          |
       |                                            |
       |  +--------------------------------------+  |
       |  |  Namespace: default                   |  |
       |  |                                        |  |
       |  |   +--------------------------------++   |  |
       |  |   | Service: gitops-webapp-service|   |  |
       |  |   +----------------+---------------+   |  |
       |  |                  |                  |  |
       |  |   +---------------v---------------+   |  |
       |  |   | Deployment: gitops-webapp     |   |  |
       |  |   +----------------+---------------+   |  |
       |  |                  |                  |  |
       |  |        +----------+----------+        |  |
       |  |        |                    |        |  |
       |  |        v                    v        |  |
       |  |  +------------+-        +------------+ |  |
       |  |  | Pod (v1.0) |        | Pod (v1.0) | |  |
       |  |  +------------+        +------------+ |  |
       |  +---------------------------------------+  |
       +---------------------------------------------+
```J

---

## 💟 Key Architectural Features

- **Declarative Infrastructure as Code (GitOps):** Zero manual cluster intervention (`kubectl apply`); application state declared in Git and continuously reconciled by ArgoCD.
- **Continuous Drift Detection & Self-Healing:** The platform identifies drift between desired Git manifests and live cluster state, automatically reconciling unauthorized manual changes or terminated workloads.
- **Resilient Networking Configuration:** Custom CNI overlay with native snapshotter execution optimized for containerized Linux virtualization environments.
- **Fault Tolerance & Zero Downtime:** Multi-replica pod scheduling backed by Kubernetes Services and ClusterIP abstraction for load distribution.

---

## 📸 Architecture Proof-of-Work

1. **ArgoCD Deployment & Authentication**
  ![ArgoCD Authentication](docs/screenshots/01-argocd-login.png)

2. **Application Dashboard**
  ![ArgoCD Dashboard](docs/screenshots/02-argocd-dashboard.png)

3. **Production Live Topology (Healthy & Synced)**
  ![Production Topology](docs/screenshots/03-argocd-synced.png)

---

## 🛿 Tech Stack

- **Orchestration:** Kubernetes (K3s v1.36)
- **Continuous Delivery:** ArgoCD v3.5.5
- **Workloads:** Python Microservices, Containerd Runtime
- **Version Control & CI:** Git, GitHub
- **Networking:** Flannel CNI, CoreDNS, ClusterIP Services

---

## 🔄 Self-Healing Verification Run


```bash
# Verify current running pods
$ kubectl get pods -l app=gitops-webapp
NAME                              READY   STATUS    RESTARTS   AGE
gitops-webapp-5858447b94-4741r   1/1     Running   0          5m
gitops-webapp-5858447b94-tq4z2   1/1     Running   0          5m

# Trigger simulated failure by terminating a production pod
Q +ubectl delete pod gitops-webapp-5858447b94-4741r
pod "gitops-webapp-5858447b94-4741r" deleted

# Immediate recovery verified (ArgoCD & Kubernetes Reconciled within 2s)
$ kubectl get pods -l app=gitops-webapp
NAME                             READY   STATUS    RESTARTS   AGE
gitops-webapp-5858447b94-kwk44   1/1     Running   0          2s
gitops-webapp-5858447b94-tq4z2   1/1     Running   0          5m
```
