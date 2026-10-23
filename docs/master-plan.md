# Master Plan: AI On-Call Copilot Platform (16 weeks)

## Project definition

We build a production-style platform (apps, cluster, pipelines, logging, monitoring, identity) and an AI agent that investigates incidents on it. When monitoring raises an alert, the agent gathers logs, metrics and recent changes with read-only tools, finds the likely cause, and writes a report that answers when it happened, why it happened and how it was diagnosed. A chaos engine injects failures with a known cause, so we can measure how often the agent is right, how fast it is, and what each investigation costs.

Two people, both learning every layer from zero. Nothing is claimed on a CV until it is built, working and written up.

## Assumptions (change these if they are wrong)

| Item | Assumed value |
|------|---------------|
| People | Tejas (A) and a teammate (B) |
| Hours per week each | 15 |
| Shared cloud budget | 100 euro per month, with a budget alert at 50 and 80 |
| Main cloud | AWS. Azure in week 15 |
| LLM | Hosted API first, optional local model comparison in week 16 |
| Workload | Small clinic app, see docs/workload-spec.md |

## How every week runs

1. **Learn from zero** (about 4 hours): read, watch, tiny hands-on. Write a 10 line summary in your own words.
2. **Guided lab** (about 3 hours): follow an official tutorial.
3. **Build into the platform** (about 5 hours): the week's deliverable, in the repo.
4. **Break it on purpose** (about 2 hours): cause a failure, find it, fix it.
5. **Write up** (about 1 hour): fill docs/templates/writeup.md. Five lines each, one per person.

## Rotation

Odd weeks: A drives (builds), B reviews and breaks it. Even weeks: swap. Every pull request needs the other person's review. Both of you must be able to explain every file in the repo.

## Depth tiers

- **Deep** (build, break, write up, interview ready): Terraform, Jenkins, Kubernetes, Prometheus, ELK/OpenSearch, Ansible, LLM agent, RAG, evaluation.
- **Working** (fundamentals plus one real use in the platform): Helm, Argo CD, EKS, Docker, GitHub Actions, OpenTelemetry, Vault, cert-manager, Packer, landing zone, Azure, AKS, Entra ID, Active Directory, PowerShell, MLflow, Airflow, CloudFormation.
- **Awareness** (a free trial or an afternoon): Splunk, Dynatrace, Datadog, Kafka, service mesh, VPN lab.

## Cost rules

- Weeks 1, 3 and 5 to 6 run locally (Docker, k3s). They cost nothing.
- EKS and RDS run only in time-boxed sessions, and whoever starts them runs `terraform destroy` at the end.
- Tag everything with `project=copilot` and `owner=<name>` so Cost Explorer shows who spent what.
- Never commit keys or `.env` files.

## The 16 weeks

### Month 1: Foundations and infrastructure

**Week 1: Linux, networking, Git, Docker (local).**
Learn: shell, files and permissions, processes, systemd, DNS, TCP, ports, firewalls, TLS and certificates, Git branches and pull requests, containers and images.
Build: the clinic app (API, worker, Postgres) running with Docker Compose. Structured JSON logs.
Break: kill the database container, then read the logs to find out why requests fail.
Gaps: Linux, networking, Git, Docker.

**Week 2: Terraform and AWS basics.**
Learn: IAM, VPC, subnets, state, providers, modules, variables, outputs.
Build: remote state in S3 with locking, a VPC module, budget alerts, cost allocation tags.
Break: delete a resource by hand, run plan, and explain drift.
Gaps: Terraform, FinOps, AWS fundamentals.

**Week 3: Kubernetes and Helm (local k3s or kind).**
Learn: pods, deployments, services, ingress, configmaps, secrets, probes, resource limits, rolling updates, Helm charts.
Build: the clinic app on Kubernetes, packaged as a Helm chart.
Break: wrong image tag, a failing probe, an out-of-memory limit.
Gaps: Kubernetes, Helm.

**Week 4: EKS, RDS and CloudFormation.**
Learn: EKS architecture, node groups, IAM roles for service accounts, upgrades.
Build: EKS and RDS with Terraform, the app deployed from the Helm chart. Rebuild one small stack in CloudFormation.
Break: drain a node, then upgrade the cluster version. Destroy everything at the end.
Gaps: EKS lifecycle, RDS, CloudFormation.
Certification checkpoint: Terraform Associate study can start now.

### Month 2: Delivery and observability

**Week 5: Jenkins from zero.**
Learn: controller and agents, Jenkinsfile, Groovy basics, plugins, credentials, JCasC.
Build: Jenkins in Docker Compose, configured as code, with a pipeline that lints, tests and builds the app image.
Break: a failing test, a broken plugin upgrade, a lost agent.
Gaps: Jenkins, Groovy.

**Week 6: Pipeline security, artifacts, GitHub Actions.**
Learn: scan gates, SAST, secret scanning, artifact repositories.
Build: Trivy, secret scan and SonarQube gates in Jenkins, an artifact repository (Artifactory or Nexus), Terraform plan and apply in a pipeline, the same flow in GitHub Actions for comparison.
Break: a vulnerable base image blocks the build. Write the root cause analysis.
Gaps: scan gates, Artifactory, Maven or Gradle basics, GitHub Actions, Terraform in CI.

