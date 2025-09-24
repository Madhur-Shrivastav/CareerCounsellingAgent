from typing import List, Dict
from sentence_transformers import SentenceTransformer
from supabase import create_client, Client

MODEL_NAME = "thenlper/gte-small"
model = SentenceTransformer(MODEL_NAME)

SUPABASE_URL ="https://puvdowgomntylrisiofy.supabase.co"
SUPABASE_KEY ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1dmRvd2dvbW50eWxyaXNpb2Z5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1ODYyMDQ5MywiZXhwIjoyMDc0MTk2NDkzfQ.0v25PaC4E9H8S2poti4U6-tSEnuajArMn6lwcZld_Ds"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def search_documents(
    query: str,
    match_count: int = 5,
    min_similarity: float = 0.7
) -> List[Dict]:

    query_vector_embeddings = model.encode([query], normalize_embeddings=True)[0].astype("float32").tolist()

    resp = supabase.rpc(
        "match_documents",
        {
            "query_embedding": query_vector_embeddings,
            "match_count": match_count,
            "min_similarity": min_similarity,
        },
    ).execute()

    return resp.data or []


if __name__ == "__main__":
    results = search_documents("Top engineering colleges in India")
    for i, row in enumerate(results, start=1):
        print(f"Result {i}")
        print(f"  Similarity: {row['similarity']:.3f}")
        print(f"  Chunk ID : {row['chunk_id']}")
        print(f"  Content  : {row['content'][:200]}...")
        print()
