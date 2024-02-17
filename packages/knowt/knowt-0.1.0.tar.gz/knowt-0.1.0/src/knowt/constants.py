# constants.py
import datetime
from pathlib import Path


try:
    BASE_DIR = Path(__file__).parent
except Exception:
    BASE_DIR = Path('./data')
DATA_DIR = BASE_DIR / "data"
GLOBS = ("**/*.txt", "**/*.md")

CORPUS_DIR = DATA_DIR / 'corpus'
DF_PATH = CORPUS_DIR / 'nutrition_sentences.csv'
EMBEDDINGS_PATH = DF_PATH.with_suffix('.embeddings.joblib')
EXAMPLES_PATH = DF_PATH.with_suffix('.search_results.csv')

TODAY = datetime.date.today()
