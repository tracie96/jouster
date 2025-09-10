from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import logging
from datetime import datetime

from models import TextAnalysisRequest, AnalysisResponse, SearchRequest
from llm_service import LLMService
from keyword_extractor import extract_keywords
from supabase_service import get_supabase_service
import os

app = FastAPI(
    title="Jouster LLM Knowledge Extractor",
    description="Extract summaries and structured data from text using LLM",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM service
try:
    llm_service = LLMService()
except ValueError as e:
    logging.error(f"LLM service initialization failed: {e}")
    llm_service = None

# Initialize Supabase service (required)
supabase_service = None
try:
    supabase_service = get_supabase_service()
    logging.info("Supabase service initialized successfully")
except Exception as e:
    logging.error(f"Supabase service initialization failed: {e}")
    supabase_service = None

@app.get("/")
async def root():
    return {"message": "Jouster LLM Knowledge Extractor API", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    llm_status = "available" if llm_service and llm_service.is_available() else "unavailable"
    supabase_status = "available" if supabase_service and supabase_service.is_available() else "unavailable"
    
    return {
        "status": "healthy" if supabase_status == "available" else "unhealthy",
        "llm_service": llm_status,
        "supabase": supabase_status
    }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(request: TextAnalysisRequest):
    """
    Analyze text and extract structured data using Supabase.
    """
    if not request.text or not request.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text cannot be empty"
        )
    
    if not supabase_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Supabase service is not available. Please check your configuration."
        )
    
    if not llm_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM service is not available. Please check your API key configuration."
        )
    
    try:
        llm_result = llm_service.analyze_text(request.text)
        
        # Extract keywords using our custom implementation
        keywords = extract_keywords(request.text, num_keywords=3)
        
        # Validate and prepare data for Supabase
        analysis_data = {
            "original_text": request.text,
            "summary": llm_result.get("summary") or "No summary available",
            "title": llm_result.get("title"),
            "topics": llm_result.get("topics") or ["general", "text", "analysis"],
            "sentiment": llm_result.get("sentiment") or "neutral",
            "keywords": keywords or ["text", "analysis", "content"]
        }
        
        # Ensure sentiment is valid and not None
        valid_sentiments = ["positive", "neutral", "negative"]
        sentiment = analysis_data["sentiment"]
        if sentiment is None or not isinstance(sentiment, str) or sentiment not in valid_sentiments:
            analysis_data["sentiment"] = "neutral"
        
        # Store in Supabase
        result = supabase_service.create_analysis(analysis_data)
        
        return AnalysisResponse(
            id=result["id"],
            summary=result["summary"],
            title=result["title"],
            topics=result["topics"],
            sentiment=result["sentiment"],
            keywords=result["keywords"],
            created_at=datetime.fromisoformat(result["created_at"].replace('Z', '+00:00'))
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Handle API failures
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Analysis failed: {str(e)}"
        )

@app.get("/search", response_model=List[AnalysisResponse])
async def search_analyses(topic: str):
    """
    Search for analyses by topic or keyword using Supabase.
    """
    if not topic or not topic.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Topic parameter cannot be empty"
        )
    
    if not supabase_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Supabase service is not available"
        )
    
    try:
        results = supabase_service.search_analyses(topic)
        
        return [
            AnalysisResponse(
                id=result["id"],
                summary=result["summary"],
                title=result["title"],
                topics=result["topics"],
                sentiment=result["sentiment"],
                keywords=result["keywords"],
                created_at=datetime.fromisoformat(result["created_at"].replace('Z', '+00:00'))
            )
            for result in results
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )

@app.get("/analyses", response_model=List[AnalysisResponse])
async def get_all_analyses():
    """
    Get all stored analyses from Supabase.
    """
    if not supabase_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Supabase service is not available"
        )
    
    try:
        results = supabase_service.get_all_analyses()
        
        return [
            AnalysisResponse(
                id=result["id"],
                summary=result["summary"],
                title=result["title"],
                topics=result["topics"],
                sentiment=result["sentiment"],
                keywords=result["keywords"],
                created_at=datetime.fromisoformat(result["created_at"].replace('Z', '+00:00'))
            )
            for result in results
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get analyses: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
