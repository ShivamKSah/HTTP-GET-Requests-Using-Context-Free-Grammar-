"""
Advanced Text Summarization Module

This module provides both extractive and abstractive text summarization
capabilities with multiple algorithms and approaches.
"""

import re
import nltk
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter, defaultdict
from datetime import datetime
import math
from dataclasses import dataclass
from enum import Enum

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('wordnet', quiet=True)
except:
    pass

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag

class SummarizationType(Enum):
    EXTRACTIVE = "extractive"
    ABSTRACTIVE = "abstractive"
    HYBRID = "hybrid"

class SummarizationMethod(Enum):
    FREQUENCY_BASED = "frequency_based"
    TF_IDF = "tf_idf"
    TEXTRANK = "textrank"
    LSA = "lsa"  # Latent Semantic Analysis
    LUHN = "luhn"
    EDMUNDSON = "edmundson"

@dataclass
class SentenceScore:
    """Score information for a sentence."""
    sentence: str
    score: float
    position: int
    length: int
    keywords_count: int
    metadata: Dict[str, Any]

@dataclass
class SummaryResult:
    """Result of text summarization."""
    original_text: str
    summary: str
    method: SummarizationMethod
    summary_type: SummarizationType
    compression_ratio: float
    sentence_scores: List[SentenceScore]
    key_phrases: List[str]
    statistics: Dict[str, Any]
    processing_time: float
    timestamp: str

