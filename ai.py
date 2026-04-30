from sentence_transformers import SentenceTransformer, util

# CPU固定
model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2",
    device="cpu"
)

def ai_search(query, entries):
    if not entries:
        return []

    texts = [
        f"{e[1]} {e[2]} {e[3]}"
        for e in entries
    ]

    embeddings = model.encode(texts, convert_to_tensor=True)
    query_vec = model.encode(query, convert_to_tensor=True)

    scores = util.cos_sim(query_vec, embeddings)[0]

    ranked = sorted(
        zip(entries, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [(e[0], float(s)) for e, s in ranked]
