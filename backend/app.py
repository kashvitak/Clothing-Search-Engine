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

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load corpus (list of {"doc_id", "title", "category", "text"} dicts)
print("Loading corpus...")
documents = parse_corpus('../data/corpus_100.txt')
print(f"Loaded {len(documents)} documents")

# Initialize indices
print("Initializing indices...")
inverted_index = InvertedIndex(documents)
positional_idx = build_positional_index(documents)
bm25_index = BM25Index(documents)
print("Indices initialized!")


# ============================================
# HEALTH CHECK ENDPOINT
# ============================================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'corpus_size': len(documents),
        'indices': ['vsm', 'bm25', 'inverted', 'positional']
    }), 200


# ============================================
# SEARCH ENDPOINTS
# ============================================

@app.route('/api/search', methods=['GET'])
def search():
    """
    Search endpoint supporting both VSM and BM25 methods

    Query parameters:
    - q: search query (required)
    - method: 'vsm' or 'bm25' (default: 'vsm')
    - top_k: number of results (default: 10)

    Example: /api/search?q=cotton+shirt&method=vsm
    """
    query = request.args.get('q', '').strip()
    method = request.args.get('method', 'vsm').lower()
    top_k = request.args.get('top_k', 10, type=int)

    if not query:
        return jsonify({'error': 'Query parameter (q) is required'}), 400

    if method not in ['vsm', 'bm25']:
        return jsonify({'error': 'Method must be "vsm" or "bm25"'}), 400

    try:
        if method == 'bm25':
            # BM25 baseline search
            results = bm25_index.search(query, top_k=top_k)
            return jsonify({
                'query': query,
                'method': 'BM25',
                'results': results,
                'count': len(results),
                'timestamp': None
            }), 200
        else:
            # VSM (lnc.ltc) search
            results = vsm_search(query, documents, inverted_index)[:top_k]
            return jsonify({
                'query': query,
                'method': 'VSM (lnc.ltc)',
                'results': results,
                'count': len(results),
                'timestamp': None
            }), 200

    except Exception as e:
        return jsonify({
            'error': f'Search failed: {str(e)}',
            'query': query,
            'method': method
        }), 500


@app.route('/api/compare', methods=['GET'])
def compare_methods():
    """
    Compare results from both VSM and BM25 methods side-by-side

    Query parameters:
    - q: search query (required)
    - top_k: number of results per method (default: 10)

    Example: /api/compare?q=cotton+shirt
    """
    query = request.args.get('q', '').strip()
    top_k = request.args.get('top_k', 10, type=int)

    if not query:
        return jsonify({'error': 'Query parameter (q) is required'}), 400

    try:
        # Get results from both methods
        vsm_results = vsm_search(query, documents, inverted_index)[:top_k]
        bm25_results = bm25_index.search(query, top_k=top_k)

        return jsonify({
            'query': query,
            'vsm': {
                'method': 'VSM (lnc.ltc)',
                'results': vsm_results,
                'count': len(vsm_results)
            },
            'bm25': {
                'method': 'BM25',
                'results': bm25_results,
                'count': len(bm25_results)
            },
            'timestamp': None
        }), 200

    except Exception as e:
        return jsonify({
            'error': f'Comparison failed: {str(e)}',
            'query': query
        }), 500


# ============================================
# PHRASE SEARCH ENDPOINT
# ============================================

@app.route('/api/phrase', methods=['GET'])
def phrase_search():
    """
    Exact phrase search

    Query parameters:
    - q: search phrase (required, should be in quotes)

    Example: /api/phrase?q="cotton+shirt"
    """
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify({'error': 'Query parameter (q) is required'}), 400

    try:
        results = run_phrase_search(query, positional_idx)
        return jsonify({
            'query': query,
            'method': 'Phrase Search',
            'results': results,
            'count': len(results),
            'type': 'phrase'
        }), 200

    except Exception as e:
        return jsonify({
            'error': f'Phrase search failed: {str(e)}',
            'query': query
        }), 500


# ============================================
# PROXIMITY SEARCH ENDPOINT
# ============================================

@app.route('/api/proximity', methods=['GET'])
def proximity_search():
    """
    Proximity/WITHIN search - finds documents where two terms appear within k positions

    Query parameters:
    - term1: first term (required)
    - term2: second term (required)
    - k: maximum distance between terms (default: 5)

    Example: /api/proximity?term1=cotton&term2=shirt&k=3
    """
    term1 = request.args.get('term1', '').strip()
    term2 = request.args.get('term2', '').strip()
    k = request.args.get('k', 5, type=int)

    if not term1 or not term2:
        return jsonify({'error': 'Both term1 and term2 parameters are required'}), 400

    if k <= 0:
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
        return jsonify({
            'error': f'Proximity search failed: {str(e)}',
            'term1': term1,
            'term2': term2,
            'k': k
        }), 500


# ============================================
# CORPUS INFORMATION ENDPOINT
# ============================================

@app.route('/api/corpus', methods=['GET'])
def corpus_info():
    """
    Get information about the corpus
    """
    doc_ids = [document['doc_id'] for document in documents]
    return jsonify({
        'corpus_size': len(documents),
        'documents': doc_ids[:10],
        'total_documents': len(documents),
        'available_methods': ['vsm', 'bm25', 'phrase', 'proximity']
    }), 200


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': [
            '/api/health',
            '/api/search?q=query&method=vsm|bm25',
            '/api/compare?q=query',
            '/api/phrase?q="exact phrase"',
            '/api/proximity?term1=x&term2=y&k=5',
            '/api/corpus'
        ]
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': str(error)
    }), 500


# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("Clothing Search Engine - Flask API")
    print("=" * 60)
    print(f"Corpus: {len(documents)} documents")
    print("Available endpoints:")
    print("  GET /api/health - Health check")
    print("  GET /api/search?q=query&method=vsm|bm25 - Search (VSM or BM25)")
    print("  GET /api/compare?q=query - Compare methods")
    print("  GET /api/phrase?q=\"phrase\" - Phrase search")
    print("  GET /api/proximity?term1=x&term2=y&k=5 - Proximity search")
    print("  GET /api/corpus - Corpus info")
    print("=" * 60)
    print("Starting server on http://localhost:5000")
    print("=" * 60 + "\n")

    app.run(debug=True, host='localhost', port=5000)
