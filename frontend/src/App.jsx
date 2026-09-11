import { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [mode, setMode] = useState("normal");

  const [term1, setTerm1] = useState("");
  const [term2, setTerm2] = useState("");
  const [k, setK] = useState(3);

  const [results, setResults] = useState([]);
  const [searched, setSearched] = useState(false);
  const [error, setError] = useState("");

  const searchNormal = async () => {
    if (!query.trim()) return;

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/search?q=${encodeURIComponent(query)}`
      );

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Search failed.");
        return;
      }

      setResults(data.results);
    } catch (err) {
      setError("Could not connect to the Flask backend.");
    }
  };

  const searchPhrase = async () => {
    if (!query.trim()) return;

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/phrase?q=${encodeURIComponent(query)}`
      );

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Phrase search failed.");
        return;
      }

      setResults(data.results);
    } catch (err) {
      setError("Could not connect to the Flask backend.");
    }
  };

  const searchProximity = async () => {
    if (!term1.trim() || !term2.trim()) return;

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/proximity?term1=${encodeURIComponent(
          term1
        )}&term2=${encodeURIComponent(term2)}&k=${k}`
      );

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Proximity search failed.");
        return;
      }

      setResults(data.results);
    } catch (err) {
      setError("Could not connect to the Flask backend.");
    }
  };

  const handleSearch = () => {
    setResults([]);
    setError("");
    setSearched(true);

    if (mode === "normal") {
      searchNormal();
    } else if (mode === "phrase") {
      searchPhrase();
    } else {
      searchProximity();
    }
  };

  const changeMode = (newMode) => {
    setMode(newMode);
    setResults([]);
    setError("");
    setSearched(false);
  };

  const getModeTitle = () => {
    if (mode === "normal") return "Vector Space Search";
    if (mode === "phrase") return "Exact Phrase Search";
    return "Ordered Proximity Search";
  };

  const getModeDescription = () => {
    if (mode === "normal") {
      return "Ranks documents using lnc.ltc cosine similarity.";
    }

    if (mode === "phrase") {
      return "Finds query terms occurring consecutively in the same order.";
    }

    return "Finds terms occurring within k positions in the specified order.";
  };

  return (
    <div className="app">
      <header className="hero">
        <div className="hero-content">
          <div className="badge">CSD358 · INFORMATION RETRIEVAL</div>

          <h1>Clothing Search Engine</h1>

          <p>
            Search a 100-document clothing corpus using Vector Space
            and Positional Retrieval.
          </p>
        </div>
      </header>

      <main>
        <section className="search-panel">
          <div className="mode-selector">
            <button
              className={mode === "normal" ? "active" : ""}
              onClick={() => changeMode("normal")}
            >
              <span>VSM</span>
              Normal Search
            </button>

            <button
              className={mode === "phrase" ? "active" : ""}
              onClick={() => changeMode("phrase")}
            >
              <span>PHRASE</span>
              Exact Phrase
            </button>

            <button
              className={mode === "proximity" ? "active" : ""}
              onClick={() => changeMode("proximity")}
            >
              <span>PROXIMITY</span>
              Proximity
            </button>
          </div>

          <div className="mode-info">
            <div>
              <h2>{getModeTitle()}</h2>
              <p>{getModeDescription()}</p>
            </div>
          </div>

          {mode === "proximity" ? (
            <div className="proximity-inputs">
              <input
                type="text"
                placeholder="First term"
                value={term1}
                onChange={(e) => setTerm1(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    handleSearch();
                  }
                }}
              />

              <span className="within-label">WITHIN</span>

              <input
                className="k-input"
                type="number"
                min="1"
                value={k}
                onChange={(e) => setK(e.target.value)}
              />

              <span className="position-label">positions</span>

              <input
                type="text"
                placeholder="Second term"
                value={term2}
                onChange={(e) => setTerm2(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    handleSearch();
                  }
                }}
              />
            </div>
          ) : (
            <input
              className="main-input"
              type="text"
              placeholder={
                mode === "normal"
                  ? "Search clothing... e.g. cotton shirt"
                  : 'Enter exact phrase... e.g. "regular fit"'
              }
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleSearch();
                }
              }}
            />
          )}

          <button className="search-button" onClick={handleSearch}>
            Search
          </button>

          <div className="examples">
            <strong>Try:</strong>

            {mode === "normal" && (
              <>
                <button onClick={() => setQuery("cotton shirt")}>
                  cotton shirt
                </button>
                <button onClick={() => setQuery("winter jacket")}>
                  winter jacket
                </button>
                <button onClick={() => setQuery("breathable fabric")}>
                  breathable fabric
                </button>
              </>
            )}

            {mode === "phrase" && (
              <>
                <button onClick={() => setQuery("cotton shirt")}>
                  "cotton shirt"
                </button>
                <button onClick={() => setQuery("regular fit")}>
                  "regular fit"
                </button>
                <button onClick={() => setQuery("winter wear")}>
                  "winter wear"
                </button>
              </>
            )}

            {mode === "proximity" && (
              <>
                <button
                  onClick={() => {
                    setTerm1("cotton");
                    setTerm2("shirt");
                    setK(3);
                  }}
                >
                  cotton / 3 / shirt
                </button>

                <button
                  onClick={() => {
                    setTerm1("stretch");
                    setTerm2("denim");
                    setK(4);
                  }}
                >
                  stretch / 4 / denim
                </button>
              </>
            )}
          </div>
        </section>

        {error && <div className="error">{error}</div>}

        {searched && !error && (
          <section className="results-section">
            <div className="results-header">
              <div>
                <h2>Search Results</h2>

                <p>
                  {mode === "proximity"
                    ? `${term1} WITHIN/${k} ${term2}`
                    : `"${query}"`}
                </p>
              </div>

              <span className="result-count">
                {results.length} result{results.length !== 1 ? "s" : ""}
              </span>
            </div>

            {results.length === 0 ? (
              <div className="no-results">
                <div className="no-results-icon">∅</div>

                <h3>No matching documents</h3>

                <p>
                  No documents matched this query after preprocessing,
                  stemming, and retrieval.
                </p>
              </div>
            ) : (
              <div className="result-list">
                {mode === "normal" &&
                  results.map((result, index) => (
                    <div className="result-card" key={result.doc_id}>
                      <div className="rank">
                        #{index + 1}
                      </div>

                      <div className="result-info">
                        <h3>{result.title}</h3>

                        <div className="metadata">
                          <span className="doc-id">
                            {result.doc_id}
                          </span>

                          <span>{result.category}</span>
                        </div>
                      </div>

                      <div className="score-box">
                        <span>Cosine Score</span>
                        <strong>{result.score.toFixed(6)}</strong>
                      </div>
                    </div>
                  ))}

                {mode === "phrase" &&
                  results.map((result) => (
                    <div className="result-card positional-card" key={result.doc_id}>
                      <div className="position-icon">P</div>

                      <div className="result-info">
                        <h3>{result.title}</h3>

                        <div className="metadata">
                          <span className="doc-id">
                            {result.doc_id}
                          </span>

                          <span>{result.category}</span>
                        </div>

                        <div className="positions">
                          <strong>Matching positions:</strong>

                          {Object.entries(result.positions).map(
                            ([term, positions]) => (
                              <span className="position-tag" key={term}>
                                {term}: [{positions.join(", ")}]
                              </span>
                            )
                          )}
                        </div>
                      </div>
                    </div>
                  ))}

                {mode === "proximity" &&
                  results.map((result) => (
                    <div className="result-card positional-card" key={result.doc_id}>
                      <div className="position-icon">P</div>

                      <div className="result-info">
                        <h3>{result.title}</h3>

                        <div className="metadata">
                          <span className="doc-id">
                            {result.doc_id}
                          </span>

                          <span>{result.category}</span>
                        </div>

                        <div className="positions">
                          <strong>Positional matches:</strong>

                          {result.matches.map((match, index) => (
                            <span className="position-tag" key={index}>
                              {term1} @ {match[term1]} → {term2} @{" "}
                              {match[term2]} · distance {match.distance}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
              </div>
            )}
          </section>
        )}

        {!searched && (
          <section className="welcome">
            <div className="welcome-icon">⌕</div>

            <h2>Search the clothing corpus</h2>

            <p>
              Choose a retrieval method above and enter your query.
            </p>

            <div className="method-cards">
              <div>
                <span>01</span>
                <h3>VSM</h3>
                <p>
                  Ranked retrieval using lnc.ltc cosine similarity.
                </p>
              </div>

              <div>
                <span>02</span>
                <h3>Exact Phrase</h3>
                <p>
                  Uses positional information to enforce consecutive
                  term matching.
                </p>
              </div>

              <div>
                <span>03</span>
                <h3>Proximity</h3>
                <p>
                  Finds ordered terms within a specified positional
                  distance.
                </p>
              </div>
            </div>
          </section>
        )}
      </main>

      <footer>
        <p>
          CSD358 · Information Retrieval · 100 Documents · 126 Indexed Terms
        </p>
      </footer>
    </div>
  );
}

export default App;