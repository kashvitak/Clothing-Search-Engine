from corpus_parser import parse_corpus
from inverted_index import build_inverted_index
from vsm import search
from positional_index import (
    build_positional_index,
    phrase_search,
    proximity_search
)


def print_separator():
    print("=" * 80)


def test_vsm(documents, inverted_index):
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
        "regular fit",
        "xyzabc"
    ]

    print_separator()
    print("PART B: VECTOR SPACE MODEL TESTS")
    print_separator()

    for query in queries:
        print(f"\nQUERY: {query}")
        print("-" * 80)

        results = search(
            query,
            documents,
            inverted_index
        )

        if not results:
            print("No matching documents.")
            continue

        for rank, result in enumerate(results, start=1):
            print(
                f"{rank:2}. "
                f"{result['doc_id']} | "
                f"{result['title']} | "
                f"{result['score']:.6f}"
            )


def test_phrase_search(positional_index):
    phrases = [
        "cotton shirt",
        "stretch denim",
        "festive wear",
        "winter wear",
        "regular fit"
    ]

    print_separator()
    print("PART C: EXACT PHRASE SEARCH TESTS")
    print_separator()

    for phrase in phrases:
        print(f"\nPHRASE: \"{phrase}\"")
        print("-" * 80)

        results = phrase_search(
            phrase,
            positional_index
        )

        if not results:
            print("No exact phrase matches.")
            continue

        print(f"Matching documents: {len(results)}")

        for result in results:
            print(
                f"{result['doc_id']} | "
                f"positions: {result['positions']}"
            )


def test_proximity_search(positional_index):
    tests = [
        ("cotton", "shirt", 2),
        ("cotton", "shirt", 3),
        ("stretch", "denim", 4),
        ("winter", "wear", 3),
        ("festive", "kurta", 4)
    ]

    print_separator()
    print("PART C: PROXIMITY SEARCH TESTS")
    print_separator()

    for term1, term2, k in tests:
        print(
            f"\nQUERY: {term1} WITHIN/{k} {term2}"
        )
        print("-" * 80)

        results = proximity_search(
            term1,
            term2,
            k,
            positional_index
        )

        if not results:
            print("No proximity matches.")
            continue

        print(f"Matching documents: {len(results)}")

        for result in results:
            print(f"\n{result['doc_id']}")

            for match in result["matches"]:
                print(
                    f"  {term1}: {match[term1]} | "
                    f"{term2}: {match[term2]} | "
                    f"distance: {match['distance']}"
                )


def main():
    corpus_path = "C:\\Users\\Kashvi Tak\\OneDrive\\Desktop\\Clothing-Search-Engine\\data\\corpus_100.txt"

    print("Loading corpus...")
    documents = parse_corpus(corpus_path)

    print(f"Documents loaded: {len(documents)}")

    print("\nBuilding inverted index...")
    inverted_index = build_inverted_index(documents)

    print("Building positional index...")
    positional_index = build_positional_index(documents)

    print("\nIndex construction complete.")

    test_vsm(
        documents,
        inverted_index
    )

    test_phrase_search(
        positional_index
    )

    test_proximity_search(
        positional_index
    )

    print_separator()
    print("ALL TESTS COMPLETED")
    print_separator()


if __name__ == "__main__":
    main()