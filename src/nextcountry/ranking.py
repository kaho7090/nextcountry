import pandas as pd


def rank_unvisited(countries_df: pd.DataFrame) -> pd.DataFrame:
    """
    未訪問国を優先度降順・日本語名昇順でランキング。
    入力列: code, name_en, name_ja, visited, priority
    """
    required = {"code", "name_en", "name_ja", "visited", "priority"}
    missing = required - set(countries_df.columns)
    if missing:
        raise ValueError(f"不足している列: {sorted(missing)}")

    df = countries_df.copy()
    df["visited"] = df["visited"].astype(int)
    df["priority"] = df["priority"].astype(int)
    unvisited = df[df["visited"] == 0].copy()
    unvisited = unvisited.sort_values(
        by=["priority", "name_ja", "code"],
        ascending=[False, True, True],
        kind="mergesort",
    )
    unvisited = unvisited.reset_index(drop=True)
    unvisited.insert(0, "rank", unvisited.index + 1)
    return unvisited[
        ["rank", "code", "name_ja", "name_en", "priority"]
    ]
