import React, { useState } from 'react';
import './App.css';

// Search Toggle Component
const SearchToggle = ({ onSearch }) => {
  const [query, setQuery] = useState('');
  const [method, setMethod] = useState('vsm');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [compareMode, setCompareMode] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) {
      setError('Please enter a search query');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      let endpoint, data;

      if (compareMode) {
        endpoint = `http://localhost:5000/api/compare?q=${encodeURIComponent(query)}`;
        const response = await fetch(endpoint);

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        data = await response.json();
        setResults(data);
      } else {
        endpoint = `http://localhost:5000/api/search?q=${encodeURIComponent(query)}&method=${method}`;
        const response = await fetch(endpoint);

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        data = await response.json();
        setResults({
          query: data.query,
          vsm: method === 'vsm' ? data : null,
          bm25: method === 'bm25' ? data : null,
          singleMode: true
        });
      }

      onSearch(data);
    } catch (err) {
      setError(`Search failed: ${err.message}`);
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="search-toggle-container">
      <div className="search-controls">
        <div className="method-selector">
          <label>
            <input
              type="radio"
              name="method"
              value="vsm"
              checked={method === 'vsm'}
              onChange={(e) => setMethod(e.target.value)}
              disabled={compareMode}
            />
            <span className="radio-label">VSM (lnc.ltc)</span>
          </label>

          <label>
            <input
              type="radio"
              name="method"
              value="bm25"
              checked={method === 'bm25'}
              onChange={(e) => setMethod(e.target.value)}
              disabled={compareMode}
            />
            <span className="radio-label">BM25 Baseline</span>
          </label>

          <label className="compare-toggle">
            <input
              type="checkbox"
              checked={compareMode}
              onChange={(e) => setCompareMode(e.target.checked)}
            />
            <span className="checkbox-label">Compare Both Methods</span>
          </label>
        </div>

        <div className="search-box">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            placeholder="Search for clothing... (e.g., cotton shirt, denim jeans)"
            className="search-input"
          />
          <button
            onClick={handleSearch}
            disabled={loading}
            className="search-button"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      {results && !compareMode && results.singleMode && (
        <div className="results-container">
          <div className="results-section">
            <h3 className="method-title">
              {results.vsm ? results.vsm.method : results.bm25.method}
            </h3>
            <p className="result-count">
              Found {results.vsm ? results.vsm.count : results.bm25.count} results
            </p>
            <div className="results-list">
              {(results.vsm?.results || results.bm25?.results || []).map((result, idx) => (
                <div key={idx} className="result-item">
                  <div className="result-rank">#{idx + 1}</div>
                  <div className="result-doc-id">{result.doc_id}</div>
                  <div className="result-score">
                    Score: <strong>{result.score.toFixed(4)}</strong>
                  </div>
                  <div className="result-text">{result.text}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {results && compareMode && !results.singleMode && (
        <div className="comparison-container">
          <div className="comparison-grid">
            {/* VSM Results */}
            <div className="results-section vsm-section">
              <div className="method-header vsm-header">
                <h3>{results.vsm.method}</h3>
                <span className="result-badge">{results.vsm.count} results</span>
              </div>
              <div className="results-list">
                {results.vsm.results.map((result, idx) => (
                  <div key={idx} className="result-item">
                    <div className="result-rank">#{idx + 1}</div>
                    <div className="result-doc-id">{result.doc_id}</div>
                    <div className="result-score">{result.score.toFixed(4)}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* BM25 Results */}
            <div className="results-section bm25-section">
              <div className="method-header bm25-header">
                <h3>{results.bm25.method}</h3>
                <span className="result-badge">{results.bm25.count} results</span>
              </div>
              <div className="results-list">
                {results.bm25.results.map((result, idx) => (
                  <div key={idx} className="result-item">
                    <div className="result-rank">#{idx + 1}</div>
                    <div className="result-doc-id">{result.doc_id}</div>
                    <div className="result-score">{result.score.toFixed(4)}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Main App Component
function App() {
  const [searchResults, setSearchResults] = useState(null);

  const handleSearch = (results) => {
    setSearchResults(results);
    console.log('Search results:', results);
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>🧵 Clothing Search Engine</h1>
          <p className="subtitle">IR System with VSM & BM25 Comparison</p>
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          <SearchToggle onSearch={handleSearch} />

          {searchResults && (
            <div className="info-section">
              <h2>Search Results</h2>
              <p className="info-text">
                Query: <strong>"{searchResults.query}"</strong>
              </p>
            </div>
          )}
        </div>
      </main>

      <footer className="app-footer">
        <p>Information Retrieval System | Clothing Corpus (100 documents)</p>
        <p>VSM (lnc.ltc) vs BM25 Baseline Comparison</p>
      </footer>
    </div>
  );
}

export default App;
