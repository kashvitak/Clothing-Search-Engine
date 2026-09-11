from corpus_parser import parse_corpus
from inverted_index import build_inverted_index
from positional_index import (
    build_positional_index,
    phrase_search,
    proximity_search
)

documents = parse_corpus("../data/corpus_100.txt")

inverted_index = build_inverted_index(documents)
positional_index = build_positional_index(documents)

document_map = {
    document["doc_id"]: document
    for document in documents
}


# -----------------------------
# Exact Phrase Tests
# -----------------------------

phrase_queries = [
    "cotton shirt",
    "stretch denim",
    "festive wear",
    "winter wear",
    "regular fit"
]

print("\n" + "=" * 80)
print("EXACT PHRASE SEARCH TESTS")
print("=" * 80)

for phrase in phrase_queries:
    results = phrase_search(phrase, positional_index)

    print(f"\nQUERY: \"{phrase}\"")
    print("Matching documents:", len(results))

    for result in results:

        document = document_map[result["doc_id"]]
        print(
            f"{result['doc_id']} | "
            f"{document['title']} | "
            f"{result['positions']}"
        )


# -----------------------------
# Proximity Tests
# -----------------------------

proximity_queries = [
    ("cotton", "shirt", 2),
    ("cotton", "shirt", 3),
    ("stretch", "denim", 4),
    ("winter", "wear", 3),
    ("festive", "kurta", 4)
]

print("\n" + "=" * 80)
print("PROXIMITY SEARCH TESTS")
print("=" * 80)

for term1, term2, k in proximity_queries:
    results = proximity_search(
        term1,
        term2,
        k,
        positional_index
    )

    print(f"\nQUERY: {term1} WITHIN/{k} {term2}")
    print("Matching documents:", len(results))

    for result in results:
        document = document_map[result["doc_id"]]

        print(
            f"{result['doc_id']} | "
            f"{document['title']} | "
            f"{result['matches']}"
        )