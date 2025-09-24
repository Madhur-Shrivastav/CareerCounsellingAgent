
"""
Recursive text embedding pipeline using SentenceTransformer (thenlper/gte-small)

Features:
- Recursively collect all .txt files under a root directory
- Read file contents with encoding fallbacks
- Chunk text into overlapping windows (word-based)
- Batch-encode chunks into embeddings with sentence-transformers
- Save embeddings to .npy and metadata to .jsonl
- Optional demo: compute similarity matrix for sample sentences

Usage:
    python embed_txt_corpus.py \
        --root_dir ./data \
        --chunk_size 200 \
        --overlap 50 \
        --batch_size 64 \
        --output_embeddings embeddings.npy \
        --output_metadata metadata.jsonl \
        --show_progress
"""

import os
import io
import json
import argparse
from typing import List, Dict, Generator, Tuple
import numpy as np

try:
    from sentence_transformers import SentenceTransformer, util as st_util
except ImportError:
    raise SystemExit(
        "Please install sentence-transformers:\n"
        "  pip install -U sentence-transformers\n"
        "Then re-run this script."
    )


def iter_txt_files(root_dir: str) -> Generator[str, None, None]:
    """Yield absolute paths to .txt files under root_dir recursively."""
    for dirpath, _, filenames in os.walk(root_dir):
        for name in filenames:
            if name.lower().endswith(".txt"):
                yield os.path.join(dirpath, name)


def read_text_file(path: str) -> str:
    """Read a text file robustly with encoding fallbacks."""
    # Try UTF-8 first
    try:
        with io.open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        pass

    # Fallback: try common encodings
    for enc in ("utf-16", "latin-1", "cp1252"):
        try:
            with io.open(path, "r", encoding=enc, errors="strict") as f:
                return f.read()
        except UnicodeDecodeError:
            continue

    # Last resort with replacement to avoid crashes (data-loss possible)
    with io.open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

def chunk_text_words(
    text: str,
    chunk_size: int = 200,
    overlap: int = 50,
    min_words: int = 1
) -> List[Dict]:
    """
    Split text by words into overlapping chunks.

    Parameters:
        text: raw text
        chunk_size: words per chunk
        overlap: words of overlap between consecutive chunks
        min_words: skip chunks shorter than this (after stripping)

    Returns:
        List of dicts: [{"text": str, "start_word": int, "end_word": int}, ...]
    """
    # Normalize whitespace
    words = text.split()
    n = len(words)
    if n == 0:
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    i = 0
    while i < n:
        j = min(i + chunk_size, n)
        piece_words = words[i:j]
        if len(piece_words) >= min_words:
            chunks.append({
                "text": " ".join(piece_words),
                "start_word": i,
                "end_word": j
            })
        if j == n:
            break
        i = j - overlap  # move forward with overlap

    return chunks


def embed_chunks(
    model_name: str,
    chunk_texts: List[str],
    batch_size: int = 64,
    show_progress: bool = False,
    normalize: bool = True
) -> np.ndarray:
    """
    Encode a list of chunk texts into embeddings using SentenceTransformer.

    Returns:
        np.ndarray of shape (num_chunks, dim)
    """
    model = SentenceTransformer(model_name)
    embeddings = model.encode(
        chunk_texts,
        batch_size=batch_size,
        show_progress_bar=show_progress,
        convert_to_numpy=True,
        normalize_embeddings=normalize
    )
    return embeddings


def build_corpus_embeddings(
    root_dir: str,
    model_name: str = "thenlper/gte-small",
    chunk_size: int = 200,
    overlap: int = 50,
    batch_size: int = 64,
    show_progress: bool = False,
    output_embeddings: str = "embeddings.npy",
    output_metadata: str = "metadata.jsonl"
) -> Tuple[np.ndarray, List[Dict]]:
    """
    Recursively process .txt files under root_dir, chunk, and embed them.

    Saves:
        - embeddings.npy: NumPy array of embeddings
        - metadata.jsonl: one JSON object per line with {file_path, chunk_id, text, start_word, end_word}

    Returns:
        (embeddings, metadata)
    """
    all_chunk_texts: List[str] = []
    metadata: List[Dict] = []

    file_count = 0
    chunk_count = 0

    for path in iter_txt_files(root_dir):
        file_count += 1
        text = read_text_file(path)
        chunks = chunk_text_words(text, chunk_size=chunk_size, overlap=overlap, min_words=1)

        for idx, ch in enumerate(chunks):
            # Collect text for embedding
            all_chunk_texts.append(ch["text"])

            # Build metadata
            metadata.append({
                "file_path": os.path.abspath(path),
                "chunk_id": idx,
                "start_word": ch["start_word"],
                "end_word": ch["end_word"],
                "text": ch["text"]
            })

        chunk_count += len(chunks)

    if chunk_count == 0:
        raise RuntimeError(f"No chunks produced from .txt files in: {root_dir}")

    # Embed in one go (if memory allows); otherwise you can stream in batches
    embeddings = embed_chunks(
        model_name=model_name,
        chunk_texts=all_chunk_texts,
        batch_size=batch_size,
        show_progress=show_progress,
        normalize=True
    )

    # Save to disk
    np.save(output_embeddings, embeddings)

    with open(output_metadata, "w", encoding="utf-8") as f:
        for md in metadata:
            f.write(json.dumps(md, ensure_ascii=False) + "\n")

    print(f"Processed {file_count} files, created {chunk_count} chunks.")
    print(f"Embeddings saved to: {output_embeddings}  (shape: {embeddings.shape})")
    print(f"Metadata saved to:   {output_metadata}    (lines: {len(metadata)})")

    return embeddings, metadata


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recursive text chunking & embeddings with SentenceTransformer.")
    parser.add_argument("--root_dir", type=str, required=True, help="Root directory containing .txt files (recursively).")
    parser.add_argument("--model_name", type=str, default="thenlper/gte-small", help="SentenceTransformer model name.")
    parser.add_argument("--chunk_size", type=int, default=200, help="Words per chunk.")
    parser.add_argument("--overlap", type=int, default=50, help="Word overlap between chunks.")
    parser.add_argument("--batch_size", type=int, default=64, help="Batch size for encoding.")
    parser.add_argument("--show_progress", action="store_true", help="Show progress bar during encoding.")
    parser.add_argument("--output_embeddings", type=str, default="embeddings.npy", help="Path to save embeddings (.npy).")
    parser.add_argument("--output_metadata", type=str, default="metadata.jsonl", help="Path to save metadata (.jsonl).")
    return parser.parse_args()


def main():
    args = parse_args()

    build_corpus_embeddings(
        root_dir=args.root_dir,
        model_name=args.model_name,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        batch_size=args.batch_size,
        show_progress=args.show_progress,
        output_embeddings=args.output_embeddings,
        output_metadata=args.output_metadata
    )



if __name__ == "__main__":
    main()
