import sys
from pathlib import Path

import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import TABLE_NAME
from app.db import DB
from app.embedder import Embedder

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def read_pdf(path):
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    return "\n".join(pages)


def clean(text):
    return text.replace("(cid:127)", "-").replace("\n[]", "")


def chunk(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_text(text)


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: python -m scripts.resume_to_db <path-to-pdf>")

    path = Path(sys.argv[1])
    if not path.is_file():
        sys.exit(f"file not found: {path}")

    text = clean(read_pdf(path))
    if not text.strip():
        sys.exit(f"no text extracted from {path}")

    chunks = chunk(text)
    print(f"{path.name}: {len(text)} chars -> {len(chunks)} chunks")

    # embed first, so a model failure leaves the existing rows alone
    embedder = Embedder()
    vectors = embedder.encode_many(chunks)
    print(f"embedded {len(vectors)} vectors of {len(vectors[0])} dimensions")

    db = DB()
    removed = db.delete(f"DELETE FROM {TABLE_NAME}")
    written = db.insert(
        f"INSERT INTO {TABLE_NAME} (content, embedding) VALUES (%s, %s)",
        list(zip(chunks, vectors)),
    )
    print(f"removed {removed} old rows, wrote {written} new rows")

    total = db.fetchone(f"SELECT count(*) AS n FROM {TABLE_NAME}")["n"]
    if total != len(chunks):
        sys.exit(f"expected {len(chunks)} rows, found {total}")

    print(f"done: {total} rows in {TABLE_NAME}")


if __name__ == "__main__":
    main()
