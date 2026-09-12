import re
from nltk.stem import PorterStemmer


# Standard English stop words
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for",
    "from", "has", "have", "in", "is", "it", "its", "of",
    "on", "or", "that", "the", "their", "this", "to", "was",
    "were", "will", "with", "you", "your", "but", "not",
    "they", "he", "she", "we", "i", "me", "my", "our",
    "ours", "his", "her", "them", "these", "those", "can",
    "could", "should", "would", "do", "does", "did","s"
}


stemmer = PorterStemmer()


def preprocess(text):
    """
    Preprocess text using:
    1. Lowercase conversion
    2. Tokenization
    3. Punctuation removal
    4. Stop-word removal
    5. Porter stemming

    Returns:
        list of processed/stemmed tokens
    """

    # 1. Lowercase
    text = text.lower()

    # 2. Tokenize and remove punctuation
    tokens = re.findall(r"\b[a-z]+\b", text)

    # 3. Remove stop words
    tokens = [
        token for token in tokens
        if token not in STOP_WORDS
    ]

    # 4. Porter stemming
    tokens = [
        stemmer.stem(token)
        for token in tokens
    ]

    return tokens


# Alias kept for backward compatibility with modules (e.g. bm25_index.py)
# that import `preprocess_text` instead of `preprocess`.
preprocess_text = preprocess


if __name__ == "__main__":

    test_text = "Men's Cotton Shirts are breathable and comfortable!"

    print("Original text:")
    print(test_text)

    print("\nProcessed tokens:")
    print(preprocess(test_text))
