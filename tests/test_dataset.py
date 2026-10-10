from pathlib import Path

import pytest

from nextcountry.config import COUNTRIES_CSV
from nextcountry.dataset import ensure_database, load_countries_csv


def test_bundled_countries_csv_has_required_columns():
    df = load_countries_csv(COUNTRIES_CSV)
    assert len(df) >= 190
    assert set(df.columns) >= {"code", "name_en", "name_ja"}
    assert df["code"].is_unique


def test_ensure_database_creates_master_table(tmp_path: Path, sample_countries_df):
    csv_path = tmp_path / "countries.csv"
    sample_countries_df.to_csv(csv_path, index=False)
    db_path = tmp_path / "app.db"
    ensure_database(db_path, csv_path)

    import sqlite3

    conn = sqlite3.connect(db_path)
    count = conn.execute("SELECT COUNT(*) FROM countries").fetchone()[0]
    prefs = conn.execute("SELECT COUNT(*) FROM user_country_preferences").fetchone()[0]
    conn.close()
    assert count == len(sample_countries_df)
    assert prefs == 0
