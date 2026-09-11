from corpus_parser import parse_corpus
from inverted_index import build_inverted_index
from vsm import search


# Load corpus
documents = parse_corpus("../data/corpus_100.txt")

# Build inverted index
index = build_inverted_index(documents)


# At least 10 free-text queries
queries = [
    "cotton shirt",
    "denim jeans",
    "winter jacket",
    "formal trousers",
    "casual wear",
    "printed dress",
    "sports shoes",
    "leather bag",
    "summer top",
    "hoodie",
    "breathable fabric",
    "zip closure",
    "xyzabc",
    "regular fit"
]


for query in queries:

    print("\n" + "=" * 80)
    print("QUERY:", query)
    print("=" * 80)

    results = search(
        query,
        documents,
        index
    )

    if not results:
        print("No matching documents found.")
        continue

    for rank, result in enumerate(results, start=1):

        print(
            f"{rank:2}. "
            f"{result['doc_id']} | "
            f"{result['title']} | "
            f"{result['score']:.6f}"
        )