import re
from nltk.stem import PorterStemmer

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for",
    "from", "has", "have", "in", "is", "it", "its", "of",
    "on", "or", "that", "the", "their", "this", "to", "was",
    "were", "will", "with", "you", "your", "but", "not",
    "they", "he", "she", "we", "i", "me", "my", "our",
    "ours", "his", "her", "them", "these", "those", "can",
    "could", "should", "would", "do", "does", "did", "s"
}

stemmer = PorterStemmer()

def preprocess(text):
    text = text.lower()
    tokens = re.findall(r"\b[a-z]+\b", text)
    tokens = [token for token in tokens if token not in STOP_WORDS]
    tokens = [stemmer.stem(token) for token in tokens]
    return tokens

# Alias kept for backward compatibility with modules (e.g. bm25_index.py)
# that import `preprocess_text` instead of `preprocess`.
preprocess_text = preprocess
