
import os
import json
import numpy as np
from supabase import create_client, Client

# ---------- Config ----------
EMBEDDINGS_PATH = "embeddings.npy"
METADATA_PATH = "metadata.jsonl"
TABLE_NAME = "documents"   # change if your table name differs
BATCH_SIZE = 300           # tune: 200-1000 is typical

# ---------- Supabase client ----------
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]  
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def load_metadata_jsonl(path):
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                items.append(json.loads(line))
    return items

def chunked(iterable, n):
    for i in range(0, len(iterable), n):
        yield iterable[i:i+n]

def main():
    embeddings = np.load(EMBEDDINGS_PATH, mmap_mode=None)  
    if embeddings.ndim != 2:
        raise ValueError(f"Expected 2D array, got shape {embeddings.shape}")
    num_rows, dim = embeddings.shape
    print(f"Loaded embeddings: {embeddings.shape}")
    metadata = load_metadata_jsonl(METADATA_PATH)
    print(f"Loaded metadata lines: {len(metadata)}")

    if len(metadata) != num_rows:
        raise ValueError(
            f"Row count mismatch: metadata={len(metadata)} vs embeddings={num_rows}. "
            "They must align 1:1 in the same order."
        )

    total_inserted = 0
    for start in range(0, num_rows, BATCH_SIZE):
        end = min(start + BATCH_SIZE, num_rows)
        batch_rows = []
        embs = embeddings[start:end].astype("float32") 
        metas = metadata[start:end]

        for md, emb in zip(metas, embs):
            batch_rows.append({
                "chunk_id": md.get("chunk_id"),
                "content": md.get("text"),
                "embedding": emb.tolist(),   
            })
            print(md.get("chunk_id"))

        try:
            response = (
                supabase.table(TABLE_NAME)
                .insert(batch_rows)
                .execute()
            )
            return response
        except Exception as exception:
            return exception

    print(f"Done. Inserted {total_inserted} rows into '{TABLE_NAME}'.")

if __name__ == "__main__":
    print(main())
