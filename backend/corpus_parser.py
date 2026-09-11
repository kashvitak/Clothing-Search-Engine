import re


def parse_corpus(file_path):
    documents = []

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Find every <DOC> ... </DOC> block
    doc_blocks = re.findall(r"<DOC>(.*?)</DOC>", content, re.DOTALL)

    for block in doc_blocks:

        doc_id = re.search(r"<DOCID>(.*?)</DOCID>", block, re.DOTALL)
        category = re.search(r"<CATEGORY>(.*?)</CATEGORY>", block, re.DOTALL)
        title = re.search(r"<TITLE>(.*?)</TITLE>", block, re.DOTALL)
        text = re.search(r"<TEXT>(.*?)</TEXT>", block, re.DOTALL)

        document = {
            "doc_id": doc_id.group(1).strip(),
            "category": category.group(1).strip(),
            "title": title.group(1).strip(),
            "text": text.group(1).strip()
        }

        documents.append(document)

    return documents


if __name__ == "__main__":

    documents = parse_corpus("../data/corpus_100.txt")

    print("Number of documents:", len(documents))

    print("\nFirst document:")
    print(documents[0])