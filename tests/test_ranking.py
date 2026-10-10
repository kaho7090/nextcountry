import pandas as pd

from nextcountry.ranking import rank_unvisited


def test_rank_unvisited_excludes_visited_and_sorts():
    df = pd.DataFrame(
        [
            {"code": "JP", "name_en": "Japan", "name_ja": "日本", "visited": 1, "priority": 5},
            {"code": "US", "name_en": "United States", "name_ja": "米国", "visited": 0, "priority": 2},
            {"code": "FR", "name_en": "France", "name_ja": "フランス", "visited": 0, "priority": 4},
            {"code": "IS", "name_en": "Iceland", "name_ja": "アイスランド", "visited": 0, "priority": 4},
        ]
    )
    ranked = rank_unvisited(df)
    assert list(ranked["code"]) == ["IS", "FR", "US"]
    assert ranked.iloc[0]["rank"] == 1
    assert "JP" not in set(ranked["code"])
