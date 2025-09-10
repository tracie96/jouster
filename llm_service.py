import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.client = OpenAI(api_key=api_key)
    
    def analyze_text(self, text: str) -> dict:
        """
        Use LLM to analyze text and extract structured data.
        Returns a dictionary with summary, title, topics, and sentiment.
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        prompt = f"""
        Analyze the following text and provide a structured response in JSON format:
        
        Text: "{text}"
        
        Please provide:
        1. A 1-2 sentence summary
        2. A title (if one can be inferred, otherwise null)
        3. Three key topics/themes
        4. Sentiment analysis (positive, neutral, or negative)
        
        Respond with valid JSON in this exact format:
        {{
            "summary": "1-2 sentence summary here",
            "title": "title or null",
            "topics": ["topic1", "topic2", "topic3"],
            "sentiment": "positive|neutral|negative"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that analyzes text and extracts structured information. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Trying to parse JSON response
            try:
                result = json.loads(content)
                
                # Validating and fixing the result
                validated_result = self._validate_result(result)
                return validated_result
                
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails.
                return {
                    "summary": content[:200] + "..." if len(content) > 200 else content,
                    "title": None,
                    "topics": ["general", "text", "analysis"],
                    "sentiment": "neutral"
                }
                
        except Exception as e:
            raise Exception(f"LLM API error: {str(e)}")
    
    def _validate_result(self, result: dict) -> dict:
        """Validate and fix the LLM result to ensure all required fields are present"""
        if not result.get("summary") or not result["summary"].strip():
            result["summary"] = "No summary available"
        
        if result.get("title") is not None and not isinstance(result["title"], str):
            result["title"] = None
        
        if not isinstance(result.get("topics"), list) or len(result["topics"]) < 3:
            result["topics"] = ["general", "text", "analysis"]
        
        valid_sentiments = ["positive", "neutral", "negative"]
        sentiment = result.get("sentiment")
        
        # Handle None or empty sentiment
        if sentiment is None or not isinstance(sentiment, str):
            sentiment = "neutral"
        else:
            sentiment = sentiment.lower().strip()
            if sentiment not in valid_sentiments:
                sentiment = "neutral"  # Default fallback
        
        result["sentiment"] = sentiment
        
        return result
    
    def is_available(self) -> bool:
        """Check if the LLM service is available."""
        try:
            # Simple test call
            self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            return True
        except:
            return False
