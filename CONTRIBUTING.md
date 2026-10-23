# Contributing

## Branches and pull requests

- `main` is always working. Never commit to it directly.
- Branch names: `week-02/vpc-module`, `week-05/jenkins-jcasc`.
- Open a pull request for every change. The other person reviews it.
- Merge only when the reviewer has run it or read it and can explain it.

## Review checklist

- Does it run from a clean checkout?
- Are there secrets, keys or `.env` files in the diff?
- For Terraform: is `terraform plan` output attached, and are resources tagged `project=copilot` and `owner`?
- Is the cost of running it written down, and is there a destroy step?
- Is there a short note in the week's write-up?

## Secrets

- Never commit keys, tokens, passwords, or Terraform state.
- Use environment variables or a secret manager. Keep a `.env.example` with fake values.
- If a secret is committed by mistake, rotate it first, then clean the history.

## Commit messages

Short and specific, for example `Add VPC module with private subnets`.

## Cloud hygiene

- Start a cloud session: check the budget dashboard.
- End a cloud session: `terraform destroy`, then confirm in the console that nothing is still running.
