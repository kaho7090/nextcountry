import pytest

from nextcountry.repository import list_countries_with_preferences, set_priority, set_visited


def test_set_visited_and_priority_persist(db_conn):
    set_visited(db_conn, "JP", True)
    set_priority(db_conn, "JP", 5)
    set_priority(db_conn, "US", 3)

    rows = {r["code"]: r for r in list_countries_with_preferences(db_conn)}
    assert rows["JP"]["visited"] == 1
    assert rows["JP"]["priority"] == 5
    assert rows["US"]["visited"] == 0
    assert rows["US"]["priority"] == 3


def test_priority_out_of_range_raises(db_conn):
    with pytest.raises(ValueError):
        set_priority(db_conn, "FR", 6)
