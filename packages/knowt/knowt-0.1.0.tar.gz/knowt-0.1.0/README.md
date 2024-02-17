
# Text Search Engine

This project implements a simple text search engine using Python. 
It processes text files to create a searchable index of sentences, allowing users to perform semantic searches against this indexed data.
See the project [final report](docs/Information Retrieval Systems.pdf) for more details.

## Installation

#### Python virtual environment

To set up the project environment, follow these steps:

1. Clone the project repository or download the project files to your local machine.
2. Navigate to the project directory.
3. Create a Python virtual environment in the project directory:
   ```bash
   pip install virtualenv
   python -m virtualenv .venv
   ```
4. Activate the virtual environment (mac/linux):
   ```bash
   source .venv/bin/activate
   ```

#### Install dependencies

Not that you have a virtual environment, you're ready to install some Python packages and download language models (spaCy and BERT).

1. Install the required packages using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```
2. Download the small spaCy language model (for sentence segmentation):
   ```bash
   python -m spacy download en_core_web_sm
   ```
3. Download the small BERT embedding model:
   ```bash
   python -c 'from sentence_transformers import SentenceTransformer; sbert = SentenceTransformer("paraphrase-MiniLM-L6-v2")'
   ```

#### Quick start

You can search an example corpus of nutrition and health documents by running the `search_engine.py` script.

#### Search your personal docs

1. Replace the text files in `data/corpus` with your own.
2. Start the command-line search engine with:
   ```bash
   python search_engine.py --refresh
   ```

The `--refresh` flag ensures that a fresh index is created based on your documents.
Otherwise it may ignore the `data/corpus` directory and reuse an existing index and corpus in the `data/cache` directory.

The `search_engine.py` script will first segement the text files into sentences.
Then it will create an inverse index to provide context for any retrieved information.
It will also create embedding vectors and locality sensitive hashes for experimenting with vector database and RAG (retrieval augmented generation)
then allow you to process search requests, returning the top matching sentences along with their filenames and line numbers.

## Contributing

Contributions to this project are welcome.

## License

This project is licensed under [MIT License](LICENSE).
