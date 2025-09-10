import os
from supabase import create_client, Client
from typing import List, Dict, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class SupabaseService:
    def __init__(self):
        """Initialize Supabase client"""
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables are required")
        
        # Remove quotes if present
        self.url = self.url.strip("'\"")
        self.key = self.key.strip("'\"")
        
        self.supabase: Client = create_client(self.url, self.key)
    
    def create_analysis(self, analysis_data: Dict) -> Dict:
        """Create a new analysis record"""
        try:
            result = self.supabase.table("analyses").insert(analysis_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            raise Exception(f"Failed to create analysis: {str(e)}")
    
    def get_analysis(self, analysis_id: int) -> Optional[Dict]:
        """Get a single analysis by ID"""
        try:
            result = self.supabase.table("analyses").select("*").eq("id", analysis_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            raise Exception(f"Failed to get analysis: {str(e)}")
    
    def get_all_analyses(self) -> List[Dict]:
        """Get all analyses ordered by creation date"""
        try:
            result = self.supabase.table("analyses").select("*").order("created_at", desc=True).execute()
            return result.data or []
        except Exception as e:
            raise Exception(f"Failed to get analyses: {str(e)}")
    
    def search_analyses(self, topic: str) -> List[Dict]:
        """Search analyses by topic or keyword"""
        try:
            # Get all analyses and filter in Python for more reliable results
            all_analyses = self.supabase.table("analyses").select("*").execute()
            
            if not all_analyses.data:
                return []
            
            # Filter results that contain the topic in any relevant field
            matching_analyses = []
            topic_lower = topic.lower()
            
            for analysis in all_analyses.data:
                # Check in topics (JSON array)
                topics = analysis.get("topics", [])
                if any(topic_lower in str(t).lower() for t in topics):
                    matching_analyses.append(analysis)
                    continue
                
                # Check in keywords (JSON array)
                keywords = analysis.get("keywords", [])
                if any(topic_lower in str(k).lower() for k in keywords):
                    matching_analyses.append(analysis)
                    continue
                
                # Check in summary
                summary = analysis.get("summary", "")
                if topic_lower in summary.lower():
                    matching_analyses.append(analysis)
                    continue
                
                # Check in original text
                original_text = analysis.get("original_text", "")
                if topic_lower in original_text.lower():
                    matching_analyses.append(analysis)
                    continue
            
            return matching_analyses
            
        except Exception as e:
            raise Exception(f"Failed to search analyses: {str(e)}")
    
    def delete_analysis(self, analysis_id: int) -> bool:
        """Delete an analysis by ID"""
        try:
            result = self.supabase.table("analyses").delete().eq("id", analysis_id).execute()
            return len(result.data) > 0
        except Exception as e:
            raise Exception(f"Failed to delete analysis: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if Supabase service is available"""
        try:
            # Test query
            self.supabase.table("analyses").select("id").limit(1).execute()
            return True
        except:
            return False

supabase_service = None

def get_supabase_service() -> SupabaseService:
    """Get or create Supabase service instance"""
    global supabase_service
    if supabase_service is None:
        supabase_service = SupabaseService()
    return supabase_service