class AdvancedTextSummarizer:
    """Advanced text summarization with multiple algorithms."""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        
    def summarize(self, text: str, 
                 method: SummarizationMethod = SummarizationMethod.TF_IDF,
                 summary_type: SummarizationType = SummarizationType.EXTRACTIVE,
                 summary_length: int = 3,
                 compression_ratio: Optional[float] = None) -> SummaryResult:
        """
        Generate summary using specified method and type.
        
        Args:
            text: Input text to summarize
            method: Summarization algorithm to use
            summary_type: Type of summarization (extractive/abstractive/hybrid)
            summary_length: Number of sentences in summary (if compression_ratio not provided)
            compression_ratio: Ratio of summary length to original (0.0-1.0)
        """
        start_time = datetime.now()
        
        # Preprocess text
        sentences = self._preprocess_text(text)
        
        if not sentences:
            raise ValueError("No valid sentences found in input text")
        
        # Calculate target summary length
        if compression_ratio:
            summary_length = max(1, int(len(sentences) * compression_ratio))
        else:
            summary_length = min(summary_length, len(sentences))
        
        # Generate summary based on method
        if method == SummarizationMethod.FREQUENCY_BASED:
            sentence_scores = self._frequency_based_scoring(sentences, text)
        elif method == SummarizationMethod.TF_IDF:
            sentence_scores = self._tfidf_scoring(sentences, text)
        elif method == SummarizationMethod.TEXTRANK:
            sentence_scores = self._textrank_scoring(sentences, text)
        elif method == SummarizationMethod.LSA:
            sentence_scores = self._lsa_scoring(sentences, text)
        elif method == SummarizationMethod.LUHN:
            sentence_scores = self._luhn_scoring(sentences, text)
        elif method == SummarizationMethod.EDMUNDSON:
            sentence_scores = self._edmundson_scoring(sentences, text)
        else:
            raise ValueError(f"Unsupported summarization method: {method}")
        
        # Select top sentences
        top_sentences = self._select_top_sentences(sentence_scores, summary_length)
        
        # Generate final summary
        if summary_type == SummarizationType.EXTRACTIVE:
            summary = self._generate_extractive_summary(top_sentences)
        elif summary_type == SummarizationType.ABSTRACTIVE:
            summary = self._generate_abstractive_summary(top_sentences, text)
        else:  # HYBRID
            summary = self._generate_hybrid_summary(top_sentences, text)
        
        # Extract key phrases
        key_phrases = self._extract_key_phrases(text)
        
        # Calculate statistics
        processing_time = (datetime.now() - start_time).total_seconds()
        actual_compression_ratio = len(summary.split()) / len(text.split())
        
        statistics = {
            'original_sentences': len(sentences),
            'summary_sentences': summary_length,
            'original_words': len(text.split()),
            'summary_words': len(summary.split()),
            'compression_ratio': actual_compression_ratio,
            'readability_score': self._calculate_readability(summary),
            'coherence_score': self._calculate_coherence(top_sentences)
        }
        
        return SummaryResult(
            original_text=text,
            summary=summary,
            method=method,
            summary_type=summary_type,
            compression_ratio=actual_compression_ratio,
            sentence_scores=sentence_scores,
            key_phrases=key_phrases,
            statistics=statistics,
            processing_time=processing_time,
            timestamp=datetime.now().isoformat()
        )
    
    def _preprocess_text(self, text: str) -> List[str]:
        """Preprocess text and extract sentences."""
        # Clean text
        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'[^\w\s\.\!\?\;]', '', text)
        
        # Tokenize sentences
        sentences = sent_tokenize(text)
        
        # Filter out very short sentences
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        return sentences
    
    def _frequency_based_scoring(self, sentences: List[str], text: str) -> List[SentenceScore]:
        """Score sentences based on word frequency."""
        # Calculate word frequencies
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalnum() and word not in self.stop_words]
        word_freq = Counter(words)
        
        sentence_scores = []
        for i, sentence in enumerate(sentences):
            sentence_words = word_tokenize(sentence.lower())
            sentence_words = [word for word in sentence_words if word.isalnum() and word not in self.stop_words]
            
            if not sentence_words:
                score = 0.0
            else:
                score = sum(word_freq[word] for word in sentence_words) / len(sentence_words)
            
            sentence_scores.append(SentenceScore(
                sentence=sentence,
                score=score,
                position=i,
                length=len(sentence_words),
                keywords_count=len(sentence_words),
                metadata={'word_frequencies': {word: word_freq[word] for word in sentence_words}}
            ))
        
        return sentence_scores
    
    def _tfidf_scoring(self, sentences: List[str], text: str) -> List[SentenceScore]:
        """Score sentences using TF-IDF algorithm."""
        # Create vocabulary
        all_words = []
        sentence_words = []
        
        for sentence in sentences:
            words = word_tokenize(sentence.lower())
            words = [self.lemmatizer.lemmatize(word) for word in words 
                    if word.isalnum() and word not in self.stop_words]
            sentence_words.append(words)
            all_words.extend(words)
        
        vocabulary = list(set(all_words))
        word_to_idx = {word: i for i, word in enumerate(vocabulary)}
        
        # Calculate TF-IDF matrix
        tf_idf_matrix = []
        for words in sentence_words:
            tf_idf_vector = [0.0] * len(vocabulary)
            word_count = len(words)
            
            for word in words:
                if word in word_to_idx:
                    # Term Frequency
                    tf = words.count(word) / word_count
                    
                    # Document Frequency
                    df = sum(1 for sent_words in sentence_words if word in sent_words)
                    
                    # Inverse Document Frequency
                    idf = math.log(len(sentences) / df) if df > 0 else 0
                    
                    # TF-IDF Score
                    tf_idf_vector[word_to_idx[word]] = tf * idf
            
            tf_idf_matrix.append(tf_idf_vector)
        
        # Score sentences
        sentence_scores = []
        for i, (sentence, tf_idf_vector) in enumerate(zip(sentences, tf_idf_matrix)):
            score = sum(tf_idf_vector) / len(tf_idf_vector) if tf_idf_vector else 0.0
            
            sentence_scores.append(SentenceScore(
                sentence=sentence,
                score=score,
                position=i,
                length=len(sentence_words[i]),
                keywords_count=len([x for x in tf_idf_vector if x > 0]),
                metadata={'tf_idf_vector': tf_idf_vector}
            ))
        
        return sentence_scores
    
    def _textrank_scoring(self, sentences: List[str], text: str) -> List[SentenceScore]:
        """Score sentences using TextRank algorithm."""
        # Create similarity matrix
        similarity_matrix = self._calculate_sentence_similarity_matrix(sentences)
        
        # Apply PageRank algorithm
        pagerank_scores = self._pagerank(similarity_matrix)
        
        sentence_scores = []
        for i, (sentence, score) in enumerate(zip(sentences, pagerank_scores)):
            words = word_tokenize(sentence.lower())
            words = [word for word in words if word.isalnum() and word not in self.stop_words]
            
            sentence_scores.append(SentenceScore(
                sentence=sentence,
                score=score,
                position=i,
                length=len(words),
                keywords_count=len(words),
                metadata={'similarity_scores': similarity_matrix[i].tolist()}
            ))
        
        return sentence_scores
    
    def _lsa_scoring(self, sentences: List[str], text: str) -> List[SentenceScore]:
        """Score sentences using Latent Semantic Analysis."""
        # This is a simplified LSA implementation
        # In a real system, you'd use libraries like sklearn or gensim
        
        # Create term-document matrix
        all_words = []
        sentence_words = []
        
        for sentence in sentences:
            words = word_tokenize(sentence.lower())
            words = [self.lemmatizer.lemmatize(word) for word in words 
                    if word.isalnum() and word not in self.stop_words]
            sentence_words.append(words)
            all_words.extend(words)
        
        vocabulary = list(set(all_words))
        
        # Create term-document matrix
        term_doc_matrix = []
        for words in sentence_words:
            vector = [words.count(word) for word in vocabulary]
            term_doc_matrix.append(vector)
        
        # Simple scoring based on term importance
        sentence_scores = []
        for i, (sentence, vector) in enumerate(zip(sentences, term_doc_matrix)):
            score = sum(vector) / len(vector) if vector else 0.0
            
            sentence_scores.append(SentenceScore(
                sentence=sentence,
                score=score,
                position=i,
                length=len(sentence_words[i]),
                keywords_count=len([x for x in vector if x > 0]),
                metadata={'term_vector': vector}
            ))
        
        return sentence_scores
    
    def _luhn_scoring(self, sentences: List[str], text: str) -> List[SentenceScore]:
        """Score sentences using Luhn's algorithm."""
        # Calculate word frequencies
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalnum() and word not in self.stop_words]
        word_freq = Counter(words)
        
        # Define significant words (high frequency)
        avg_freq = sum(word_freq.values()) / len(word_freq)
        significant_words = set(word for word, freq in word_freq.items() if freq > avg_freq)
        
        sentence_scores = []
        for i, sentence in enumerate(sentences):
            sentence_words = word_tokenize(sentence.lower())
            sentence_words = [word for word in sentence_words if word.isalnum()]
            
            # Find clusters of significant words
            score = self._calculate_luhn_score(sentence_words, significant_words)
            
            sentence_scores.append(SentenceScore(
                sentence=sentence,
                score=score,
                position=i,
                length=len(sentence_words),
                keywords_count=len([w for w in sentence_words if w in significant_words]),
                metadata={'significant_words': list(significant_words)}
            ))
        
        return sentence_scores
    
    def _edmundson_scoring(self, sentences: List[str], text: str) -> List[SentenceScore]:
        """Score sentences using Edmundson's method."""
        sentence_scores = []
        total_sentences = len(sentences)
        
        for i, sentence in enumerate(sentences):
            words = word_tokenize(sentence.lower())
            words = [word for word in words if word.isalnum() and word not in self.stop_words]
            
            # Position score (beginning and end sentences are important)
            position_score = 1.0 if i < 3 or i >= total_sentences - 3 else 0.5
            
            # Title words score (would need title as input in real implementation)
            title_score = 0.5  # Simplified
            
            # Cue phrase score
            cue_phrases = ['important', 'significant', 'conclude', 'summary', 'therefore', 'finally']
            cue_score = sum(1 for phrase in cue_phrases if phrase in sentence.lower()) * 0.3
            
            # Length score
            length_score = 1.0 if 10 <= len(words) <= 30 else 0.5
            
            total_score = position_score + title_score + cue_score + length_score
            
            sentence_scores.append(SentenceScore(
                sentence=sentence,
                score=total_score,
                position=i,
                length=len(words),
                keywords_count=len(words),
                metadata={
                    'position_score': position_score,
                    'cue_score': cue_score,
                    'length_score': length_score
                }
            ))
        
        return sentence_scores
    
    def _calculate_sentence_similarity_matrix(self, sentences: List[str]) -> np.ndarray:
        """Calculate similarity matrix between sentences."""
        n = len(sentences)
        similarity_matrix = np.zeros((n, n))
        
        # Preprocess sentences
        sentence_words = []
        for sentence in sentences:
            words = word_tokenize(sentence.lower())
            words = [self.lemmatizer.lemmatize(word) for word in words 
                    if word.isalnum() and word not in self.stop_words]
            sentence_words.append(set(words))
        
        # Calculate Jaccard similarity
        for i in range(n):
            for j in range(n):
                if i != j:
                    intersection = sentence_words[i].intersection(sentence_words[j])
                    union = sentence_words[i].union(sentence_words[j])
                    similarity = len(intersection) / len(union) if union else 0.0
                    similarity_matrix[i][j] = similarity
        
        return similarity_matrix
    
    def _pagerank(self, similarity_matrix: np.ndarray, damping: float = 0.85, 
                 max_iter: int = 100, tolerance: float = 1e-6) -> List[float]:
        """Apply PageRank algorithm to similarity matrix."""
        n = len(similarity_matrix)
        scores = np.ones(n) / n
        
        for _ in range(max_iter):
            new_scores = np.zeros(n)
            
            for i in range(n):
                for j in range(n):
                    if similarity_matrix[j][i] > 0:
                        new_scores[i] += similarity_matrix[j][i] * scores[j]
                
                new_scores[i] = (1 - damping) / n + damping * new_scores[i]
            
            if np.allclose(scores, new_scores, atol=tolerance):
                break
            
            scores = new_scores
        
        return scores.tolist()
    
    def _calculate_luhn_score(self, words: List[str], significant_words: set) -> float:
        """Calculate Luhn score for a sentence."""
        if not words:
            return 0.0
        
        # Find clusters of significant words
        clusters = []
        current_cluster = []
        
        for word in words:
            if word in significant_words:
                current_cluster.append(word)
            else:
                if current_cluster:
                    clusters.append(current_cluster)
                    current_cluster = []
        
        if current_cluster:
            clusters.append(current_cluster)
        
        if not clusters:
            return 0.0
        
        # Score based on cluster density
        max_score = 0.0
        for cluster in clusters:
            cluster_score = len(cluster) ** 2 / len(cluster)  # Simplified scoring
            max_score = max(max_score, cluster_score)
        
        return max_score
    
    def _select_top_sentences(self, sentence_scores: List[SentenceScore], 
                            summary_length: int) -> List[SentenceScore]:
        """Select top sentences for summary."""
        # Sort by score (descending)
        sorted_sentences = sorted(sentence_scores, key=lambda x: x.score, reverse=True)
        
        # Select top sentences
        selected = sorted_sentences[:summary_length]
        
        # Sort by original position to maintain coherence
        selected.sort(key=lambda x: x.position)
        
        return selected
    
    def _generate_extractive_summary(self, sentences: List[SentenceScore]) -> str:
        """Generate extractive summary from selected sentences."""
        return ' '.join(sentence.sentence for sentence in sentences)
    
    def _generate_abstractive_summary(self, sentences: List[SentenceScore], 
                                    original_text: str) -> str:
        """Generate abstractive summary (simplified implementation)."""
        # This is a simplified abstractive summarization
        # In a real system, you'd use neural networks or other advanced NLP techniques
        
        # Extract key concepts and generate new sentences
        key_phrases = self._extract_key_phrases(original_text)
        
        # For now, return a modified extractive summary
        extractive_summary = self._generate_extractive_summary(sentences)
        
        # Add key phrases context
        if key_phrases:
            summary = f"{extractive_summary} Key concepts include: {', '.join(key_phrases[:3])}."
        else:
            summary = extractive_summary
        
        return summary
    
    def _generate_hybrid_summary(self, sentences: List[SentenceScore], 
                                original_text: str) -> str:
        """Generate hybrid summary combining extractive and abstractive approaches."""
        extractive_part = self._generate_extractive_summary(sentences)
        
        # Add abstractive elements
        key_phrases = self._extract_key_phrases(original_text)
        
        if key_phrases:
            hybrid_summary = f"{extractive_part} This text primarily discusses {', '.join(key_phrases[:2])}."
        else:
            hybrid_summary = extractive_part
        
        return hybrid_summary
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract key phrases from text."""
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalnum() and word not in self.stop_words]
        
        # Use POS tagging to find noun phrases
        pos_tags = pos_tag(words)
        
        # Extract noun phrases
        noun_phrases = []
        current_phrase = []
        
        for word, pos in pos_tags:
            if pos.startswith('NN') or pos.startswith('JJ'):  # Nouns and adjectives
                current_phrase.append(word)
            else:
                if len(current_phrase) >= 2:
                    noun_phrases.append(' '.join(current_phrase))
                current_phrase = []
        
        if len(current_phrase) >= 2:
            noun_phrases.append(' '.join(current_phrase))
        
        # Return most frequent phrases
        phrase_freq = Counter(noun_phrases)
        return [phrase for phrase, _ in phrase_freq.most_common(10)]
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate readability score (simplified Flesch Reading Ease)."""
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        syllables = sum(self._count_syllables(word) for word in words)
        
        if not sentences or not words:
            return 0.0
        
        # Flesch Reading Ease formula
        score = 206.835 - 1.015 * (len(words) / len(sentences)) - 84.6 * (syllables / len(words))
        return max(0.0, min(100.0, score))
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word (simplified)."""
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        # Handle silent 'e'
        if word.endswith('e'):
            syllable_count -= 1
        
        return max(1, syllable_count)
    
    def _calculate_coherence(self, sentences: List[SentenceScore]) -> float:
        """Calculate coherence score for selected sentences."""
        if len(sentences) < 2:
            return 1.0
        
        # Simple coherence based on position proximity
        positions = [sentence.position for sentence in sentences]
        position_differences = []
        
        for i in range(1, len(positions)):
            position_differences.append(abs(positions[i] - positions[i-1]))
        
        # Lower differences indicate better coherence
        avg_difference = sum(position_differences) / len(position_differences)
        coherence = 1.0 / (1.0 + avg_difference * 0.1)  # Normalize to 0-1 range
        
        return coherence

# Example usage and testing
if __name__ == "__main__":
    summarizer = AdvancedTextSummarizer()
    
    sample_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. Colloquially, the term "artificial intelligence" is often used to describe machines that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem solving".
    
    The scope of AI is disputed: as machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. A quip in Tesler's Theorem says "AI is whatever hasn't been done yet." For instance, optical character recognition is frequently excluded from things considered to be AI, having become a routine technology.
    
    Modern machine learning techniques are at the heart of AI. Problems for AI applications include reasoning, knowledge representation, planning, learning, natural language processing, perception, and the ability to move and manipulate objects. General intelligence is among the field's long-term goals. Approaches include statistical methods, computational intelligence, and traditional symbolic AI.
    """
    
    # Test different summarization methods
    methods = [SummarizationMethod.TF_IDF, SummarizationMethod.TEXTRANK, SummarizationMethod.FREQUENCY_BASED]
    
    for method in methods:
        result = summarizer.summarize(sample_text, method=method, summary_length=2)
        print(f"\n{method.value.upper()} Summary:")
        print(result.summary)
        print(f"Compression ratio: {result.compression_ratio:.2f}")
        print(f"Processing time: {result.processing_time:.3f}s")