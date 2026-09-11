Clothing Search Engine

An Information Retrieval system for a 100-document clothing corpus supporting:

Text preprocessing, stop-word removal and Porter stemming

Inverted index with term frequency and document frequency

lnc.ltc Vector Space Model with cosine similarity

Positional index

Exact phrase search

Ordered proximity search

Flask REST API

React web interface

Automated tests

Project Structure

Clothing-Search-Engine/
├── backend/
│   ├── app.py
│   ├── corpus_parser.py
│   ├── preprocessing.py
│   ├── inverted_index.py
│   ├── positional_index.py
│   ├── vsm.py
│   ├── generate_index_outputs.py
│   └── test_all.py
├── data/
│   └── corpus_100.txt
├── frontend/
├── output/
│   ├── inverted_index.txt
│   └── positional_index.txt
└── README.md

Retrieval Methods

VSM — lnc.ltc

Document weight:

1 + log10(tf)

Query weight:

(1 + log10(tf)) × log10(N / df)

where N = 100.

Cosine similarity is used to rank the top 10 documents.

Positional Search

Postings store:

(docID, tf, positions)

Exact phrase search requires terms to occur consecutively and in order.

Proximity search uses:

0 < position(term2) - position(term1) <= k

API

GET /api/health
GET /api/search?q=cotton shirt
GET /api/phrase?q=cotton shirt
GET /api/proximity?term1=cotton&term2=shirt&k=2

Running

Backend

cd backend
pip install Flask flask-cors nltk
python app.py

Frontend

cd frontend
npm install
npm run dev

Tests

cd backend
python test_all.py

Generate Index Files

cd backend
python generate_index_outputs.py

Example Queries

Free text

cotton shirt
denim jeans
winter jacket
sports shoes
regular fit

Phrase

"cotton shirt"
"stretch denim"
"regular fit"

Proximity

cotton WITHIN 2 shirt
cotton WITHIN 3 shirt
stretch WITHIN 4 denim

Results

The system dynamically computes results without hardcoded document IDs.

Example observations:

"cotton shirt" returns 5 exact phrase matches.

"regular fit" returns 15 phrase matches, while VSM returns the top 10 ranked documents.

cotton WITHIN 2 shirt returns 10 matches, increasing to 15 with k = 3.

Technologies

Python, Flask, NLTK, React, Vite, JavaScript, CSS.

Assignment Coverage

Requirement

Implementation

Preprocessing

preprocessing.py

Inverted index

inverted_index.py

lnc.ltc VSM

vsm.py

Positional index

positional_index.py

Phrase/proximity search

positional_index.py

REST API

app.py

Web interface

React

Testing

test_all.py

Index outputs

output/