from collections import defaultdict

from corpus_parser import parse_corpus
from preprocessing import preprocess


def build_positional_index(documents):
    index = defaultdict(lambda: {
        "df": 0,
        "postings": {}
    })

    for document in documents:
        doc_id = document["doc_id"]
        tokens = preprocess(document["text"])

        # Count each term once per document for document frequency.
        unique_terms = set(tokens)

        for term in unique_terms:
            index[term]["df"] += 1

        # Store term frequency and every position.
        for position, term in enumerate(tokens):
            if doc_id not in index[term]["postings"]:
                index[term]["postings"][doc_id] = {
                    "tf": 0,
                    "positions": []
                }

            index[term]["postings"][doc_id]["tf"] += 1
            index[term]["postings"][doc_id]["positions"].append(position)

    return dict(index)


def phrase_search(phrase, index):
    """
    Return documents where all processed query terms occur
    consecutively and in the same order as the query.

    Example:
        "cotton shirt"

    requires:
        cotton at position p
        shirt at position p + 1
    """

    tokens = preprocess(phrase)

    if not tokens:
        return []

    # Single-term phrase.
    if len(tokens) == 1:
        term = tokens[0]

        if term not in index:
            return []

        results = []

        for doc_id, posting in index[term]["postings"].items():
            results.append({
                "doc_id": doc_id,
                "positions": {
                    term: posting["positions"]
                }
            })

        return sorted(
            results,
            key=lambda result: result["doc_id"]
        )

    # All query terms must exist in the index.
    for term in tokens:
        if term not in index:
            return []

    # Find documents containing every query term.
    candidate_docs = set(
        index[tokens[0]]["postings"].keys()
    )

    for term in tokens[1:]:
        candidate_docs &= set(
            index[term]["postings"].keys()
        )

    matching_docs = []

    for doc_id in candidate_docs:

        first_term = tokens[0]

        first_positions = index[first_term]["postings"][
            doc_id
        ]["positions"]

        for start_position in first_positions:

            matched_positions = {
                first_term: [start_position]
            }

            match = True

            for offset, term in enumerate(
                tokens[1:],
                start=1
            ):
                target_position = start_position + offset

                term_positions = index[term]["postings"][
                    doc_id
                ]["positions"]

                if target_position not in term_positions:
                    match = False
                    break

                matched_positions[term] = [
                    target_position
                ]

            if match:
                matching_docs.append({
                    "doc_id": doc_id,
                    "positions": matched_positions
                })

                # One exact phrase match is enough
                # to include the document.
                break

    return sorted(
        matching_docs,
        key=lambda result: result["doc_id"]
    )


def proximity_search(term1, term2, k, index):
    """
    Find documents where term2 occurs after term1
    and the positional distance is at most k.

    Example:
        cotton WITHIN/3 shirt

    means:

        0 < position(shirt) - position(cotton) <= 3

    The search is ordered: term1 must occur before term2.
    """

    if k < 1:
        return []

    tokens1 = preprocess(term1)
    tokens2 = preprocess(term2)

    if not tokens1 or not tokens2:
        return []

    # Proximity endpoint expects one term for each input.
    term1 = tokens1[0]
    term2 = tokens2[0]

    if term1 not in index or term2 not in index:
        return []

    docs1 = set(
        index[term1]["postings"].keys()
    )

    docs2 = set(
        index[term2]["postings"].keys()
    )

    candidate_docs = docs1 & docs2

    matching_docs = []

    for doc_id in candidate_docs:

        positions1 = index[term1]["postings"][
            doc_id
        ]["positions"]

        positions2 = index[term2]["postings"][
            doc_id
        ]["positions"]

        matches = []

        for pos1 in positions1:
            for pos2 in positions2:

                distance = pos2 - pos1

                if 0 < distance <= k:
                    matches.append({
                        term1: pos1,
                        term2: pos2,
                        "distance": distance
                    })

        if matches:
            matching_docs.append({
                "doc_id": doc_id,
                "matches": matches
            })

    return sorted(
        matching_docs,
        key=lambda result: result["doc_id"]
    )


if __name__ == "__main__":
    documents = parse_corpus("../data/corpus_100.txt")

    positional_index = build_positional_index(
        documents
    )

    print("Number of documents:", len(documents))
    print(
        "Number of unique terms:",
        len(positional_index)
    )

    print("\nSample positional index entries:")

    for term in sorted(positional_index.keys())[:10]:
        print(
            term,
            "-> df:",
            positional_index[term]["df"],
            "postings:",
            positional_index[term]["postings"]
        )

    print("\nPhrase search: cotton shirt")
    print(
        phrase_search(
            "cotton shirt",
            positional_index
        )
    )

    print("\nProximity search: cotton WITHIN/3 shirt")
    print(
        proximity_search(
            "cotton",
            "shirt",
            3,
            positional_index
        )
    )