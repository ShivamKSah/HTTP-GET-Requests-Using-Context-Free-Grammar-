"""
Intelligent Query Handling System

This module provides advanced NLP-based query processing, intent recognition,
entity extraction, and intelligent response generation.
"""

import re
import nltk
import spacy
from typing import Dict, List, Any, Optional, Tuple, Union
from collections import defaultdict, Counter
from datetime import datetime
import json
from dataclasses import dataclass, asdict
from enum import Enum

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
except:
    pass

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.sentiment import SentimentIntensityAnalyzer

class QueryType(Enum):
    QUESTION = "question"
    COMMAND = "command"
    SEARCH = "search"
    COMPARISON = "comparison"
    DEFINITION = "definition"
    INSTRUCTION = "instruction"
    UNKNOWN = "unknown"

class Intent(Enum):
    GET_INFORMATION = "get_information"
    PERFORM_ACTION = "perform_action"
    SEARCH_CONTENT = "search_content"
    COMPARE_ITEMS = "compare_items"
    GET_DEFINITION = "get_definition"
    GET_INSTRUCTIONS = "get_instructions"
    ANALYZE_DATA = "analyze_data"
    GENERATE_CONTENT = "generate_content"
    UNKNOWN = "unknown"

class EntityType(Enum):
    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    DATE = "date"
    TIME = "time"
    MONEY = "money"
    PERCENT = "percent"
    PRODUCT = "product"
    TECHNOLOGY = "technology"
    CONCEPT = "concept"

@dataclass
class Entity:
    """Extracted entity from query."""
    text: str
    entity_type: EntityType
    confidence: float
    start_pos: int
    end_pos: int
    metadata: Dict[str, Any]

@dataclass
class QueryIntent:
    """Detected intent from query."""
    intent: Intent
    confidence: float
    reasoning: str
    parameters: Dict[str, Any]

@dataclass
class QueryAnalysis:
    """Complete analysis of a user query."""
    original_query: str
    cleaned_query: str
    query_type: QueryType
    intent: QueryIntent
    entities: List[Entity]
    keywords: List[str]
    sentiment: Dict[str, float]
    complexity_score: float
    language: str
    timestamp: str

@dataclass
class QueryResponse:
    """Response to a user query."""
    query_analysis: QueryAnalysis
    response_text: str
    confidence: float
    sources: List[str]
    suggestions: List[str]
    follow_up_questions: List[str]
    processing_time: float
    metadata: Dict[str, Any]

