import os

from corpus_parser import parse_corpus
from inverted_index import build_inverted_index
from positional_index import build_positional_index


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CORPUS_PATH = os.path.join(
    BASE_DIR,
    "data",
    "corpus_100.txt"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "output"
)


def write_inverted_index(index, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("INVERTED INDEX\n")
        file.write("=" * 80 + "\n\n")

        for term in sorted(index.keys()):
            df = index[term]["df"]
            postings = index[term]["postings"]

            file.write(f"TERM: {term}\n")
            file.write(f"DF: {df}\n")
            file.write("POSTINGS: ")

            posting_list = []

            for doc_id in sorted(postings.keys()):
                tf = postings[doc_id]
                posting_list.append(f"({doc_id}, {tf})")

            file.write(", ".join(posting_list))
            file.write("\n\n")


def write_positional_index(index, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("POSITIONAL INDEX\n")
        file.write("=" * 80 + "\n\n")

        for term in sorted(index.keys()):
            df = index[term]["df"]
            postings = index[term]["postings"]

            file.write(f"TERM: {term}\n")
            file.write(f"DF: {df}\n")
            file.write("POSTINGS: ")

            posting_list = []

            for doc_id in sorted(postings.keys()):
                tf = postings[doc_id]["tf"]
                positions = postings[doc_id]["positions"]

                posting_list.append(
                    f"({doc_id}, {tf}, {positions})"
                )

            file.write(", ".join(posting_list))
            file.write("\n\n")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Reading corpus...")
    documents = parse_corpus(CORPUS_PATH)

    print(f"Documents loaded: {len(documents)}")

    print("Building inverted index...")
    inverted_index = build_inverted_index(documents)

    print("Building positional index...")
    positional_index = build_positional_index(documents)

    inverted_output = os.path.join(
        OUTPUT_DIR,
        "inverted_index.txt"
    )

    positional_output = os.path.join(
        OUTPUT_DIR,
        "positional_index.txt"
    )

    print("Writing inverted index...")
    write_inverted_index(
        inverted_index,
        inverted_output
    )

    print("Writing positional index...")
    write_positional_index(
        positional_index,
        positional_output
    )

    print("\nIndex files generated successfully!")
    print(f"Documents: {len(documents)}")
    print(f"Unique terms: {len(inverted_index)}")
    print(f"\nCreated:")
    print(inverted_output)
    print(positional_output)


if __name__ == "__main__":
    main()