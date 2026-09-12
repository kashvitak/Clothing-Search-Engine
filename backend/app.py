"""
Flask REST API for Clothing Search Engine
Supports: VSM (lnc.ltc), BM25 baseline, Phrase search, Proximity search
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

from corpus_parser import parse_corpus
from inverted_index import InvertedIndex
from vsm import search as vsm_search
from positional_index import (
    build_positional_index,
    phrase_search as run_phrase_search,
    proximity_search as run_proximity_search
)
from bm25_index import BM25Index

app = Flask(__name__)
CORS(app)

print("Loading corpus...")
documents = parse_corpus('../data/corpus_100.txt')
print(f"Loaded {len(documents)} documents")

print("Initializing indices...")
inverted_index = InvertedIndex(documents)
positional_idx = build_positional_index(documents)
bm25_index = BM25Index(documents)
print("Indices initialized!")

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'corpus_size': len(documents),
        'indices': ['vsm', 'bm25', 'inverted', 'positional']
    }), 200

@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    method = request.args.get('method', 'vsm').lower()
    top_k = request.args.get('top_k', 10, type=int)
    if not query:
        return jsonify({'error': 'Query parameter (q) is required'}), 400
    if method not in ['vsm', 'bm25']:
        return jsonify({'error': 'Method must be "vsm" or "bm25"'}), 400
    try:
        if method == 'bm25':
            results = bm25_index.search(query, top_k=top_k)
            return jsonify({'query': query, 'method': 'BM25', 'results': results, 'count': len(results), 'timestamp': None}), 200
        else:
            results = vsm_search(query, documents, inverted_index)[:top_k]
            return jsonify({'query': query, 'method': 'VSM (lnc.ltc)', 'results': results, 'count': len(results), 'timestamp': None}), 200
    except Exception as e:
        return jsonify({'error': f'Search failed: {str(e)}', 'query': query, 'method': method}), 500

@app.route('/api/compare', methods=['GET'])
def compare_methods():
    query = request.args.get('q', '').strip()
    top_k = request.args.get('top_k', 10, type=int)
    if not query:
        return jsonify({'error': 'Query parameter (q) is required'}), 400
    try:
        vsm_results = vsm_search(query, documents, inverted_index)[:top_k]
        bm25_results = bm25_index.search(query, top_k=top_k)
        return jsonify({
            'query': query,
            'vsm': {'method': 'VSM (lnc.ltc)', 'results': vsm_results, 'count': len(vsm_results)},
            'bm25': {'method': 'BM25', 'results': bm25_results, 'count': len(bm25_results)},
            'timestamp': None
        }), 200
    except Exception as e:
        return jsonify({'error': f'Comparison failed: {str(e)}', 'query': query}), 500

@app.route('/api/phrase', methods=['GET'])
def phrase_search():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': 'Query parameter (q) is required'}), 400
    try:
        results = run_phrase_search(query, positional_idx)
        return jsonify({'query': query, 'method': 'Phrase Search', 'results': results, 'count': len(results), 'type': 'phrase'}), 200
    except Exception as e:
        return jsonify({'error': f'Phrase search failed: {str(e)}', 'query': query}), 500

@app.route('/api/proximity', methods=['GET'])
def proximity_search():
    term1 = request.args.get('term1', '').strip()
    term2 = request.args.get('term2', '').strip()
    k = request.args.get('k', 5, type=int)
    if not term1 or not term2:
        return jsonify({'error': 'Both term1 and term2 parameters are required'}), 400
    if k < 0:
        return jsonify({'error': 'k must be a positive integer'}), 400
    try:
        results = run_proximity_search(term1, term2, k, positional_idx)
        return jsonify({
            'query': f'{term1} WITHIN {k} {term2}',
            'method': 'Proximity Search',
            'results': results,
            'count': len(results),
            'type': 'proximity',
            'parameters': {'term1': term1, 'term2': term2, 'k': k}
        }), 200
    except Exception as e:
        return jsonify({'error': f'Proximity search failed: {str(e)}', 'term1': term1, 'term2': term2, 'k': k}), 500

@app.route('/api/corpus', methods=['GET'])
def corpus_info():
    doc_ids = [document['doc_id'] for document in documents]
    return jsonify({
        'corpus_size': len(documents),
        'documents': doc_ids[:10],
        'total_documents': len(documents),
        'available_methods': ['vsm', 'bm25', 'phrase', 'proximity']
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': ['/api/health', '/api/search?q=query&method=vsm|bm25', '/api/compare?q=query', '/api/phrase?q="exact phrase"', '/api/proximity?term1=x&term2=y&k=5', '/api/corpus']
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'message': str(error)}), 500

if __name__ == '__main__':
    print(f"Corpus: {len(documents)} documents")
    print("Starting server on http://localhost:5000")
    app.run(debug=True, host='localhost', port=5000)
