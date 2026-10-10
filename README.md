# nextcountry

NextCountry helps travellers discover unvisited countries and plan efficient trips.

## 概要

NextCountry は、未訪問の国を優先度（0〜5）でランキングし、訪問済み国を記録する Streamlit アプリです。国マスタは同梱 CSV、個人の訪問状況・優先度は SQLite に保存します（外部 API は使いません）。

## 技術スタック

- Python 3.12
- Streamlit
- SQLite
- pandas
- pytest

## セットアップ

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## 起動

```bash
streamlit run src/nextcountry/app.py
```

ブラウザで UI が開きます（表示言語は日本語）。

## テスト

```bash
pytest
```

## データ

| ファイル | 内容 |
|----------|------|
| `data/countries.csv` | 国コード・英語名・日本語名（マスタ） |
| `data/nextcountry.db` | 訪問状況・優先度（初回起動時に自動作成、git 管理外） |

## プロジェクト構成

```text
src/nextcountry/   アプリ本体（DB・ランキング・Streamlit）
data/              国マスタ CSV と SQLite DB
tests/             pytest
```
