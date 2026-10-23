# AI On-Call Copilot Platform

A production-style platform and an AI agent that investigates incidents on it. When monitoring raises an alert, the agent gathers logs, metrics and recent changes with read-only tools, finds the likely cause, and writes a report that says when it happened, why, and how it was diagnosed.

Built by two people learning every layer from zero, over 16 weeks.

## Start here (VS Code)

1. Open this folder in VS Code (File, Open Folder).
2. Accept the recommended extensions when VS Code asks.
3. Read `CONTEXT.md`, then `docs/master-plan.md`.
4. Start `docs/weeks/week-01.md`.
5. Use branches and pull requests, see `CONTRIBUTING.md`.

## Layout

```
ml/            incident classifier with MLflow (reference solution, rebuild it in week 12)
services/      the clinic app: api, worker (week 1)
infra/         Terraform: VPC, EKS, RDS (weeks 2 and 4)
charts/        Helm charts (week 3)
jenkins/       Jenkins as code and Jenkinsfiles (weeks 5 and 6)
gitops/        Argo CD apps (week 7)
monitoring/    Prometheus, Grafana, OpenTelemetry (week 8)
logging/       OpenSearch and Fluent Bit (week 9)
ansible/       roles and playbooks (week 10)
chaos/         failure injectors (week 11 onward)
agent/         the incident agent, RAG, evaluation (weeks 12 and 13)
landing-zone/  Organizations, SCPs, policy checks (week 14)
azure/         AKS, Entra, Active Directory lab (week 15)
docs/          plan, tracker, weekly guides, write-ups, templates
```

## Rules

- No secrets in Git. Ever.
- Nothing goes on a CV until it is built, working and written up.
- Plain hyphens and commas in writing. Black and white diagrams.
- Destroy cloud resources at the end of every session.
