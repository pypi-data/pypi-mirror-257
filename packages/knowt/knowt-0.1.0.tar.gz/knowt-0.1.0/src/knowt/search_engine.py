"""
## TODO: Specialized MemMap file for Wikipedia articles
### 1. memmap.MemMap
- use memmap within VectorDB instead of RAM CSV

### 2. Specialized Wikipedia MemMap
- fix wikipedia page download (consider using `pwiki` instead of nlpia2-wikipedia)
- add binary category tags to all pages downloaded
- script to convert MariaDB *.sql.gz to CSVs
- add category prefix to all titles https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-category.sql.gz
- add page title to intro paragraph
"""

import argparse
import re
import sys
import time
import jsonlines as jsl

import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from py_lsh import LSHash
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

from .constants import DATA_DIR, GLOBS, DF_PATH
from .memmap import generate_encodings

try:
    nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
except OSError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
nlp.add_pipe("sentencizer")

model = SentenceTransformer("all-MiniLM-L6-v2")
NUM_DIM = len(model.encode(['hi'])[0])


def load_data(data_dir=DATA_DIR / 'corpus', globs=GLOBS, limit=None):
    """Load data from text files and return a DataFrame."""
    globs = globs or GLOBS
    if isinstance(globs, str):
        globs = (globs,)
    data_dir = Path(data_dir)
    data = []

    filepaths = []
    for g in globs:
        print(g)
        filepaths.extend(list(data_dir.glob(g)))
        print(len(filepaths))
    for i, filename in enumerate(filepaths):
        if limit and i >= limit:
            break
        print(f"Processing {filename}...")
        file_path = data_dir / filename

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Create a mapping of character positions to line numbers
        line_starts = {0: 1}
        for i, char in enumerate(content):
            if char == "\n":
                line_starts[i + 1] = line_starts[i] + 1
            else:
                line_starts[i + 1] = line_starts[i]

        # Process the entire content with spaCy
        doc = nlp(content)
        for sent in doc.sents:
            start_char = sent.start_char
            line_number = line_starts[start_char]
            sentence = sent.text.strip()
            data.append(
                {
                    "filename": filename,
                    "sentence": ' '.join(sentence.splitlines()),
                    "line_number": line_number,
                    "line_start": line_starts[start_char],
                    "sent_start_char": start_char,
                    "len": len(sent.text),
                    "num_tokens": len(sent),
                }
            )

    return pd.DataFrame(data)


def generate_all_embeddings(df):
    """ Generate embedding vectors, one for each row in the DataFrame. """
    print(f"Generating embeddings for {len(df)} documents (sentences)...")
    num_tokens = df["num_tokens"].sum()
    num_chars = df["sentence"].str.len().sum()
    t = time.time()
    embeddings = model.encode(df["sentence"].tolist(), show_progress_bar=True)
    t -= time.time()
    t *= -1
    print(f"Finished embedding {len(df)} sentences({num_tokens} tokens) in {t} s.")
    print(f"   {num_tokens/t/1000:.6f} token/ms\n   {num_chars/t/1000:.6f} char/ms")
    return embeddings


# def hash_embeddings(df):
#    print("Hashing embeddings for {len(df)} documents (sentences)...")
#    t = time.time()
#    hashes = model.encode(df["sentence"].tolist(), show_progress_bar=True)
#    t = time.time()

def generate_hashes(embeddings, hash_size=None, input_dims=None, num_hashtables=None):
    input_dims = int(input_dims or len(embeddings[0]))
    input_dims = int(input_dims)
    hash_size = int(hash_size or int(2 * np.sqrt(input_dims)) + 2)
    print(f'hash_size: {hash_size}\ninput_dims: {input_dims}\nnum_hashtables: {num_hashtables}\n')

    num_hashtables = num_hashtables or 1
    lsh = LSHash(hash_size=hash_size, input_dim=input_dims, num_hashtables=num_hashtables)
    for e in embeddings:
        lsh.index(e)
    return lsh


