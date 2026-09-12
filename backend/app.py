"""
Flask REST API for Clothing Search Engine
Supports: VSM (lnc.ltc), BM25 baseline, Phrase search, Proximity search
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from corpus_parser import parse_corpus
from preprocessing import preprocess
from inverted_index import InvertedIndex
from vsm import VSM
from positional_index import PositionalIndex
from bm25_index import BM25Index

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load corpus
print("Loading corpus...")
corpus_dict = parse_corpus('../data/corpus_100.txt')
print(f"Loaded {len(corpus_dict)} documents")

# Initialize indices
print("Initializing indices...")
inverted_index = InvertedIndex(corpus_dict)
vsm_index = VSM(corpus_dict, inverted_index)
positional_index = PositionalIndex(corpus_dict)
bm25_index = BM25Index(corpus_dict)
print("Indices initialized!")


# ============================================
# HEALTH CHECK ENDPOINT
# ============================================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'corpus_size': len(corpus_dict),
        'indices': ['vsm', 'bm25', 'inverted', 'positional']
    }), 200


# ============================================
# SEARCH ENDPOINTS
# ============================================

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
            return jsonify({
                'query': query,
                'method': 'BM25',
                'results': results,
                'count': len(results),
                'timestamp': None
            }), 200
        else:
            results = vsm_index.search(query, top_k=top_k)
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
    query = request.args.get('q', '').strip()
    top_k = request.args.get('top_k', 10, type=int)
    
    if not query:
        return jsonify({'error': 'Query parameter (q) is required'}), 400
    
    try:
        vsm_results = vsm_index.search(query, top_k=top_k)
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
# PHRASE & PROXIMITY ENDPOINTS
# ============================================

@app.route('/api/phrase', methods=['GET'])
def phrase_search():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': 'Query parameter (q) is required'}), 400
    try:
        results = positional_index.phrase_search(query)
        return jsonify({'query': query, 'method': 'Phrase Search', 'results': results, 'count': len(results)}), 200
    except Exception as e:
        return jsonify({'error': f'Phrase search failed: {str(e)}'}), 500


@app.route('/api/proximity', methods=['GET'])
def proximity_search():
    term1 = request.args.get('term1', '').strip()
    term2 = request.args.get('term2', '').strip()
    k = request.args.get('k', 5, type=int)
    if not term1 or not term2:
        return jsonify({'error': 'Both term1 and term2 are required'}), 400
    try:
        results = positional_index.proximity_search(term1, term2, k)
        return jsonify({'query': f'{term1} WITHIN {k} {term2}', 'results': results, 'count': len(results)}), 200
    except Exception as e:
        return jsonify({'error': f'Proximity search failed: {str(e)}'}), 500


@app.route('/api/corpus', methods=['GET'])
def corpus_info():
    return jsonify({'corpus_size': len(corpus_dict), 'available_methods': ['vsm', 'bm25', 'phrase', 'proximity']}), 200


if __name__ == '__main__':
    print("\nStarting server on http://localhost:5000\n")
    app.run(debug=True, host='localhost', port=5000)
