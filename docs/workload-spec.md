# Workload spec: the clinic app

The app exists to give the platform something real to run, log, monitor and break. Keep it small. Build it yourselves in week 1.

## Services

| Service | What it does | Tech suggestion |
|---------|--------------|-----------------|
| api | HTTP API: list slots, book appointment, health check, metrics | Python with FastAPI |
| worker | Background job: sends booking reminders from a queue table | Python script, polls Postgres |
| db | Stores slots, appointments, reminders | Postgres |

Later weeks add: a risk endpoint that calls the classifier or a risk model, and an optional small frontend.

## API endpoints

- `GET /health` returns 200 when the app and database are reachable
- `GET /slots` lists free slots
- `POST /appointments` books a slot
- `GET /metrics` exposes Prometheus metrics (week 8)

## Log contract (do not change without telling the other person)

One JSON object per line on stdout:

```
{"ts": "2026-10-26T09:15:02Z", "level": "ERROR", "service": "api", "msg": "database connection refused", "request_id": "abc123"}
```

Levels: DEBUG, INFO, WARN, ERROR. Every request logs one line with `request_id`, path, status and latency in milliseconds.

## Metrics to expose (week 8)

- request count by path and status
- request latency histogram
- database connection errors
- worker jobs processed and failed

## Failure hooks (for the chaos engine, from week 11)

Each failure must be injectable without editing code:

| Incident label | How it is injected |
|----------------|--------------------|
| memory_leak | An environment flag makes the api allocate memory on each request |
| db_down | Stop or block the database |
| bad_deploy | Deploy an image tag with a missing config key |
| disk_full | Fill the log volume |
| cert_expired | Serve a certificate that has expired |
| account_locked | Lock the service account (week 15) |
| normal | No injection |

These labels match the classifier in ml/.