class IntelligentQueryHandler:
    """Advanced NLP-based query processing system."""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = PorterStemmer()
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Load spaCy model if available
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Warning: spaCy English model not found. Some features may be limited.")
            self.nlp = None
        
        # Intent patterns
        self.intent_patterns = self._init_intent_patterns()
        
        # Entity patterns
        self.entity_patterns = self._init_entity_patterns()
        
        # Question words
        self.question_words = {
            'what', 'when', 'where', 'who', 'why', 'how', 'which', 'whose', 'whom'
        }
        
        # Command words
        self.command_words = {
            'create', 'make', 'build', 'generate', 'develop', 'design', 'implement',
            'show', 'display', 'list', 'find', 'search', 'get', 'fetch', 'retrieve',
            'compare', 'analyze', 'evaluate', 'explain', 'describe', 'summarize'
        }
    
    def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> QueryResponse:
        """
        Process a user query and generate intelligent response.
        
        Args:
            query: User's input query
            context: Optional context information
            
        Returns:
            QueryResponse with analysis and generated response
        """
        start_time = datetime.now()
        
        # Analyze query
        analysis = self.analyze_query(query)
        
        # Generate response based on analysis
        response_text, confidence, sources = self._generate_response(analysis, context)
        
        # Generate suggestions and follow-up questions
        suggestions = self._generate_suggestions(analysis)
        follow_up_questions = self._generate_follow_up_questions(analysis)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return QueryResponse(
            query_analysis=analysis,
            response_text=response_text,
            confidence=confidence,
            sources=sources,
            suggestions=suggestions,
            follow_up_questions=follow_up_questions,
            processing_time=processing_time,
            metadata={
                'context_used': context is not None,
                'spacy_available': self.nlp is not None,
                'analysis_components': ['intent', 'entities', 'sentiment', 'keywords']
            }
        )
    
    def analyze_query(self, query: str) -> QueryAnalysis:
        """Analyze user query for intent, entities, and other features."""
        # Clean query
        cleaned_query = self._clean_query(query)
        
        # Detect query type
        query_type = self._detect_query_type(cleaned_query)
        
        # Detect intent
        intent = self._detect_intent(cleaned_query, query_type)
        
        # Extract entities
        entities = self._extract_entities(cleaned_query)
        
        # Extract keywords
        keywords = self._extract_keywords(cleaned_query)
        
        # Analyze sentiment
        sentiment = self._analyze_sentiment(cleaned_query)
        
        # Calculate complexity
        complexity_score = self._calculate_complexity(cleaned_query)
        
        # Detect language (simplified - assumes English)
        language = "en"
        
        return QueryAnalysis(
            original_query=query,
            cleaned_query=cleaned_query,
            query_type=query_type,
            intent=intent,
            entities=entities,
            keywords=keywords,
            sentiment=sentiment,
            complexity_score=complexity_score,
            language=language,
            timestamp=datetime.now().isoformat()
        )
    
    def _clean_query(self, query: str) -> str:
        """Clean and normalize the query."""
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', query.strip())
        
        # Fix common typos and normalize punctuation
        cleaned = re.sub(r'[.]{2,}', '.', cleaned)
        cleaned = re.sub(r'[?]{2,}', '?', cleaned)
        cleaned = re.sub(r'[!]{2,}', '!', cleaned)
        
        return cleaned
    
    def _detect_query_type(self, query: str) -> QueryType:
        """Detect the type of query."""
        query_lower = query.lower()
        
        # Check for question words
        if any(word in query_lower for word in self.question_words):
            return QueryType.QUESTION
        
        # Check for question marks
        if '?' in query:
            return QueryType.QUESTION
        
        # Check for command words
        first_word = query_lower.split()[0] if query_lower.split() else ""
        if first_word in self.command_words:
            return QueryType.COMMAND
        
        # Check for search patterns
        if any(phrase in query_lower for phrase in ['search for', 'find', 'look for', 'show me']):
            return QueryType.SEARCH
        
        # Check for comparison patterns
        if any(phrase in query_lower for phrase in ['compare', 'vs', 'versus', 'difference between']):
            return QueryType.COMPARISON
        
        # Check for definition patterns
        if any(phrase in query_lower for phrase in ['what is', 'define', 'definition of', 'meaning of']):
            return QueryType.DEFINITION
        
        # Check for instruction patterns
        if any(phrase in query_lower for phrase in ['how to', 'steps to', 'tutorial', 'guide']):
            return QueryType.INSTRUCTION
        
        return QueryType.UNKNOWN
    
    def _detect_intent(self, query: str, query_type: QueryType) -> QueryIntent:
        """Detect the intent behind the query."""
        query_lower = query.lower()
        
        # Map query types to intents
        type_to_intent = {
            QueryType.QUESTION: Intent.GET_INFORMATION,
            QueryType.COMMAND: Intent.PERFORM_ACTION,
            QueryType.SEARCH: Intent.SEARCH_CONTENT,
            QueryType.COMPARISON: Intent.COMPARE_ITEMS,
            QueryType.DEFINITION: Intent.GET_DEFINITION,
            QueryType.INSTRUCTION: Intent.GET_INSTRUCTIONS
        }
        
        base_intent = type_to_intent.get(query_type, Intent.UNKNOWN)
        
        # Refine intent based on patterns
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return QueryIntent(
                        intent=intent,
                        confidence=0.8,
                        reasoning=f"Matched pattern: {pattern}",
                        parameters=self._extract_intent_parameters(query, intent)
                    )
        
        # Default intent based on query type
        confidence = 0.6 if base_intent != Intent.UNKNOWN else 0.3
        
        return QueryIntent(
            intent=base_intent,
            confidence=confidence,
            reasoning=f"Inferred from query type: {query_type.value}",
            parameters=self._extract_intent_parameters(query, base_intent)
        )
    
    def _extract_entities(self, query: str) -> List[Entity]:
        """Extract entities from the query."""
        entities = []
        
        # Use spaCy if available
        if self.nlp:
            doc = self.nlp(query)
            for ent in doc.ents:
                entity_type = self._map_spacy_entity_type(ent.label_)
                entities.append(Entity(
                    text=ent.text,
                    entity_type=entity_type,
                    confidence=0.8,
                    start_pos=ent.start_char,
                    end_pos=ent.end_char,
                    metadata={'spacy_label': ent.label_}
                ))
        
        # Pattern-based entity extraction
        pattern_entities = self._extract_pattern_entities(query)
        entities.extend(pattern_entities)
        
        # Remove duplicates
        unique_entities = []
        seen_texts = set()
        for entity in entities:
            if entity.text.lower() not in seen_texts:
                unique_entities.append(entity)
                seen_texts.add(entity.text.lower())
        
        return unique_entities
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract important keywords from the query."""
        words = word_tokenize(query.lower())
        
        # Remove stop words and punctuation
        keywords = [word for word in words 
                   if word.isalnum() and word not in self.stop_words and len(word) > 2]
        
        # Add stemmed versions
        stemmed_keywords = [self.stemmer.stem(word) for word in keywords]
        
        # Combine and remove duplicates
        all_keywords = list(set(keywords + stemmed_keywords))
        
        # Sort by word frequency in query
        word_freq = Counter(words)
        sorted_keywords = sorted(all_keywords, 
                               key=lambda x: word_freq.get(x, 0), reverse=True)
        
        return sorted_keywords[:10]  # Return top 10 keywords
    
    def _analyze_sentiment(self, query: str) -> Dict[str, float]:
        """Analyze sentiment of the query."""
        scores = self.sentiment_analyzer.polarity_scores(query)
        
        return {
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'compound': scores['compound']
        }
    
    def _calculate_complexity(self, query: str) -> float:
        """Calculate complexity score of the query."""
        words = word_tokenize(query)
        sentences = sent_tokenize(query)
        
        # Factors affecting complexity
        word_count = len(words)
        sentence_count = len(sentences)
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        question_words_count = sum(1 for word in words if word.lower() in self.question_words)
        
        # Normalize to 0-1 range
        complexity = (
            min(word_count / 50, 1.0) * 0.3 +  # Word count factor
            min(sentence_count / 5, 1.0) * 0.2 +  # Sentence count factor
            min(avg_word_length / 10, 1.0) * 0.3 +  # Average word length
            min(question_words_count / 3, 1.0) * 0.2  # Question complexity
        )
        
        return complexity
    
    def _generate_response(self, analysis: QueryAnalysis, 
                         context: Optional[Dict[str, Any]] = None) -> Tuple[str, float, List[str]]:
        """Generate response based on query analysis."""
        intent = analysis.intent.intent
        query_type = analysis.query_type
        
        # Base response templates
        responses = {
            Intent.GET_INFORMATION: self._generate_information_response,
            Intent.SEARCH_CONTENT: self._generate_search_response,
            Intent.GET_DEFINITION: self._generate_definition_response,
            Intent.GET_INSTRUCTIONS: self._generate_instruction_response,
            Intent.COMPARE_ITEMS: self._generate_comparison_response,
            Intent.ANALYZE_DATA: self._generate_analysis_response,
            Intent.PERFORM_ACTION: self._generate_action_response
        }
        
        generator = responses.get(intent, self._generate_default_response)
        response_text, confidence, sources = generator(analysis, context)
        
        return response_text, confidence, sources
    
    def _generate_information_response(self, analysis: QueryAnalysis, 
                                     context: Optional[Dict[str, Any]]) -> Tuple[str, float, List[str]]:
        """Generate response for information requests."""
        entities = [e.text for e in analysis.entities]
        keywords = analysis.keywords[:3]
        
        if entities:
            response = f"Based on your query about {', '.join(entities)}, here's what I found: "
            response += f"This relates to {', '.join(keywords)} and involves key concepts in our database."
        else:
            response = f"Your query about {', '.join(keywords)} requires more specific information. "
            response += "Could you provide more details about what specific aspect you're interested in?"
        
        return response, 0.7, ["internal_database", "query_analysis"]
    
    def _generate_search_response(self, analysis: QueryAnalysis, 
                                context: Optional[Dict[str, Any]]) -> Tuple[str, float, List[str]]:
        """Generate response for search requests."""
        keywords = analysis.keywords[:5]
        
        response = f"Searching for content related to: {', '.join(keywords)}. "
        response += "Here are the most relevant results from our database. "
        response += "Would you like me to filter these results further?"
        
        return response, 0.8, ["search_engine", "content_database"]
    
    def _generate_definition_response(self, analysis: QueryAnalysis, 
                                    context: Optional[Dict[str, Any]]) -> Tuple[str, float, List[str]]:
        """Generate response for definition requests."""
        entities = [e.text for e in analysis.entities if e.entity_type in [EntityType.CONCEPT, EntityType.TECHNOLOGY]]
        
        if entities:
            term = entities[0]
            response = f"Definition of '{term}': This is a fundamental concept in computer science. "
            response += "It relates to our CFG QODER project's focus on formal languages and network protocols. "
            response += "Would you like a more detailed explanation or related examples?"
        else:
            response = "I'd be happy to provide a definition. Could you specify which term you'd like me to define?"
        
        return response, 0.6, ["definition_database", "educational_content"]
    
    def _generate_instruction_response(self, analysis: QueryAnalysis, 
                                     context: Optional[Dict[str, Any]]) -> Tuple[str, float, List[str]]:
        """Generate response for instruction requests."""
        keywords = analysis.keywords[:3]
        
        response = f"Here's how to work with {', '.join(keywords)}: "
        response += "1. Start by understanding the basic concepts. "
        response += "2. Review the relevant documentation in our system. "
        response += "3. Try the interactive examples. "
        response += "Would you like me to elaborate on any of these steps?"
        
        return response, 0.7, ["tutorial_system", "documentation"]
    
    def _generate_comparison_response(self, analysis: QueryAnalysis, 
                                    context: Optional[Dict[str, Any]]) -> Tuple[str, float, List[str]]:
        """Generate response for comparison requests."""
        entities = [e.text for e in analysis.entities]
        
        if len(entities) >= 2:
            response = f"Comparing {entities[0]} and {entities[1]}: "
            response += "Both have distinct characteristics and use cases. "
            response += "Let me highlight the key differences and similarities. "
            response += "Which specific aspects would you like me to focus on?"
        else:
            response = "To provide a comparison, I need at least two items to compare. "
            response += "Could you specify what you'd like me to compare?"
        
        return response, 0.6, ["comparison_engine", "knowledge_base"]
    
    def _generate_analysis_response(self, analysis: QueryAnalysis, 
                                  context: Optional[Dict[str, Any]]) -> Tuple[str, float, List[str]]:
        """Generate response for analysis requests."""
        keywords = analysis.keywords[:3]
        
        response = f"Analyzing the data related to {', '.join(keywords)}: "
        response += "Based on the available information, I can provide insights on patterns, trends, and relationships. "
        response += "What specific type of analysis are you looking for?"
        
        return response, 0.7, ["analytics_engine", "data_processor"]
    
    def _generate_action_response(self, analysis: QueryAnalysis, 
                                context: Optional[Dict[str, Any]]) -> Tuple[str, float, List[str]]:
        """Generate response for action requests."""
        keywords = analysis.keywords[:3]
        
        response = f"To perform the requested action involving {', '.join(keywords)}: "
        response += "I'll need to process this through the appropriate system modules. "
        response += "Please confirm if you'd like me to proceed with this action."
        
        return response, 0.5, ["action_processor", "system_interface"]
    
    def _generate_default_response(self, analysis: QueryAnalysis, 
                                 context: Optional[Dict[str, Any]]) -> Tuple[str, float, List[str]]:
        """Generate default response for unknown intents."""
        response = "I understand you're asking about something, but I need more context to provide a helpful response. "
        response += "Could you rephrase your question or provide more specific details?"
        
        return response, 0.3, ["fallback_system"]
    
    def _generate_suggestions(self, analysis: QueryAnalysis) -> List[str]:
        """Generate helpful suggestions based on query analysis."""
        suggestions = []
        
        # Suggestions based on intent
        intent = analysis.intent.intent
        
        if intent == Intent.GET_INFORMATION:
            suggestions.extend([
                "Try asking for specific examples",
                "Request more detailed explanations", 
                "Ask about related concepts"
            ])
        elif intent == Intent.SEARCH_CONTENT:
            suggestions.extend([
                "Use more specific keywords",
                "Try different search terms",
                "Filter results by category"
            ])
        elif intent == Intent.GET_DEFINITION:
            suggestions.extend([
                "Ask for examples of usage",
                "Request related terminology",
                "Inquire about practical applications"
            ])
        
        # Add general suggestions
        suggestions.extend([
            "Explore the interactive examples",
            "Check the documentation",
            "Try the visualization tools"
        ])
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def _generate_follow_up_questions(self, analysis: QueryAnalysis) -> List[str]:
        """Generate relevant follow-up questions."""
        questions = []
        keywords = analysis.keywords[:3]
        
        if analysis.query_type == QueryType.QUESTION:
            questions.extend([
                f"Would you like to know more about {keywords[0] if keywords else 'this topic'}?",
                "Are you looking for practical examples?",
                "Would you like to see related concepts?"
            ])
        elif analysis.query_type == QueryType.COMMAND:
            questions.extend([
                "Would you like step-by-step instructions?",
                "Do you need any prerequisites explained?",
                "Should I show you examples?"
            ])
        
        # Add context-specific questions
        questions.extend([
            "Is this related to our CFG parsing features?",
            "Are you working on a specific project?",
            "Would visualization help explain this?"
        ])
        
        return questions[:3]  # Return top 3 questions
    
    def _init_intent_patterns(self) -> Dict[Intent, List[str]]:
        """Initialize intent detection patterns."""
        return {
            Intent.GET_INFORMATION: [
                r'\b(what|where|when|who|why|how)\b.*\?',
                r'\b(tell me|explain|describe)\b',
                r'\b(information about|details on)\b'
            ],
            Intent.SEARCH_CONTENT: [
                r'\b(search|find|look for|show me)\b',
                r'\b(list|display|get)\b.*\b(all|every)\b'
            ],
            Intent.GET_DEFINITION: [
                r'\b(what is|define|definition|meaning)\b',
                r'\b(means|refers to)\b'
            ],
            Intent.GET_INSTRUCTIONS: [
                r'\b(how to|steps|tutorial|guide)\b',
                r'\b(teach me|show me how)\b'
            ],
            Intent.COMPARE_ITEMS: [
                r'\b(compare|vs|versus|difference)\b',
                r'\b(better|worse|similar)\b'
            ],
            Intent.ANALYZE_DATA: [
                r'\b(analyze|analysis|examine|study)\b',
                r'\b(trends|patterns|insights)\b'
            ]
        }
    
    def _init_entity_patterns(self) -> Dict[EntityType, List[str]]:
        """Initialize entity extraction patterns."""
        return {
            EntityType.TECHNOLOGY: [
                r'\b(HTTP|TCP|IP|CFG|FSA|PDA|API|JSON|XML)\b',
                r'\b(algorithm|protocol|framework|library)\b'
            ],
            EntityType.CONCEPT: [
                r'\b(parsing|tokenization|validation|analysis)\b',
                r'\b(grammar|syntax|semantic|lexical)\b'
            ],
            EntityType.DATE: [
                r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
                r'\b(today|yesterday|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b'
            ],
            EntityType.TIME: [
                r'\b\d{1,2}:\d{2}(?::\d{2})?\s*(?:am|pm)?\b'
            ]
        }
    
    def _extract_pattern_entities(self, query: str) -> List[Entity]:
        """Extract entities using pattern matching."""
        entities = []
        
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, query, re.IGNORECASE)
                for match in matches:
                    entities.append(Entity(
                        text=match.group(),
                        entity_type=entity_type,
                        confidence=0.6,
                        start_pos=match.start(),
                        end_pos=match.end(),
                        metadata={'pattern': pattern}
                    ))
        
        return entities
    
    def _map_spacy_entity_type(self, spacy_label: str) -> EntityType:
        """Map spaCy entity labels to our entity types."""
        mapping = {
            'PERSON': EntityType.PERSON,
            'ORG': EntityType.ORGANIZATION,
            'GPE': EntityType.LOCATION,
            'LOC': EntityType.LOCATION,
            'DATE': EntityType.DATE,
            'TIME': EntityType.TIME,
            'MONEY': EntityType.MONEY,
            'PERCENT': EntityType.PERCENT,
            'PRODUCT': EntityType.PRODUCT
        }
        
        return mapping.get(spacy_label, EntityType.CONCEPT)
    
    def _extract_intent_parameters(self, query: str, intent: Intent) -> Dict[str, Any]:
        """Extract parameters specific to the detected intent."""
        parameters = {}
        
        if intent == Intent.SEARCH_CONTENT:
            # Extract search terms
            search_terms = re.findall(r'search for\s+([^.?!]+)', query, re.IGNORECASE)
            if search_terms:
                parameters['search_terms'] = search_terms[0].strip()
        
        elif intent == Intent.COMPARE_ITEMS:
            # Extract comparison targets
            vs_match = re.search(r'(\w+)\s+(?:vs|versus)\s+(\w+)', query, re.IGNORECASE)
            if vs_match:
                parameters['item1'] = vs_match.group(1)
                parameters['item2'] = vs_match.group(2)
        
        elif intent == Intent.GET_DEFINITION:
            # Extract term to define
            define_match = re.search(r'(?:what is|define|definition of)\s+([^.?!]+)', query, re.IGNORECASE)
            if define_match:
                parameters['term'] = define_match.group(1).strip()
        
        return parameters

# Example usage and testing
if __name__ == "__main__":
    handler = IntelligentQueryHandler()
    
    test_queries = [
        "What is a context-free grammar?",
        "How to parse HTTP requests?",
        "Compare CFG and regular expressions",
        "Search for TCP protocol examples",
        "Explain the difference between FSA and PDA",
        "Create a new parsing rule for JSON"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        response = handler.process_query(query)
        print(f"Intent: {response.query_analysis.intent.intent.value}")
        print(f"Entities: {[e.text for e in response.query_analysis.entities]}")
        print(f"Response: {response.response_text}")
        print(f"Confidence: {response.confidence:.2f}")