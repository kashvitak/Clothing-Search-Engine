import React, { useState } from 'react';
import './App.css';

const SearchToggle = ({ onSearch }) => {
  const [query, setQuery] = useState('');
  const [method, setMethod] = useState('vsm');
  const [k, setK] = useState(2);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [compareMode, setCompareMode] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) {
      setError('Please enter a search query');
      return;
    }

    if (method === 'proximity' && k <= 0) {
      setError('Proximity distance k must be greater than 0');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      let endpoint;
      let data;

      if (compareMode) {
        endpoint = `http://localhost:5000/api/compare?q=${encodeURIComponent(query)}`;
      } else if (method === 'phrase') {
        endpoint = `http://localhost:5000/api/phrase?q=${encodeURIComponent(query)}`;
      } else if (method === 'proximity') {
        const parts = query.trim().split(/\s+/);

        if (parts.length < 2) {
          throw new Error('Enter two terms, e.g. cotton shirt');
        }

        const term1 = parts[0];
        const term2 = parts.slice(1).join(' ');

        endpoint =
          `http://localhost:5000/api/proximity` +
          `?term1=${encodeURIComponent(term1)}` +
          `&term2=${encodeURIComponent(term2)}` +
          `&k=${k}`;
      } else {
        endpoint =
          `http://localhost:5000/api/search` +
          `?q=${encodeURIComponent(query)}` +
          `&method=${method}`;
      }

      const response = await fetch(endpoint);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      data = await response.json();

      if (compareMode) {
        setResults(data);
      } else {
        setResults({
          query: data.query,
          method: data.method,
          results: data.results || [],
          count: data.count || 0,
          type: data.type || method,
          singleMode: true,
          parameters: data.parameters
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
              onChange={(e) => {
                setMethod(e.target.value);
                setCompareMode(false);
              }}
            />
            <span className="radio-label">VSM (lnc.ltc)</span>
          </label>

          <label>
            <input
              type="radio"
              name="method"
              value="bm25"
              checked={method === 'bm25'}
              onChange={(e) => {
                setMethod(e.target.value);
                setCompareMode(false);
              }}
            />
            <span className="radio-label">BM25 Baseline</span>
          </label>

          <label>
            <input
              type="radio"
              name="method"
              value="phrase"
              checked={method === 'phrase'}
              onChange={(e) => {
                setMethod(e.target.value);
                setCompareMode(false);
              }}
            />
            <span className="radio-label">Exact Phrase</span>
          </label>

          <label>
            <input
              type="radio"
              name="method"
              value="proximity"
              checked={method === 'proximity'}
              onChange={(e) => {
                setMethod(e.target.value);
                setCompareMode(false);
              }}
            />
            <span className="radio-label">Proximity</span>
          </label>

          <label className="compare-toggle">
            <input
              type="checkbox"
              checked={compareMode}
              onChange={(e) => setCompareMode(e.target.checked)}
            />
            <span className="checkbox-label">Compare VSM & BM25</span>
          </label>

        </div>

        <div className="search-box">

          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            placeholder={
              method === 'phrase'
                ? 'e.g. cotton shirt'
                : method === 'proximity'
                ? 'e.g. cotton shirt'
                : 'Search for clothing...'
            }
            className="search-input"
          />

          {method === 'proximity' && (
            <input
              type="number"
              min="1"
              value={k}
              onChange={(e) => setK(Number(e.target.value))}
              className="search-input"
              style={{ maxWidth: '90px' }}
              title="Maximum proximity distance"
            />
          )}

          <button
            onClick={handleSearch}
            disabled={loading}
            className="search-button"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>

        </div>

      </div>

      {method === 'phrase' && (
        <p className="result-count">
          Exact phrase matching using the positional index
        </p>
      )}

      {method === 'proximity' && (
        <p className="result-count">
          Ordered proximity search: term 1 before term 2, within {k} positions
        </p>
      )}

      {error && <div className="error-message">{error}</div>}

      {results && results.singleMode && (
        <div className="results-container">

          <div className="results-section">

            <h3 className="method-title">
              {results.method}
            </h3>

            <p className="result-count">
              Found {results.count} results
            </p>

            <div className="results-list">

              {results.results.length === 0 && (
                <div className="result-item">
                  No matching documents found.
                </div>
              )}

              {results.results.map((result, idx) => (
                <div key={idx} className="result-item">

                  <div className="result-rank">
                    #{idx + 1}
                  </div>

                  <div className="result-doc-id">
                    {result.doc_id}
                  </div>

                  {result.score !== undefined && (
                    <div className="result-score">
                      Score:{' '}
                      <strong>
                        {Number(result.score).toFixed(4)}
                      </strong>
                    </div>
                  )}

                  {result.title && (
                    <div>
                      <strong>{result.title}</strong>
                    </div>
                  )}

                  {result.category && (
                    <div>
                      Category: {result.category}
                    </div>
                  )}

                  {result.text && (
                    <div className="result-text">
                      {result.text}
                    </div>
                  )}

                  {result.positions && (
                    <div className="result-text">
                      Matching positions:{' '}
                      {JSON.stringify(result.positions)}
                    </div>
                  )}

                  {result.matches && (
                    <div className="result-text">
                      Matches:{' '}
                      {JSON.stringify(result.matches)}
                    </div>
                  )}

                </div>
              ))}

            </div>

          </div>

        </div>
      )}

      {results && compareMode && !results.singleMode && (
        <div className="comparison-container">

          <div className="comparison-grid">

            <div className="results-section vsm-section">

              <div className="method-header vsm-header">
                <h3>{results.vsm.method}</h3>
                <span className="result-badge">
                  {results.vsm.count} results
                </span>
              </div>

              <div className="results-list">

                {results.vsm.results.map((result, idx) => (
                  <div key={idx} className="result-item">
                    <div className="result-rank">
                      #{idx + 1}
                    </div>

                    <div className="result-doc-id">
                      {result.doc_id}
                    </div>

                    <div className="result-score">
                      {Number(result.score).toFixed(4)}
                    </div>
                  </div>
                ))}

              </div>

            </div>

            <div className="results-section bm25-section">

              <div className="method-header bm25-header">
                <h3>{results.bm25.method}</h3>
                <span className="result-badge">
                  {results.bm25.count} results
                </span>
              </div>

              <div className="results-list">

                {results.bm25.results.map((result, idx) => (
                  <div key={idx} className="result-item">
                    <div className="result-rank">
                      #{idx + 1}
                    </div>

                    <div className="result-doc-id">
                      {result.doc_id}
                    </div>

                    <div className="result-score">
                      {Number(result.score).toFixed(4)}
                    </div>
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
          <h1>Clothing Search Engine</h1>
          <p className="subtitle">
            Information Retrieval System
          </p>
        </div>
      </header>

      <main className="app-main">
        <div className="container">

          <SearchToggle onSearch={handleSearch} />

          {searchResults && (
            <div className="info-section">
              <h2>Search Results</h2>
              <p className="info-text">
                Query:{' '}
                <strong>
                  "{searchResults.query}"
                </strong>
              </p>
            </div>
          )}

        </div>
      </main>

      <footer className="app-footer">
        <p>
          Information Retrieval System | Clothing Corpus
          (100 documents)
        </p>
        <p>
          VSM • BM25 • Phrase • Proximity Search
        </p>
      </footer>

    </div>
  );
}

export default App;