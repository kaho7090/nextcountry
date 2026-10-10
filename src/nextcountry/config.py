from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_ROOT.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
COUNTRIES_CSV = DATA_DIR / "countries.csv"
DEFAULT_DB_PATH = DATA_DIR / "nextcountry.db"
