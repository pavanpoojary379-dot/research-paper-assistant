from pypdf import PdfReader
from typing import List, Dict, Any
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter


def extract_and_chunk_pdf(
    filepath: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[Dict[str, Any]]:

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"PDF file not found: {filepath}")

    reader = PdfReader(filepath)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = []

    for page_no, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if not text:
            continue

        page_chunks = splitter.split_text(text)

        for chunk in page_chunks:
            chunks.append({
                "content": chunk,
                "page": page_no,
                "source": os.path.basename(filepath)
            })

    return chunks