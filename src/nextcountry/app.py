"""Streamlit UI（日本語）。"""

import sqlite3

import pandas as pd
import streamlit as st

from nextcountry.config import COUNTRIES_CSV, DEFAULT_DB_PATH
from nextcountry.dataset import ensure_database
from nextcountry.ranking import rank_unvisited
from nextcountry.repository import list_countries_with_preferences, set_priority, set_visited

st.set_page_config(page_title="NextCountry", page_icon="🌍", layout="wide")


@st.cache_resource
def get_connection(db_path: str) -> sqlite3.Connection:
    ensure_database(DEFAULT_DB_PATH, COUNTRIES_CSV)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def main() -> None:
    st.title("NextCountry")
    st.caption("未訪問国を優先度付きでランキングし、旅の計画を支援します。")

    conn = get_connection(str(DEFAULT_DB_PATH))
    records = list_countries_with_preferences(conn)
    df = pd.DataFrame(records)

    visited_count = int((df["visited"] == 1).sum())
    total = len(df)
    st.metric("訪問済み / 全地域", f"{visited_count} / {total}")

    options = df.apply(
        lambda r: f"{r['name_ja']} ({r['name_en']}) [{r['code']}]", axis=1
    ).tolist()
    code_by_label = dict(zip(options, df["code"]))

    tab_rank, tab_visit, tab_priority = st.tabs(
        ["未訪問国ランキング", "訪問状況", "優先度の設定"]
    )

    with tab_rank:
        st.subheader("未訪問国ランキング")
        ranked = rank_unvisited(df)
        if ranked.empty:
            st.info("未訪問の国がありません。")
        else:
            display = ranked.rename(
                columns={
                    "rank": "順位",
                    "code": "コード",
                    "name_ja": "国名（日本語）",
                    "name_en": "国名（英語）",
                    "priority": "優先度",
                }
            )
            st.dataframe(display, use_container_width=True, hide_index=True)

    with tab_visit:
        st.subheader("訪問済みにする")
        current_visited = df[df["visited"] == 1]["code"].tolist()
        selected_labels = st.multiselect(
            "訪問済みの国",
            options=options,
            default=[
                lbl for lbl, code in code_by_label.items() if code in current_visited
            ],
        )
        if st.button("訪問状況を保存", type="primary"):
            selected_codes = {code_by_label[lbl] for lbl in selected_labels}
            for row in df.itertuples(index=False):
                set_visited(conn, row.code, row.code in selected_codes)
            st.success("訪問状況を保存しました。")
            st.rerun()

    with tab_priority:
        st.subheader("国ごとの優先度（0〜5）")
        st.write("訪問済みの国にも優先度を残せます。")
        label = st.selectbox(
            "国を選択",
            options=options,
            index=0,
        )
        code = code_by_label[label]
        current = int(df.loc[df["code"] == code, "priority"].iloc[0])
        priority = st.slider("優先度", min_value=0, max_value=5, value=current)
        if st.button("優先度を保存"):
            set_priority(conn, code, priority)
            st.success(f"{label} の優先度を {priority} に保存しました。")
            st.rerun()


if __name__ == "__main__":
    main()
