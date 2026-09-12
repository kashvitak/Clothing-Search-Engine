import math

from corpus_parser import parse_corpus
from inverted_index import build_inverted_index
from preprocessing import preprocess


def calculate_document_weights(document, index):
    """
    Calculate lnc weights for one document.

    lnc:
        l = logarithmic TF
        n = no IDF
        c = cosine normalization

    Raw weight:
        1 + log10(tf)

    Returns:
        Dictionary containing:
        {
            term: normalized_weight
        }
    """

    doc_id = document["doc_id"]

    # Preprocess the document
    tokens = preprocess(document["text"])

    # Count term frequencies
    term_frequencies = {}

    for token in tokens:
        term_frequencies[token] = term_frequencies.get(token, 0) + 1

    # Calculate raw lnc weights
    raw_weights = {}

    for term, tf in term_frequencies.items():

        weight = 1 + math.log10(tf)

        raw_weights[term] = weight

    # Calculate vector length
    vector_length = math.sqrt(
        sum(weight ** 2 for weight in raw_weights.values())
    )

    # Normalize
    normalized_weights = {}

    for term, weight in raw_weights.items():

        normalized_weights[term] = weight / vector_length

    return normalized_weights

def calculate_query_weights(query, index, N):
    """
    Calculate ltc weights for a query.

    ltc:
        l = logarithmic TF
        t = IDF
        c = cosine normalization

    Query weight:
        (1 + log10(tf)) * log10(N / df)

    Returns:
        Dictionary containing normalized query weights.
    """

    # Preprocess the query
    tokens = preprocess(query)

    # Calculate query term frequencies
    term_frequencies = {}

    for token in tokens:
        term_frequencies[token] = (
            term_frequencies.get(token, 0) + 1
        )

    raw_weights = {}

    for term, tf in term_frequencies.items():

        # Ignore terms that don't exist in the corpus
        if term not in index:
            continue

        df = index[term]["df"]

        # Logarithmic TF
        tf_weight = 1 + math.log10(tf)

        # IDF
        idf = math.log10(N / df)

        # ltc weight
        raw_weights[term] = tf_weight * idf

    # If none of the query terms exist in the corpus
    if not raw_weights:
        return {}
    
    vector_length = math.sqrt(
        sum(weight ** 2 for weight in raw_weights.values())
    )
    
    if vector_length == 0:
        return {}
    
    normalized_weights = {}
    
    for term, weight in raw_weights.items():
        normalized_weights[term] = weight / vector_length
    
    return normalized_weights
    
    


def cosine_similarity(query_weights, document_weights):
    """
    Calculate cosine similarity between a normalized
    query vector and a normalized document vector.

    Since both vectors are already normalized,
    cosine similarity is simply their dot product.
    """

    score = 0.0

    # Only terms present in both vectors contribute
    for term, query_weight in query_weights.items():

        if term in document_weights:
            score += query_weight * document_weights[term]

    return score


def search(query, documents, index):
    """
    Search the corpus using lnc.ltc cosine similarity.

    Returns up to 10 documents sorted by:
    1. Descending cosine similarity
    2. Increasing docID for ties
    """

    N = len(documents)

    # Calculate query vector
    query_weights = calculate_query_weights(
        query,
        index,
        N
    )

    # No query terms exist in the corpus
    if not query_weights:
        return []

    results = []

    # Compare query against every document
    for document in documents:

        document_weights = calculate_document_weights(
            document,
            index
        )

        score = cosine_similarity(
            query_weights,
            document_weights
        )

        if score > 0:

         results.append({
            "doc_id": document["doc_id"],
            "title": document["title"],
            "category": document["category"],
            "score": score
        })

    # Sort:
    # 1. Highest score first
    # 2. Lowest docID first when scores are tied
    results.sort(
        key=lambda result: (
            -result["score"],
            result["doc_id"]
        )
    )

    # Return top 10
    return results[:10]

if __name__ == "__main__":

    documents = parse_corpus("C:\\Users\\Kashvi Tak\\OneDrive\\Desktop\\Clothing-Search-Engine\\data\\corpus_100.txt")

    index = build_inverted_index(documents)

    query = "cotton shirt"

    results = search(
        query,
        documents,
        index
    )

    print("Query:", query)

    print("\nTop results:")

    for rank, result in enumerate(results, start=1):

        print(
            f"{rank}. "
            f"{result['doc_id']} | "
            f"{result['title']} | "
            f"{result['score']:.6f}"
        )
    class VSM:
    """
    Compatibility wrapper class for VSM functions so it matches app.py
    """
    def __init__(self, corpus, inverted_index):
        self.corpus = corpus
        self.inverted_index = inverted_index

    def search(self, query, top_k=10):
        # Calls the existing search function in vsm.py
        results = search(query, self.corpus, self.inverted_index)
        if isinstance(results, list):
            return results[:top_k]
        return results