def prettify_search_results(top_docs, ascending=False):
    """ Print out a sorted list of search result sentence pairs with relevance """
    # TODO: highlight most relevant parts of sentencess with **text**
    if not len(top_docs):
        return "No results found."
    top_docs = top_docs.sort_values('relevance', ascending=ascending)
    return [
        f"{i+1:02d} {row['relevance']:.2f}: {row['sentence']}\n"
        + f"    ({Path(row['filename']).name}:{row['line_number']})"
        for i, (index, row) in enumerate(top_docs.iterrows())
    ]


def pretty_print(top_docs):
    if isinstance(top_docs, pd.DataFrame):
        top_docs = prettify_search_results(top_docs, ascending=False)
    if isinstance(top_docs, (list, tuple)):
        top_docs = '\n'.join(top_docs)
    print(top_docs)


class VectorDB:
    def __init__(self, df=DF_PATH, embeddings=None, encoder=model.encode, lsh=None, limit=None, min_relevance=0, refresh=False):
        self.limit = limit or 100
        self.min_relevance = min_relevance
        self.encoder = encoder

        self.num_dim = self.encoder(['hi'])[0].shape[1]
        self.df_path = df or DF_PATH
        # load sentences from cache/sentences.csv or recreate it from text files
        if isinstance(df, pd.DataFrame):
            self.df = df
        elif refresh or not isinstance(self.df_path, (str, Path)) or not Path(self.df_path).exists():
            if isinstance(df, (str, Path)):
                df = Path(df)
                if df.is_dir():
                    self.df_path = df / 'sentences.csv'
                elif df.is_file():
                    self.df = df
            self.df = load_data(self.df_path.parent, limit=self.limit)  # use default corpus dir
            self.df.to_csv(DF_PATH, index=False)
        else:
            if isinstance(df, (str, Path)):
                df = Path(df)
                if df.is_file():
                    print(f"Trying to load cached sentences from {df}...")
                    self.df = pd.read_csv(df)
                elif df.is_dir():
                    print(f"Trying to load and parse sentences from text files in {df} directory...")
                    self.df = pd.read_csv(df)
                else:
                    print()
                    raise ValueError(f'ERROR: unable to load sentence from {str(df)[:256]} of type {type(df)}.')

        self.embeddings_path = Path(self.df_path.with_suffix(".embeddings.joblib"))
        print(f'embeddings_path: {self.embeddings_path}')
        # load sentences from cache/sentences.csv or recreate it from text files
        if isinstance(embeddings, (pd.DataFrame, np.ndarray)):
            self.embeddings = np.array(embeddings)
            print(f'1 embeddings type: {type(self.embeddings)}')
            joblib.dump(self.embeddings_path)
        elif refresh or not isinstance(self.embeddings_path, (str, Path)) or not self.embeddings_path.is_file():
            self.embeddings = generate_encodings(self.df)
            print(f'2 embeddings type: {type(self.embeddings)}')
            print(f'2 embeddings_path: {self.embeddings_path}')
            joblib.dump(self.embeddings, self.embeddings_path)
        else:  # None
            print(f"3 Loading embeddings from file {self.embeddings_path}...")
            self.embeddings = joblib.load(self.embeddings_path)
            if self.embeddings is None:
                self.embeddings = generate_encodings(self.df)

        self.lsh = generate_hashes(self.embeddings)

    def search(self, query, min_relevance=None, limit=None, n_sentences=2, lsh_limit=None):
        """ Search the corpus sentence embeddings with the equivalent embedding of the query string. """
        if isinstance(limit, int) and limit > 0:
            self.limit = limit
        limit = limit or self.limit

        if isinstance(min_relevance, (float, int)):
            self.min_relevance = min_relevance
        if min_relevance is None:
            min_relevance = self.min_relevance
        if min_relevance is True:
            min_relevance = self.min_relevance
        min_relevance = min_relevance or 0

        if not isinstance(self.embeddings, pd.DataFrame):
            self.embeddings = pd.DataFrame(self.embeddings)
        self.n_sentence_embeddings = self.embeddings.rolling(n_sentences).mean()
        query_embedding = self.model.encode([query])
        if lsh_limit:
            self.lsh.query(query_embedding, num_results=lsh_limit)
        similarities = cosine_similarity(
            query_embedding,
            self.n_sentence_embeddings[n_sentences - 1:])[0]
        top_indices = np.argsort(similarities)[-limit:]
        top_docs_df = self.df.iloc[top_indices]
        top_docs = [self.df.iloc[top_indices + i] for i in range(n_sentences)]
        top_docs_df['sentence'] = [" ".join(s) for s in zip(*[d['sentence'] for d in top_docs])]
        top_docs_df['relevance'] = similarities[top_indices].copy()

        return top_docs_df[top_docs_df['relevance'] >= min_relevance].copy()

    def preprocess_query(self, query):
        """ Transform questions into statements likely to correspond to useful sentences in the corpus. """
        query = query.strip()
        is_question = ''
        if query[-1] == '?':
            is_question = query
            query = query.rstrip('?')
        query_doc = nlp(query)
        if query_doc[0].text.lower() in 'who what when where why how':
            is_question = is_question or query
            suffix = f'{query_doc[0].text}.'
            query = query_doc[1:].text
            if query_doc[1].pos_ in 'AUX VERB':
                query = query_doc[2:].text + f'{query_doc[1].text} {suffix}'
        return query

    def search_pretty(self, query, preprocess=True, min_relevance=None, limit=None):
        """ Pretty print search results to a string rather than returning a DataFrame """
        if preprocess is True:
            preprocess = self.preprocess_query
        if callable(preprocess):
            query = preprocess(query)
        top_docs = self.search(query, min_relevance=min_relevance, limit=limit)
        return self.prettify_search_results(top_docs, limit=limit)

    def cli(self, preprocess=True):
        while True:
            query = input("Enter search query ([ENTER] or 'exit' to quit): ")
            if query.lower().strip() in ("exit", "exit()", "quit", "quit()", ""):
                break
            if preprocess is True:
                preprocess = self.preprocess_query
            if callable(preprocess):
                query = preprocess(query)
            top_docs = self.search(query)
            self.pretty_print(top_docs)


