# Week 1: Linux, networking, Git, Docker (local, no cost)

Driver: Tejas. Reviewer: teammate. Next week you swap.

Goal: by Sunday, the clinic app runs with Docker Compose, you can read its logs, and you can explain what happens when a request travels from a browser to the database.

Read first: `docs/workload-spec.md`.

## Day 1: The shell and files (about 2 hours learning, 1 hour lab)

Learn: the filesystem layout, `ls cd cat less grep find`, pipes, redirects, file permissions (`chmod`, `chown`), environment variables.
Lab: use `grep` to count ERROR lines in a log file you create. Write a 10 line summary in your own words.
Check yourself: what does `chmod 640 file` allow, and for whom?

## Day 2: Processes and services

Learn: processes, signals, `ps top kill`, systemd units, logs with `journalctl`.
Lab: start a small Python HTTP server, find its process id, stop it with a signal. Read how a systemd unit file is structured.
Check yourself: what is the difference between stopping a process with SIGTERM and SIGKILL?

## Day 3: Networking from zero

Learn: IP addresses, ports, DNS, TCP handshake, firewalls, HTTP, TLS and certificates.
Lab: use `curl -v`, `dig`, `ss -tlnp` and `ping` against a site and against your local server. Draw what happens when you type a URL.
Check yourself: what is the difference between a port being closed and a firewall dropping the packet?

## Day 4: Git workflow

Learn: commits, branches, pull requests, merge conflicts, `.gitignore`.
Lab: create the repo, set up branch `week-01/app`, open a pull request, have the reviewer comment, fix, merge. Install pre-commit hooks with `make hooks`.
Check yourself: why must secrets never be committed, even if you delete them later?

## Day 5: Docker and the app

Learn: images, containers, layers, volumes, networks, Compose.
Build: write the api (FastAPI), the worker and the Postgres service. Write a Dockerfile for each Python service. Write `docker-compose.yml` to run all three. Follow the log contract in the spec.
Check yourself: what is the difference between an image and a container?

## Day 6: Break it, then write it up

Break it on purpose, one at a time. For each, find the cause from logs only, then fix it:
1. Stop the database container while the api is running.
2. Give the api a wrong database password.
3. Fill a volume so writes fail (use a tiny tmpfs size).
4. Set a very low memory limit on the api container.

Write up: copy `docs/templates/writeup.md` to `docs/writeups/week-01.md`. Each person writes 5 lines.

## Day 7: Review and rest

The reviewer runs the whole thing from a clean clone, reads every file, and asks three "why" questions. The driver answers without notes. Merge the pull request when both are satisfied.

## Deliverable

- `services/` with api, worker and `docker-compose.yml`
- Logs follow the contract
- `docs/writeups/week-01.md` with both people's notes
- The gap tracker rows for Linux, networking, Git and Docker moved to Learning or Built

## Do not move to Closed yet

Closed means built, working, on the CV. That happens after the final proof in week 16.
