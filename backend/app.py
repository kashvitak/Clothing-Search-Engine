from flask import Flask, request, jsonify
from flask_cors import CORS

from corpus_parser import parse_corpus
from inverted_index import build_inverted_index
from vsm import search
from positional_index import (
    build_positional_index,
    phrase_search,
    proximity_search
)


app = Flask(__name__)
CORS(app)


# Load corpus and build indexes once when the server starts
documents = parse_corpus("../data/corpus_100.txt")

inverted_index = build_inverted_index(documents)
positional_index = build_positional_index(documents)

def add_document_details(results):
    document_map = {
        document["doc_id"]: document
        for document in documents
    }

    enriched_results = []

    for result in results:
        document = document_map[result["doc_id"]]

        enriched_result = {
            **result,
            "title": document["title"],
            "category": document["category"]
        }

        enriched_results.append(enriched_result)

    return enriched_results

@app.route("/api/search", methods=["GET"])
def normal_search():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({
            "error": "Query is required"
        }), 400

    results = search(
        query,
        documents,
        inverted_index
    )

    return jsonify({
        "query": query,
        "results": results
    })


@app.route("/api/phrase", methods=["GET"])
def phrase_search_api():
    phrase = request.args.get("q", "").strip()

    if not phrase:
        return jsonify({
            "error": "Phrase is required"
        }), 400

    results = phrase_search(
        phrase,
        positional_index
    )


    results = add_document_details(results)

    return jsonify({
        "query": phrase,
        "results": results
    })


@app.route("/api/proximity", methods=["GET"])
def proximity_search_api():
    term1 = request.args.get("term1", "").strip()
    term2 = request.args.get("term2", "").strip()
    k = request.args.get("k", type=int)

    if not term1 or not term2 or k is None:
        return jsonify({
            "error": "term1, term2 and k are required"
        }), 400

    results = proximity_search(
        term1,
        term2,
        k,
        positional_index
    )

    results = add_document_details(results)

    return jsonify({
        "term1": term1,
        "term2": term2,
        "k": k,
        "results": results
    })


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "documents": len(documents),
        "unique_terms": len(inverted_index)
    })




if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )