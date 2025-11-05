"""
Document Classification System

This module provides document classification using machine learning approaches.
"""

import re
import nltk
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter, defaultdict
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
except:
    pass

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

class DocumentCategory(Enum):
    TECHNICAL_DOCUMENTATION = "technical_documentation"
    RESEARCH_PAPER = "research_paper"
    TUTORIAL = "tutorial"
    API_DOCUMENTATION = "api_documentation"
    SPECIFICATION = "specification"
    USER_GUIDE = "user_guide"
    FAQ = "faq"
    BLOG_POST = "blog_post"
    UNKNOWN = "unknown"

class ClassificationMethod(Enum):
    NAIVE_BAYES = "naive_bayes"
    RULE_BASED = "rule_based"
    ENSEMBLE = "ensemble"

@dataclass
class ClassificationResult:
    """Result of document classification."""
    document_text: str
    predicted_category: DocumentCategory
    confidence: float
    probability_distribution: Dict[DocumentCategory, float]
    method_used: ClassificationMethod
    reasoning: List[str]
    processing_time: float
    timestamp: str

class DocumentClassifier:
    """Document classification system with multiple ML approaches."""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.category_keywords = self._init_category_keywords()
        self.models = {}
        self.is_trained = False
        
    def classify(self, document_text: str, 
                method: ClassificationMethod = ClassificationMethod.RULE_BASED) -> ClassificationResult:
        """Classify a document using the specified method."""
        start_time = datetime.now()
        
        # Extract features
        features = self._extract_features(document_text)
        
        # Classify based on method
        if method == ClassificationMethod.RULE_BASED:
            category, confidence, probabilities, reasoning = self._classify_rule_based(features)
        elif method == ClassificationMethod.NAIVE_BAYES:
            category, confidence, probabilities, reasoning = self._classify_naive_bayes(features)
        else:  # ENSEMBLE
            category, confidence, probabilities, reasoning = self._classify_ensemble(features)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return ClassificationResult(
            document_text=document_text,
            predicted_category=category,
            confidence=confidence,
            probability_distribution=probabilities,
            method_used=method,
            reasoning=reasoning,
            processing_time=processing_time,
            timestamp=datetime.now().isoformat()
        )
    
    def _extract_features(self, text: str) -> Dict[str, Any]:
        """Extract features from document."""
        words = word_tokenize(text.lower())
        filtered_words = [word for word in words if word.isalnum() and word not in self.stop_words]
        
        features = {
            'word_count': Counter(filtered_words),
            'total_words': len(filtered_words),
            'question_density': text.count('?') / len(text.split('.')) if text.split('.') else 0,
            'code_density': len(re.findall(r'[{}[\]();]|\/\/|\/\*', text)) / len(filtered_words) if filtered_words else 0,
            'technical_density': sum(1 for word in filtered_words if word in ['algorithm', 'protocol', 'implementation', 'system']) / len(filtered_words) if filtered_words else 0,
            'academic_density': sum(1 for word in filtered_words if word in ['research', 'study', 'analysis', 'methodology']) / len(filtered_words) if filtered_words else 0
        }
        
        return features
    
    def _classify_rule_based(self, features: Dict[str, Any]) -> Tuple[DocumentCategory, float, Dict[DocumentCategory, float], List[str]]:
        """Classify using rule-based approach."""
        category_scores = defaultdict(float)
        reasoning = []
        
        # Score based on keywords
        for category, keywords in self.category_keywords.items():
            score = sum(features['word_count'].get(keyword, 0) for keyword in keywords)
            
            # Add feature bonuses
            if category == DocumentCategory.FAQ and features['question_density'] > 0.1:
                score += 5
                reasoning.append(f"{category.value}: high question density")
            
            if category == DocumentCategory.API_DOCUMENTATION and features['code_density'] > 0.05:
                score += 5
                reasoning.append(f"{category.value}: high code density")
            
            category_scores[category] = score
        
        # Normalize to probabilities
        total_score = sum(category_scores.values()) or 1
        probabilities = {cat: score / total_score for cat, score in category_scores.items()}
        
        best_category = max(category_scores.items(), key=lambda x: x[1])[0] if category_scores else DocumentCategory.UNKNOWN
        confidence = probabilities.get(best_category, 0.0)
        
        return best_category, confidence, probabilities, reasoning
    
    def _classify_naive_bayes(self, features: Dict[str, Any]) -> Tuple[DocumentCategory, float, Dict[DocumentCategory, float], List[str]]:
        """Classify using simplified Naive Bayes."""
        # Simplified implementation - in practice you'd train on labeled data
        category_scores = {}
        reasoning = ["Using simplified Naive Bayes"]
        
        for category in DocumentCategory:
            # Simple scoring based on keyword presence
            keywords = self.category_keywords.get(category, [])
            score = sum(features['word_count'].get(keyword, 0) for keyword in keywords)
            category_scores[category] = score + 1  # Smoothing
        
        total_score = sum(category_scores.values())
        probabilities = {cat: score / total_score for cat, score in category_scores.items()}
        
        best_category = max(probabilities.items(), key=lambda x: x[1])[0]
        confidence = probabilities[best_category]
        
        return best_category, confidence, probabilities, reasoning
    
    def _classify_ensemble(self, features: Dict[str, Any]) -> Tuple[DocumentCategory, float, Dict[DocumentCategory, float], List[str]]:
        """Classify using ensemble of methods."""
        # Get predictions from both methods
        rule_cat, rule_conf, rule_probs, rule_reasoning = self._classify_rule_based(features)
        nb_cat, nb_conf, nb_probs, nb_reasoning = self._classify_naive_bayes(features)
        
        # Combine probabilities (weighted average)
        combined_probs = defaultdict(float)
        for category in DocumentCategory:
            combined_probs[category] = 0.6 * rule_probs.get(category, 0) + 0.4 * nb_probs.get(category, 0)
        
        best_category = max(combined_probs.items(), key=lambda x: x[1])[0]
        confidence = combined_probs[best_category]
        
        reasoning = ["Ensemble method:"] + rule_reasoning + nb_reasoning
        
        return best_category, confidence, dict(combined_probs), reasoning
    
    def _init_category_keywords(self) -> Dict[DocumentCategory, List[str]]:
        """Initialize category-specific keywords."""
        return {
            DocumentCategory.TECHNICAL_DOCUMENTATION: [
                'specification', 'implementation', 'architecture', 'design', 'system', 'protocol'
            ],
            DocumentCategory.RESEARCH_PAPER: [
                'abstract', 'methodology', 'experiment', 'results', 'conclusion', 'hypothesis'
            ],
            DocumentCategory.TUTORIAL: [
                'tutorial', 'guide', 'step', 'instructions', 'learn', 'example'
            ],
            DocumentCategory.API_DOCUMENTATION: [
                'api', 'endpoint', 'request', 'response', 'parameter', 'method', 'function'
            ],
            DocumentCategory.SPECIFICATION: [
                'specification', 'standard', 'rfc', 'protocol', 'format', 'syntax'
            ],
            DocumentCategory.USER_GUIDE: [
                'user', 'guide', 'manual', 'instructions', 'configuration', 'setup'
            ],
            DocumentCategory.FAQ: [
                'faq', 'frequently', 'asked', 'questions', 'answer', 'problem'
            ],
            DocumentCategory.BLOG_POST: [
                'blog', 'post', 'article', 'opinion', 'thoughts', 'experience'
            ]
        }

# Example usage
if __name__ == "__main__":
    classifier = DocumentClassifier()
    
    sample_texts = [
        "This API provides endpoints for user authentication. Send POST requests to /api/login with username and password parameters.",
        "How do I configure the system? Follow these steps: 1. Install the software 2. Edit the config file 3. Restart the service.",
        "Our research methodology involved analyzing 1000 samples using statistical methods. The results show significant correlation."
    ]
    
    for text in sample_texts:
        result = classifier.classify(text)
        print(f"\nText: {text[:50]}...")
        print(f"Category: {result.predicted_category.value}")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Method: {result.method_used.value}")