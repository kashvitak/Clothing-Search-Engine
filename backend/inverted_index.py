from collections import defaultdict, Counter
from corpus_parser import parse_corpus
from preprocessing import preprocess

class InvertedIndex:
    """
    Inverted Index class that builds and stores the index structure:
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
    def __init__(self, corpus):
        if isinstance(corpus, dict):
            documents = []
            for doc_id, doc_data in corpus.items():
                if isinstance(doc_data, dict):
                    doc_copy = doc_data.copy()
                    if 'doc_id' not in doc_copy:
                        doc_copy['doc_id'] = doc_id
                    documents.append(doc_copy)
                else:
                    documents.append({"doc_id": doc_id, "text": str(doc_data)})
        else:
            documents = corpus

        self.index = self._build_inverted_index(documents)

    def _build_inverted_index(self, documents):
        index = defaultdict(lambda: {
            "df": 0,
            "postings": {}
        })

        for document in documents:
            doc_id = document.get("doc_id") or document.get("id")
            text = document.get("text") or document.get("description") or ""
            
            if not doc_id:
                continue

            # Preprocess document text
            tokens = preprocess(text)

            # Count term frequency within this document
            term_counts = Counter(tokens)

            for term, tf in term_counts.items():
                index[term]["postings"][doc_id] = tf
                index[term]["df"] += 1

        return dict(index)

    def __getitem__(self, term):
        return self.index.get(term, {"df": 0, "postings": {}})

    def get(self, term, default=None):
        return self.index.get(term, default)

    def keys(self):
        return self.index.keys()

    def items(self):
        return self.index.items()

    def __len__(self):
        return len(self.index)
        
    def build_inverted_index(documents):
        """Compatibility helper for modules expecting the old function name"""
        index_obj = InvertedIndex(documents)
        return index_obj.index
