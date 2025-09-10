import re
from collections import Counter
import nltk
import ssl
import os

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def download_nltk_data():
    """Download required NLTK data if not already present"""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        try:
            print("Downloading NLTK punkt tokenizer...")
            nltk.download('punkt', quiet=True)
        except Exception as e:
            print(f"Warning: Could not download punkt tokenizer: {e}")

    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        try:
            print("Downloading NLTK stopwords...")
            nltk.download('stopwords', quiet=True)
        except Exception as e:
            print(f"Warning: Could not download stopwords: {e}")

    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        try:
            print("Downloading NLTK POS tagger...")
            nltk.download('averaged_perceptron_tagger', quiet=True)
        except Exception as e:
            print(f"Warning: Could not download POS tagger: {e}")

download_nltk_data()

try:
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.tag import pos_tag
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    print("Warning: NLTK components not available, using fallback keyword extraction")

def extract_keywords_fallback(text: str, num_keywords: int = 3) -> list:
    """
    Fallback keyword extraction without NLTK.
    Uses simple word frequency analysis.
    """
    if not text or not text.strip():
        return []
    
    # Basic stopwords list
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
        'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
        'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
        'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'hers', 'ours', 'theirs'
    }
    
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    filtered_words = [word for word in words if word not in stop_words]
    word_counts = Counter(filtered_words)
    
    return [word for word, count in word_counts.most_common(num_keywords)]

def extract_keywords(text: str, num_keywords: int = 3) -> list:
    """
    Extract the most frequent nouns from text.
    Returns a list of the top N keywords.
    """
    if not text or not text.strip():
        return []
    
    if not NLTK_AVAILABLE:
        return extract_keywords_fallback(text, num_keywords)
    
    try:
        tokens = word_tokenize(text.lower())
        
        stop_words = set(stopwords.words('english'))
        
        stop_words.update(['.', ',', '!', '?', ';', ':', '-', '(', ')', '[', ']', '{', '}', '"', "'", '`', '``', "''"])
        stop_words.update(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
        
        filtered_tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
        
        tagged_tokens = pos_tag(filtered_tokens)
        
        nouns = [word for word, pos in tagged_tokens if pos in ['NN', 'NNS', 'NNP', 'NNPS']]
        
        noun_counts = Counter(nouns)
        top_nouns = [word for word, count in noun_counts.most_common(num_keywords)]
        
        return top_nouns
        
    except Exception as e:
        print(f"Warning: NLTK keyword extraction failed: {e}, using fallback")
        return extract_keywords_fallback(text, num_keywords)
