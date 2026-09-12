import math

from corpus_parser import parse_corpus
from inverted_index import build_inverted_index
from preprocessing import preprocess


def calculate_document_weights(document, index):
    doc_id = document["doc_id"]
    tokens = preprocess(document["text"])

    term_frequencies = {}
    for token in tokens:
        term_frequencies[token] = term_frequencies.get(token, 0) + 1

    raw_weights = {}
    for term, tf in term_frequencies.items():
        weight = 1 + math.log10(tf)
        raw_weights[term] = weight

    vector_length = math.sqrt(sum(weight ** 2 for weight in raw_weights.values()))

    normalized_weights = {}
    for term, weight in raw_weights.items():
        normalized_weights[term] = weight / vector_length

    return normalized_weights


def calculate_query_weights(query, index, N):
    tokens = preprocess(query)

    term_frequencies = {}
    for token in tokens:
        term_frequencies[token] = term_frequencies.get(token, 0) + 1

    raw_weights = {}
    for term, tf in term_frequencies.items():
        if term not in index:
            continue

        df = index[term]["df"]
        tf_weight = 1 + math.log10(tf)
        idf = math.log10(N / df)
        raw_weights[term] = tf_weight * idf

    if not raw_weights:
        return {}

    vector_length = math.sqrt(sum(weight ** 2 for weight in raw_weights.values()))

    if vector_length == 0:
        return {}

    normalized_weights = {}
    for term, weight in raw_weights.items():
        normalized_weights[term] = weight / vector_length

    return normalized_weights


def cosine_similarity(query_weights, document_weights):
    score = 0.0
    for term, query_weight in query_weights.items():
        if term in document_weights:
            score += query_weight * document_weights[term]
    return score


def search(query, documents, index):
    N = len(documents)

    query_weights = calculate_query_weights(query, index, N)

    if not query_weights:
        return []

    results = []

    for document in documents:
        document_weights = calculate_document_weights(document, index)
        score = cosine_similarity(query_weights, document_weights)

        if score > 0:
            text = document.get("text", "")
            results.append({
                "doc_id": document["doc_id"],
                "title": document["title"],
                "category": document["category"],
                "score": score,
                "text": (text[:200] + "...") if len(text) > 200 else text
            })

    results.sort(key=lambda result: (-result["score"], result["doc_id"]))

    return results[:10]


if __name__ == "__main__":
    documents = parse_corpus("../data/corpus_100.txt")
    index = build_inverted_index(documents)
    query = "cotton shirt"
    results = search(query, documents, index)
    print("Query:", query)
    print("\nTop results:")
    for rank, result in enumerate(results, start=1):
        print(f"{rank}. {result['doc_id']} | {result['title']} | {result['score']:.6f}")
