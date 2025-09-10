#!/usr/bin/env python3
"""
Unit tests for the Jouster LLM Knowledge Extractor
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from keyword_extractor import extract_keywords
from llm_service import LLMService

class TestKeywordExtractor(unittest.TestCase):
    """Test the keyword extraction functionality"""
    
    def test_extract_keywords_basic(self):
        """Test basic keyword extraction"""
        text = "Artificial Intelligence is revolutionizing technology and machine learning algorithms."
        keywords = extract_keywords(text, num_keywords=3)
        
        self.assertIsInstance(keywords, list)
        self.assertLessEqual(len(keywords), 3)
        expected_words = ['intelligence', 'technology', 'learning', 'algorithms']
        self.assertTrue(any(word in keywords for word in expected_words))
    
    def test_extract_keywords_empty_text(self):
        """Test keyword extraction with empty text"""
        keywords = extract_keywords("")
        self.assertEqual(keywords, [])
        
        keywords = extract_keywords("   ")
        self.assertEqual(keywords, [])
    
    def test_extract_keywords_short_text(self):
        """Test keyword extraction with very short text"""
        text = "AI is great."
        keywords = extract_keywords(text, num_keywords=3)
        self.assertIsInstance(keywords, list)
        self.assertLessEqual(len(keywords), 3)
    
    def test_extract_keywords_custom_count(self):
        """Test keyword extraction with custom count"""
        text = "Machine learning and artificial intelligence are transforming data science and analytics."
        keywords = extract_keywords(text, num_keywords=5)
        self.assertLessEqual(len(keywords), 5)

class TestLLMService(unittest.TestCase):
    """Test the LLM service functionality"""
    
    @patch('llm_service.OpenAI')
    def test_llm_service_initialization_success(self, mock_openai):
        """Test successful LLM service initialization"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            service = LLMService()
            self.assertIsNotNone(service.client)
            mock_openai.assert_called_once_with(api_key='test-key')
    
    def test_llm_service_initialization_no_key(self):
        """Test LLM service initialization without API key"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as context:
                LLMService()
            self.assertIn("OPENAI_API_KEY", str(context.exception))
    
    @patch('llm_service.OpenAI')
    def test_analyze_text_empty(self, mock_openai):
        """Test analyze_text with empty input"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            service = LLMService()
            
            with self.assertRaises(ValueError) as context:
                service.analyze_text("")
            self.assertIn("Text cannot be empty", str(context.exception))
    
    @patch('llm_service.OpenAI')
    def test_is_available_success(self, mock_openai):
        """Test is_available method when service is working"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = MagicMock()
            mock_openai.return_value = mock_client
            
            service = LLMService()
            result = service.is_available()
            
            self.assertTrue(result)
    
    @patch('llm_service.OpenAI')
    def test_is_available_failure(self, mock_openai):
        """Test is_available method when service fails"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            mock_client = MagicMock()
            mock_client.chat.completions.create.side_effect = Exception("API Error")
            mock_openai.return_value = mock_client
            
            service = LLMService()
            result = service.is_available()
            
            self.assertFalse(result)

if __name__ == '__main__':
    unittest.main(verbosity=2)
