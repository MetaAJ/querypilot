"""Deterministic synthetic ForgeFlow revenue dataset generator."""

import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path


SCHEMA = """
CREATE TABLE accounts (
    account_id INTEGER PRIMARY KEY,
    company_name TEXT NOT NULL,
    industry TEXT NOT NULL,
    region TEXT NOT NULL,
    employee_band TEXT NOT NULL,
    plan TEXT NOT NULL
);
CREATE TABLE campaigns (
    campaign_id INTEGER PRIMARY KEY,
    campaign_name TEXT NOT NULL,
    channel TEXT NOT NULL,
    monthly_budget REAL NOT NULL
);
CREATE TABLE leads (
    lead_id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(account_id),
    campaign_id INTEGER NOT NULL REFERENCES campaigns(campaign_id),
    created_at TEXT NOT NULL,
    lead_score INTEGER NOT NULL,
    lifecycle_stage TEXT NOT NULL,
    sales_response_hours REAL NOT NULL
);
CREATE TABLE opportunities (
    opportunity_id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(account_id),
    created_at TEXT NOT NULL,
    amount REAL NOT NULL,
    stage TEXT NOT NULL,
    won INTEGER NOT NULL
);
CREATE TABLE subscriptions (
    subscription_id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(account_id),
    started_at TEXT NOT NULL,
    monthly_recurring_revenue REAL NOT NULL,
    churned_at TEXT
);
CREATE TABLE support_tickets (
    ticket_id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(account_id),
    created_at TEXT NOT NULL,
    severity TEXT NOT NULL,
    resolution_hours REAL NOT NULL
);
CREATE TABLE product_usage (
    usage_id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(account_id),
    week_start TEXT NOT NULL,
    active_users INTEGER NOT NULL,
    weekly_events INTEGER NOT NULL
);
"""


def create_dataset(output_path: str | Path, seed: int = 42) -> Path:
    """Create a reproducible ForgeFlow database and return its path."""
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        destination.unlink()

    random_generator = random.Random(seed)
    connection = sqlite3.connect(destination)
    connection.executescript(SCHEMA)
    _insert_reference_data(connection)
    _insert_accounts(connection)
    _insert_time_series(connection, random_generator)
    connection.commit()
    connection.close()
    return destination


def _insert_reference_data(connection: sqlite3.Connection) -> None:
    campaigns = [
        (1, "Developer Productivity Search", "paid_search", 18000),
        (2, "Engineering Leaders Webinar", "webinar", 12000),
        (3, "Open Source Community", "community", 8000),
        (4, "Platform Migration Guide", "content", 10000),
    ]
    connection.executemany("INSERT INTO campaigns VALUES (?, ?, ?, ?)", campaigns)


def _insert_accounts(connection: sqlite3.Connection) -> None:
    industries = ["Software", "Fintech", "Healthcare", "E-commerce", "Education"]
    regions = ["North America", "Europe", "Asia Pacific", "Latin America"]
    bands = ["1-50", "51-200", "201-1000", "1000+"]
    plans = ["Starter", "Growth", "Enterprise"]
    rows = [
        (account_id, f"ForgeFlow Customer {account_id:03d}", industries[account_id % 5],
         regions[account_id % 4], bands[account_id % 4], plans[account_id % 3])
        for account_id in range(1, 101)
    ]
    connection.executemany("INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?)", rows)


def _insert_time_series(connection: sqlite3.Connection, random_generator: random.Random) -> None:
    start = date(2025, 1, 1)
    leads = []
    opportunities = []
    subscriptions = []
    tickets = []
    usage = []
    lead_id = opportunity_id = subscription_id = ticket_id = usage_id = 1

    for week_number in range(78):
        week_start = start + timedelta(days=week_number * 7)
        for account_id in range(1, 101):
            campaign_id = (account_id + week_number) % 4 + 1
            lead_count = 1 + ((account_id + week_number) % 3 == 0)
            for _ in range(lead_count):
                quality_penalty = 18 if week_number >= 58 and campaign_id == 1 else 0
                response_penalty = 12 if week_number >= 65 and account_id % 4 == 0 else 0
                score = max(20, min(98, 72 + random_generator.randint(-24, 22) - quality_penalty))
                stage = "qualified" if score >= 70 else "new"
                response_hours = max(2, 18 + random_generator.random() * 30 + response_penalty)
                leads.append((lead_id, account_id, campaign_id, week_start.isoformat(), score, stage, response_hours))
                lead_id += 1

            active_users = max(1, 3 + account_id % 12 + random_generator.randint(-2, 4))
            events = active_users * (35 + (account_id * 7 + week_number) % 90)
            usage.append((usage_id, account_id, week_start.isoformat(), active_users, events))
            usage_id += 1

            if (account_id + week_number) % 17 == 0:
                amount = 900 + (account_id % 5) * 700
                won = int((account_id + week_number) % 3 != 0)
                opportunities.append((opportunity_id, account_id, week_start.isoformat(), amount, "closed_won" if won else "closed_lost", won))
                opportunity_id += 1

            if (account_id + week_number) % 29 == 0 or (week_number >= 62 and account_id % 11 == 0):
                severity = "high" if week_number >= 62 and account_id % 11 == 0 else "medium"
                tickets.append((ticket_id, account_id, week_start.isoformat(), severity, 12 + random_generator.random() * 60))
                ticket_id += 1

        if week_number in (0, 26, 52):
            for account_id in range(1, 101):
                subscriptions.append((subscription_id, account_id, week_start.isoformat(), 500 + (account_id % 3) * 1000, None))
                subscription_id += 1

    connection.executemany("INSERT INTO leads VALUES (?, ?, ?, ?, ?, ?, ?)", leads)
    connection.executemany("INSERT INTO opportunities VALUES (?, ?, ?, ?, ?, ?)", opportunities)
    connection.executemany("INSERT INTO subscriptions VALUES (?, ?, ?, ?, ?)", subscriptions)
    connection.executemany("INSERT INTO support_tickets VALUES (?, ?, ?, ?, ?)", tickets)
    connection.executemany("INSERT INTO product_usage VALUES (?, ?, ?, ?, ?)", usage)
