# CONTEXT (read this first, including any AI assistant you use)

## What we are building

An AI on-call copilot on a production-style platform. Monitoring tools (Prometheus, Alertmanager, OpenSearch) detect problems and raise alerts. The AI agent investigates with read-only tools and writes an incident report answering when, why and how. A chaos engine injects failures with a known cause so we can score the agent.

## People and goals

- Two MSc Cloud Computing graduates (Tejas and a teammate), both learning every layer from zero.
- Goal 1: close the gaps in each person's tech gap tracker, with working evidence.
- Goal 2: be able to explain and defend every part in interviews.
- Tejas is also moving toward Forward Deployed Engineer roles.

## Decisions made

- Project: AI on-call copilot plus the platform it watches. Not a CV-only demo.
- The agent is read-only first. Proposing fixes as pull requests is a stretch goal, and a human must approve.
- Everything is treated as fresh learning, including tools used before.
- Order: foundations and infrastructure, then delivery and observability, then logs, configuration and the agent, then governance and identity.
- Main cloud: AWS. Azure in week 15. Hosted LLM first.
- The old Sapphire Villas app is not used as the workload.
- Workload: small clinic app, see docs/workload-spec.md.
- The ML layer in ml/ is a reference solution to rebuild in week 12.

## Assumptions still to confirm

- 15 hours per week each
- 100 euro per month shared cloud budget
- Teammate's strengths (decides who leads which week)

## Working agreements

- Odd weeks Tejas drives and the teammate reviews and breaks it. Even weeks swap.
- Every change goes through a pull request reviewed by the other person.
- Each week ends with a write-up, five lines per person (docs/templates/writeup.md).
- Run `terraform destroy` after every cloud session. Budget alerts are on.
- Never commit secrets or `.env` files.

## Writing style

- No em dashes. Use plain hyphens and commas.
- Black and white diagrams.
- CV entries use what-I-built style and claim only what is built and working.

## Interfaces between parts (keep stable)

- App logs: JSON lines with ts, level, service, msg, request_id.
- Incident labels: normal, memory_leak, db_down, bad_deploy, cert_expired, account_locked, disk_full.
- Agent tools are read-only: search_logs, query_metrics, get_recent_deploys, classify_incident.

## How to use an AI assistant here

Paste or attach this file first. Ask it to explain before it builds, to give a break-it exercise after each step, and to keep the CV rule. Do not let it write a week's deliverable for you without you being able to explain it.