**Week 7: GitOps with Argo CD.**
Learn: GitOps, reconciliation, app of apps, sync policies.
Build: Argo CD deploying everything from Git, Jenkins updating the image tag in Git.
Break: change something by hand in the cluster and watch self-heal. Roll back a bad deploy through Git.
Gaps: Argo CD, GitOps.

**Week 8: Prometheus, Grafana, Alertmanager, tracing.**
Learn: metrics, PromQL, exporters, SLOs, alert routing, traces and spans.
Build: Prometheus with node-exporter, kube-state-metrics and cAdvisor, app metrics, Grafana dashboards, alert rules, OpenTelemetry tracing with Jaeger.
Break: trigger an alert on purpose, then silence it, then fix it.
Gaps: Prometheus, Grafana, OpenTelemetry.
Certification checkpoint: CKA study can start now.

### Month 3: Logs, configuration, secrets, the agent

**Week 9: ELK / OpenSearch.**
Learn: indexing, mappings, queries, ingestion, dashboards, alerting.
Build: Fluent Bit shipping app and Kubernetes logs to OpenSearch, dashboards, alerts. A one-afternoon Splunk free trial for comparison.
Break: a mapping conflict, then a full disk on the search node.
Gaps: ELK/OpenSearch, Splunk (awareness).

**Week 10: Ansible and Packer.**
Learn: inventories, playbooks, roles, handlers, vault, idempotency.
Build: roles that configure a small Linux fleet, run from Jenkins. A Packer golden image.
Break: a non-idempotent task, then a role that fails halfway.
Gaps: Ansible, Packer.

**Week 11: Secrets, certificates, and the chaos engine.**
Learn: Vault basics, certificate lifecycle, ACME.
Build: Vault for secrets, cert-manager with Let's Encrypt or a private CA. Chaos engine v1 with injectors for bad deploy, memory leak, database down, disk full, expired certificate.
Break: let a certificate expire on purpose.
Gaps: Vault, cert-manager, certificate rotation.

**Week 12: The agent, part 1: tools and the ML model.**
Learn: tool calling, agent loops, guardrails, prompt injection.
Build: first rebuild the incident classifier in ml/ yourselves, then compare with the reference. MLflow on the cluster. Agent tools: search_logs, query_metrics, get_recent_deploys, classify_incident. Read-only, with a call budget and timeout.
Break: put a prompt injection in a log line and see what the agent does.
Gaps: LLM agents with tool use, MLflow, model versioning.

**Week 13: The agent, part 2: RAG, reports, evaluation.**
Learn: embeddings, chunking, retrieval quality, evaluation sets, cost tracking.
Build: runbook and past-incident RAG on pgvector or Qdrant, the report generator, an evaluation harness over 30 injected incidents, Grafana panels for tokens, latency and cost. An Airflow DAG that retrains and promotes the model.
Break: remove the runbook that matches an incident and see how the agent copes.
Gaps: RAG, vector DB operations, LLMOps, Airflow.

### Month 4: Governance, identity, proof

**Week 14: Landing zone and policy as code.**
Learn: AWS Organizations, OUs, SCPs, Control Tower concepts, GCP org policies.
Build: Organizations, OUs and SCPs in Terraform, an OPA or Checkov check, a DR runbook.
Break: attempt a denied action and capture the SCP block.
Gaps: landing zones, SCPs, org policies, policy as code, DR.

**Week 15: Azure, Entra ID, Active Directory.**
Learn: Entra ID, app registrations, OIDC, AKS, Active Directory, GPO, PowerShell.
Build: a small app on AKS with Entra login, a Windows Server VM with AD, a GPO and PowerShell scripts, a locked-account incident for the chaos engine.
Break: lock a service account and trace the failure.
Gaps: Azure, AKS, Entra ID, Active Directory, PowerShell, SSO.

**Week 16: Game days, proof, write-ups.**
Do: run 30 injected incidents (software and IT), time a manual diagnosis on a sample as a baseline, score the agent (correct cause, time, tool calls, cost). ITIL-style incident, change and problem records. Full teardown and rebuild from code. Final write-ups and CV bullets for each person.
Gaps: ITIL (process), evidence for everything above.

## Certification track (in parallel, not part of the weekly hours)

| Certificate | Study can start after |
|-------------|-----------------------|
| HashiCorp Terraform Associate | Week 4 |
| CKA | Week 8 |
| AWS Solutions Architect Associate | Any time |
| ITIL 4 Foundation | Week 16 |

## Definition of done

- Repo with README, architecture diagram, runbooks
- Screenshots: a pipeline blocked and then passing, Argo CD synced, a Grafana alert, an OpenSearch dashboard, an agent report, an SCP deny
- Evaluation table for the agent against injected incidents, including the failures
- At least three written-up failures and fixes
- A documented rebuild from scratch
- Per-person notes on who built what, so CV claims stay honest
