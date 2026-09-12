# Clothing Search Engine 

An **Information Retrieval system** for a 100-document clothing corpus supporting multiple retrieval methods including **VSM (lnc.ltc)** and **BM25 baseline comparison**.

## Features 

- **Vector Space Model (lnc.ltc)** - TF-IDF based retrieval with cosine similarity
- **BM25 Baseline** - Probabilistic ranking (novelty feature) 
- **Side-by-side Comparison** - Toggle between methods or compare results 
- **Phrase Search** - Find exact phrase matches
- **Proximity Search** - Find terms within k positions of each other
- **Text Preprocessing** - Tokenization, stop-word removal, Porter stemming
- **Inverted Index** - Efficient term-to-document lookup with TF/DF
- **Positional Index** - Support for phrase and proximity queries
- **REST API** - Flask backend with CORS support
- **React Web Interface** - Modern, responsive UI with search toggle
- **Automated Tests** - Comprehensive test suite

## Project Structure

```
Clothing-Search-Engine/
├── backend/
│   ├── app.py                          # Flask API server
│   ├── bm25_index.py                   # BM25 implementation
│   ├── corpus_parser.py                # Parse corpus from file
│   ├── preprocessing.py                # Text preprocessing
│   ├── inverted_index.py              # Inverted index implementation
│   ├── positional_index.py            # Positional index for phrases
│   ├── vsm.py                         # Vector Space Model (lnc.ltc)
│   ├── generate_index_outputs.py      # Generate index files
│   ├── test_all.py                    # Test suite
│   └── requirements.txt               # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx                    # Main React app (with toggle)
│   │   ├── App.css                    # Styling
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── .gitignore
├── data/
│   └── corpus_100.txt                 # 100-document clothing corpus
├── output/
│   ├── inverted_index.txt            # Generated index
│   └── positional_index.txt          # Generated index
├── BM25_SETUP.md                      # BM25 integration guide
└── README.md                          # This file
```

## Retrieval Methods

### 1. **Vector Space Model (lnc.ltc)** 

Document weighting:
```
w(term, doc) = (1 + log₁₀(tf)) if tf > 0, else 0
```

Query weighting:
```
w(term, query) = (1 + log₁₀(tf)) × log₁₀(N / df)
```

