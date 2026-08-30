from querypilot.dataset import create_dataset


def test_dataset_is_reproducible_and_has_expected_tables(tmp_path) -> None:
    first = create_dataset(tmp_path / "first.db")
    second = create_dataset(tmp_path / "second.db")

    import sqlite3

    with sqlite3.connect(first) as first_connection, sqlite3.connect(second) as second_connection:
        first_counts = first_connection.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
        second_counts = second_connection.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
        assert first_counts == second_counts
        assert first_counts > 10_000
        tables = first_connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
        ).fetchall()
        assert [table[0] for table in tables] == [
            "accounts", "campaigns", "leads", "opportunities", "product_usage",
            "subscriptions", "support_tickets",
        ]
