from rapidfuzz import fuzz

def search(query, entries):
    if not query.strip():
        return entries

    result = []
    q = query.lower()

    for e in entries:
        text = (e[1] + " " + (e[2] or "")).lower()
        score = fuzz.partial_ratio(q, text)

        if score > 30:
            result.append((score, e))

    result.sort(key=lambda x: x[0], reverse=True)
    return [e for score, e in result]
