from pydantic import BaseModel
from typing import List, Optional

class PaperBase(BaseModel):
    filename: str
    filepath: str

class PaperCreate(PaperBase):
    uploaded_by: int

class PaperResponse(BaseModel):
    id: int
    filename: str
    uploaded_by: int

    class Config:
        from_attributes = True

class QueryRequest(BaseModel):
    query: str
    paper_ids: Optional[List[int]] = None

class SourceDocument(BaseModel):
    page: int
    content: str
    score: Optional[float] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceDocument]
