"""Incident log simulator.

Generates windows of log lines with a KNOWN incident type. The label is the
answer key, so we can score the classifier (and later the AI agent) honestly.

Concept: a "window" is a few minutes of logs from one service. Normal windows
are mostly INFO lines. Incident windows mix in the symptoms of one failure.
Real logs are messy, so every incident window also contains normal lines and
some misleading lines from other failure types.
"""
import random

import pandas as pd

LABELS = [
    "normal",
    "memory_leak",
    "db_down",
    "bad_deploy",
    "cert_expired",
    "account_locked",
    "disk_full",
]

NORMAL_LINES = [
    "INFO request completed status=200 path=/api/bookings latency_ms={ms}",
    "INFO request completed status=200 path=/api/health latency_ms={ms}",
    "INFO user login ok user=u{n}",
    "INFO cache hit key=session:{n}",
    "INFO worker job finished job_id={n} duration_ms={ms}",
    "DEBUG connection pool size=10 in_use={small}",
    "INFO metrics scrape ok",
]

# Symptom lines per incident type. {n}, {ms}, {small} are filled in randomly.
SYMPTOMS = {
    "memory_leak": [
        "WARN heap usage high used_mb={big} limit_mb=512",
        "ERROR java.lang.OutOfMemoryError: Java heap space",
        "WARN gc pause long duration_ms={big}",
        "ERROR container restarted reason=OOMKilled restart_count={small}",
        "WARN request slow path=/api/bookings latency_ms={big}",
    ],
    "db_down": [
        "ERROR connection refused host=db-primary port=5432",
        "ERROR could not connect to database after {small} retries",
        "ERROR query failed: server closed the connection unexpectedly",
        "WARN circuit breaker open dependency=postgres",
        "ERROR request failed status=503 path=/api/bookings",
    ],
    "bad_deploy": [
        "INFO deploy started version=v{small}.{small} image=booking:{n}",
        "ERROR unhandled exception NullPointerException at BookingService.create",
        "ERROR request failed status=500 path=/api/bookings",
        "ERROR config key missing: PAYMENT_API_URL",
        "WARN readiness probe failed after deploy version=v{small}.{small}",
    ],
    "cert_expired": [
        "ERROR tls handshake failed: certificate has expired",
        "ERROR x509: certificate expired or is not yet valid",
        "WARN upstream call failed host=auth.internal reason=ssl_error",
        "ERROR request failed status=502 path=/api/bookings",
        "ERROR peer certificate verification failed",
    ],
    "account_locked": [
        "ERROR ldap bind failed: account locked user=svc-booking",
        "WARN authentication failed user=svc-booking attempts={small}",
        "ERROR kerberos preauthentication failed principal=svc-booking",
        "ERROR request failed status=401 path=/api/bookings",
        "WARN password policy change applied at {ms}",
    ],
    "disk_full": [
        "ERROR no space left on device path=/var/log/app",
        "ERROR failed to write file: disk quota exceeded",
        "WARN filesystem usage 98 percent mount=/data",
        "ERROR database write failed: could not extend file",
        "ERROR request failed status=500 path=/api/bookings",
    ],
}


def _fill(template: str, rng: random.Random) -> str:
    return template.format(
        n=rng.randint(100, 99999),
        ms=rng.randint(5, 250),
        small=rng.randint(1, 9),
        big=rng.randint(900, 6000),
    )


def make_window(label: str, rng: random.Random, lines: int = 30) -> str:
    """Return one window of log text for the given label."""
    out = []
    if label == "normal":
        for _ in range(lines):
            out.append(_fill(rng.choice(NORMAL_LINES), rng))
        # Normal windows still contain the odd harmless warning or error.
        if rng.random() < 0.3:
            out.append(_fill(rng.choice(
                ["WARN request slow path=/api/bookings latency_ms={ms}",
                 "ERROR request failed status=500 path=/api/bookings"]), rng))
    else:
        n_symptoms = rng.randint(4, 12)
        for _ in range(lines - n_symptoms):
            out.append(_fill(rng.choice(NORMAL_LINES), rng))
        for _ in range(n_symptoms):
            out.append(_fill(rng.choice(SYMPTOMS[label]), rng))
        # Misleading noise: one symptom from a different failure type.
        if rng.random() < 0.35:
            other = rng.choice([k for k in SYMPTOMS if k != label])
            out.append(_fill(rng.choice(SYMPTOMS[other]), rng))
    rng.shuffle(out)
    return "\n".join(out)


def make_dataset(per_class: int = 150, seed: int = 0) -> pd.DataFrame:
    rng = random.Random(seed)
    rows = []
    for label in LABELS:
        for _ in range(per_class):
            rows.append({"logs": make_window(label, rng), "label": label})
    df = pd.DataFrame(rows).sample(frac=1.0, random_state=seed).reset_index(drop=True)
    return df


if __name__ == "__main__":
    df = make_dataset(per_class=5, seed=1)
    print(df["label"].value_counts().to_string())
    print("\n--- example: memory_leak window (first 8 lines) ---")
    example = df[df.label == "memory_leak"].iloc[0]["logs"].splitlines()[:8]
    print("\n".join(example))
