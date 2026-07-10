import os
from typing import List, Dict, Any, Optional
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# Define path for local FAISS storage
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTOR_DB_DIR = os.path.join(BASE_DIR, "vectorstore")
INDEX_PATH = os.path.join(VECTOR_DB_DIR, "faiss_index")

_embeddings = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return _embeddings

def add_paper_chunks(chunks: List[Dict[str, Any]], paper_id: int):
    """
    Given a list of chunks, adds them to the FAISS index and saves to disk.
    Each chunk contains 'content', 'page', and 'source'.
    """
    embeddings = get_embeddings()
    documents = []
    
    for chunk in chunks:
        doc = Document(
            page_content=chunk["content"],
            metadata={
                "paper_id": paper_id,
                "page": chunk["page"],
                "source": chunk["source"]
            }
        )
        documents.append(doc)

    if not documents:
        return

    # Check if index files exist on disk
    index_file = os.path.join(INDEX_PATH, "index.faiss")
    if os.path.exists(INDEX_PATH) and os.path.exists(index_file):
        db = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
        db.add_documents(documents)
    else:
        db = FAISS.from_documents(documents, embeddings)

    os.makedirs(VECTOR_DB_DIR, exist_ok=True)
    db.save_local(INDEX_PATH)

def search_chunks(query: str, paper_ids: Optional[List[int]] = None, k: int = 5) -> List[Document]:
    """
    Searches the FAISS index for relevant chunks.
    Filters by paper_ids if specified.
    """
    index_file = os.path.join(INDEX_PATH, "index.faiss")
    if not os.path.exists(INDEX_PATH) or not os.path.exists(index_file):
        return []

    embeddings = get_embeddings()
    db = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

    if paper_ids:
        # Use lambda filter for multiple paper IDs
        filter_func = lambda metadata: metadata.get("paper_id") in paper_ids
        return db.similarity_search(query, k=k, filter=filter_func)
    else:
        return db.similarity_search(query, k=k)
