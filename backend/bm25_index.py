"""
BM25 Search Implementation as a baseline for comparison
Uses rank_bm25 library for efficient BM25 retrieval
"""

from rank_bm25 import BM25Okapi
from preprocessing import preprocess_text

class BM25Index:
    def __init__(self, corpus_dict):
        """
        Initialize BM25 index
        
        Args:
            corpus_dict: Dictionary with doc_id -> document_text mapping
        """
        self.corpus_dict = corpus_dict
        self.doc_ids = list(corpus_dict.keys())
        
        # Preprocess all documents
        self.tokenized_docs = []
        for doc_id in self.doc_ids:
            tokens = preprocess_text(corpus_dict[doc_id])
            self.tokenized_docs.append(tokens)
        
        # Initialize BM25
        self.bm25 = BM25Okapi(self.tokenized_docs)
    
    def search(self, query, top_k=10):
        """
        Search using BM25 ranking
        
        Args:
            query: Search query string
            top_k: Number of top results to return
            
        Returns:
            List of tuples (doc_id, score, document_text)
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
                results.append({
                    'doc_id': doc_id,
                    'score': float(scores[idx]),
                    'text': self.corpus_dict[doc_id][:200] + '...'  # Preview text
                })
        
        return results