Where:
- `tf` = term frequency in document
- `df` = document frequency (# docs containing term)
- `N` = 100 (total documents)

**Ranking:** Cosine similarity between query and document vectors

### 2. **BM25** (Baseline) 

A **probabilistic ranking function** that considers:
- **Term frequency saturation** - Diminishing returns for repeated terms
- **Document length normalization** - Favors relevant shorter documents
- **IDF weighting** - Emphasizes rare, discriminative terms

**Key parameters:**
- `k1 = 2.0` - Controls TF saturation point
- `b = 0.75` - Controls length normalization

**Why compare both?**
- VSM is a classic, well-understood baseline
- BM25 often performs better in practice
- Side-by-side comparison reveals ranking differences

### 3. **Phrase Search**

Finds documents with **exact consecutive term matches** in order.

Example: `"cotton shirt"` matches only documents with both terms adjacent.

### 4. **Proximity Search**

Finds documents where two terms appear **within k positions** of each other.

Example: `cotton WITHIN 3 shirt` matches if "shirt" appears ≤3 positions after "cotton".

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+ (for frontend)
- npm or yarn

### Backend Setup

#### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### 2. Download NLTK Data (one-time setup)

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

#### 3. Run the Flask Server

```bash
python app.py
```

Server starts on `http://localhost:5000`

### Frontend Setup

#### 1. Install Dependencies

```bash
cd frontend
npm install
```

#### 2. Start Development Server

```bash
npm run dev
```

Frontend starts on `http://localhost:5173` (Vite)

### Run Tests

```bash
cd backend
python test_all.py
```

## API Endpoints

### Health Check
```
GET /api/health
```
Returns: Server status and available indices

### Search (VSM or BM25)
```
GET /api/search?q=query&method=vsm|bm25&top_k=10
```

**Parameters:**
- `q` (required): Search query
- `method` (optional): "vsm" or "bm25" (default: "vsm")
- `top_k` (optional): Number of results (default: 10)

**Example:**
```
GET /api/search?q=cotton+shirt&method=vsm
GET /api/search?q=denim+jeans&method=bm25
```

**Response:**
```json
{
  "query": "cotton shirt",
  "method": "VSM (lnc.ltc)",
  "results": [
    {
      "doc_id": "doc_5",
      "score": 0.8234,
      "text": "Document preview text..."
    }
  ],
  "count": 10
}
```

### Compare Both Methods
```
GET /api/compare?q=query&top_k=10
```

**Example:**
```
GET /api/compare?q=cotton+shirt
```

**Response:**
```json
{
  "query": "cotton shirt",
  "vsm": {
    "method": "VSM (lnc.ltc)",
    "results": [...],
    "count": 10
  },
  "bm25": {
    "method": "BM25",
    "results": [...],
    "count": 10
  }
}
```

### Phrase Search
```
GET /api/phrase?q="exact+phrase"
```

**Example:**
```
GET /api/phrase?q="cotton+shirt"
```

### Proximity Search
```
GET /api/proximity?term1=term1&term2=term2&k=distance
```

**Example:**
```
GET /api/proximity?term1=cotton&term2=shirt&k=3
```

### Corpus Information
```
GET /api/corpus
```

Returns: Corpus statistics and available documents

## Web Interface Features 🎨

### Search Toggle

The React frontend includes an interactive search toggle:

1. **Single Method Search** - Query with VSM or BM25 individually
2. **Compare Mode** - See results from both methods side-by-side
3. **Real-time Toggle** - Switch methods without reloading
4. **Score Display** - Relevance scores for transparency

### UI Components

- **Method Selector** - Radio buttons for VSM/BM25
- **Compare Checkbox** - Toggle comparison mode
- **Search Box** - Text input with Enter key support
- **Results Display** - Ranked results with scores
- **Comparison Grid** - Split-view with color-coded sections

## Example Queries

### Free Text Search
- `cotton shirt`
- `denim jeans`
- `winter jacket`
- `sports shoes`
- `regular fit`

### Phrase Search
- `"cotton shirt"`
- `"stretch denim"`
- `"regular fit"`
- `"summer collection"`

### Proximity Search
- `cotton WITHIN 2 shirt`
- `cotton WITHIN 3 shirt`
- `stretch WITHIN 4 denim`

## Results & Performance

### VSM (lnc.ltc) Performance
- Average query time: ~20-50ms
- Top 10 results retrieved per query
- Works well with short phrases

### BM25 Performance
- Average query time: ~10-30ms (typically faster)
- Better handling of term frequency variations
- Excellent for longer documents

### Comparison
- Phrase search: ~5-15 results (exact matches only)
- Proximity search: ~10-20 results depending on k
- Both methods complement each other

## Technologies Used 🛠️

### Backend
- **Python 3.8+**
- **Flask 2.3** - Web framework
- **Flask-CORS 4.0** - Cross-origin support
- **NLTK 3.8** - Natural language processing
- **rank-bm25 0.2.2** - BM25 implementation

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **CSS 3** - Styling
- **JavaScript ES6+** - Client logic

### Testing
- **Python unittest** - Backend tests

## Code Quality

-  Full type hints and docstrings
-  Modular design with separation of concerns
-  Comprehensive error handling
-  CORS support for API access
-  Responsive UI design

## Assignment Coverage

| Requirement | Implementation | Location |
|---|---|---|
| Text Preprocessing | Tokenization, stop-word removal, stemming | `preprocessing.py` |
| Inverted Index | TF/DF computation | `inverted_index.py` |
| VSM (lnc.ltc) | Full TF-IDF implementation | `vsm.py` |
| Positional Index | Document positions stored | `positional_index.py` |
| Phrase/Proximity Search | Both implemented | `positional_index.py` |
| REST API | Full Flask API | `app.py` |
| Web Interface | React with search toggle | `App.jsx`, `App.css` |
| Testing | Comprehensive test suite | `test_all.py` |
| Index Outputs | Generated files | `output/` |
| **BM25 Baseline** | **Novelty feature** | **`bm25_index.py`** |

## Installation & Execution

### Quick Start

```bash
# Backend
cd backend
pip install -r requirements.txt
python app.py

# Frontend (in new terminal)
cd frontend
npm install
npm run dev
```

### Full Setup

```bash
# Clone and setup backend
git clone https://github.com/sharanyagupta239/Clothing-Search-Engine.git
cd Clothing-Search-Engine/backend

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Start Flask server
python app.py

# In another terminal, setup frontend
cd ../frontend
npm install
npm run dev

# Open browser to http://localhost:5173
```

## Troubleshooting

### Backend Issues

**Port already in use (5000):**
```bash
# Find and kill process using port 5000
# On macOS/Linux:
lsof -ti:5000 | xargs kill -9

# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**NLTK data not found:**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Frontend Issues

**npm install fails:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Port 5173 in use:**
```bash
npm run dev -- --port 3000  # Use different port
```

### API Connection Issues

**"Cannot connect to backend" error:**
- Ensure Flask server is running: `python app.py`
- Check backend is on `http://localhost:5000`
- Verify CORS is enabled in Flask
- Check browser console for specific errors

## Contributing

This is an assignment project. For improvements or bug reports, please open an issue or submit a pull request.

## License

Educational project for Information Retrieval course.

## Acknowledgments

- NLTK library for natural language processing
- rank-bm25 library for BM25 implementation
- React and Vite for frontend framework
- Flask for REST API framework

---

**Last Updated:** September 2026  
**Corpus Size:** 100 documents  
**Supported Retrieval Methods:** 4 (VSM, BM25, Phrase, Proximity)
