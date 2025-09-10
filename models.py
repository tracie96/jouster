from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TextAnalysisRequest(BaseModel):
    text: str

class AnalysisResponse(BaseModel):
    id: int
    summary: str
    title: Optional[str]
    topics: List[str]
    sentiment: str
    keywords: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class SearchRequest(BaseModel):
    topic: str
