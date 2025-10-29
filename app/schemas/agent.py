from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    query: str

class SourceDocument(BaseModel):
    content: str
    metadata: Dict[str, Any]  

class ChatResponse(BaseModel):
    answer: str
    source_documents: Optional[List[SourceDocument]] = None