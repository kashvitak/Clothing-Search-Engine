from collections import defaultdict, Counter

from corpus_parser import parse_corpus
from preprocessing import preprocess


def build_inverted_index(documents):
    """
    Build an inverted index.

    Structure:

    {
        "term": {
            "df": number_of_documents,
            "postings": {
                "D001": term_frequency,
                "D002": term_frequency,
                ...
            }
        }
    }
    """

    index = defaultdict(lambda: {
        "df": 0,
        "postings": {}
    })

    for document in documents:

        doc_id = document["doc_id"]

        # Preprocess document text
        tokens = preprocess(document["text"])

        # Count term frequency within this document
        term_counts = Counter(tokens)

        for term, tf in term_counts.items():

            # Store TF for this document
            index[term]["postings"][doc_id] = tf

            # Since this term appears in this document,
            # increase document frequency by 1
            index[term]["df"] += 1

    return dict(index)


if __name__ == "__main__":

    # Read corpus
    documents = parse_corpus("../data/corpus_100.txt")

    # Build index
    index = build_inverted_index(documents)

    print("Number of documents:", len(documents))
    print("Number of unique terms:", len(index))

    # Display a few terms
    print("\nSample dictionary entries:")

    for term in sorted(index.keys())[:20]:

        print(
            term,
            "-> df:",
            index[term]["df"],
            "postings:",
            index[term]["postings"]
        )