"""
BM25 Search Implementation as a baseline for comparison
Uses rank_bm25 library for efficient BM25 retrieval
"""

from rank_bm25 import BM25Okapi
from preprocessing import preprocess_text


class BM25Index:
    def __init__(self, corpus):
        """
        Initialize BM25 index

        Args:
            corpus: Either
                - a list of document dicts as returned by
                  corpus_parser.parse_corpus(), each with
                  "doc_id", "title", "category", "text", or
                - a dict of doc_id -> text (kept for backward
                  compatibility).
        """
        if isinstance(corpus, dict):
            documents = []
            for doc_id, doc_data in corpus.items():
                if isinstance(doc_data, dict):
                    doc_copy = doc_data.copy()
                    doc_copy.setdefault("doc_id", doc_id)
                    documents.append(doc_copy)
                else:
                    documents.append({"doc_id": doc_id, "text": str(doc_data)})
        else:
            documents = corpus

        self.doc_ids = [document["doc_id"] for document in documents]
        self.doc_map = {document["doc_id"]: document for document in documents}

        # Preprocess all documents
        self.tokenized_docs = [
            preprocess_text(document.get("text", ""))
            for document in documents
        ]

        # Initialize BM25
        self.bm25 = BM25Okapi(self.tokenized_docs)

    def search(self, query, top_k=10):
        """
        Search using BM25 ranking

        Args:
            query: Search query string
            top_k: Number of top results to return

        Returns:
            List of dicts: doc_id, title, category, score, text (preview)
        """
        # Preprocess query using same pipeline as documents
        query_tokens = preprocess_text(query)

        # Get BM25 scores for all documents
        scores = self.bm25.get_scores(query_tokens)

        # Get top-k results
        top_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        results = []
        for idx in top_indices:
            if scores[idx] > 0:  # Only include documents with positive scores
                doc_id = self.doc_ids[idx]
                document = self.doc_map[doc_id]
                text = document.get("text", "")
                results.append({
                    'doc_id': doc_id,
                    'title': document.get("title", ""),
                    'category': document.get("category", ""),
                    'score': float(scores[idx]),
                    'text': (text[:200] + '...') if len(text) > 200 else text
                })

        return results