def update_votes(df, votes, filepath=DATA_DIR / 'votes.jsonl'):
    with jsl.open(filepath, mode='a') as writer:
        for v in votes:
            writer.write(dict(
                vote=v, ))


def main(df_path=None, embeddings=None, refresh=False):
    df_path = Path(df_path or DF_PATH)
    print(f"Starting script with corpus {df_path}, embeddings {embeddings}, and refresh={refresh}.")

    embeddings_path = Path(embeddings or df_path).with_suffix('.embeddings.joblib')
    embeddings_path.parent.mkdir(exist_ok=True)
    df_path.parent.mkdir(exist_ok=True)
    db = VectorDB(df=df_path, embeddings=embeddings_path, refresh=refresh)

    db.cli()
    return db


parser = argparse.ArgumentParser(
    prog="search_engine",
    description='A command line semantic search engine and RAM "database".',
    epilog="by Ethan Cavill with support from Hobson Lane",


)
# parser.add_argument("corpus_dir")
parser.add_argument("-r", "--refresh", action="store_true")
parser.add_argument("-c", "--cache", default=DATA_DIR / "cache" / "nutrition_sentences.csv")
for i in range(1, 11):
    parser.add_argument(f"-{i}", f"--downvote{i}", action="store_true", default=None)

if __name__ == "__main__":
    argv = sys.argv[1:]
    i = 0
    flags = []
    votes = []
    for i, a in enumerate(argv):
        if a[0] not in '-+':
            break
        m = re.match(r'[-+]\d', a)
        if m:
            votes.append(float(a))
            continue
        flags.append(a)
    args = parser.parse_args(flags)
    query = ' '.join(argv[i:])
    db = main(refresh=args.refresh)
    db.pretty_search()
