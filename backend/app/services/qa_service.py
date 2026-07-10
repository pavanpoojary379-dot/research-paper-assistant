import os
import google.generativeai as genai
from typing import List
from langchain_core.documents import Document

def generate_summary(query: str, chunks: List[Document]) -> str:
    """
    Formulates a prompt using retrieved document chunks and queries the Gemini LLM
    to generate a structured summary/answer.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        context_previews = []
        for doc in chunks:
            page = doc.metadata.get('page', '?')
            source = doc.metadata.get('source', 'Unknown')
            preview = doc.page_content[:200].replace('\n', ' ').strip()
            context_previews.append(f"- **{source} (Page {page})**: \"{preview}...\"")
        
        preview_text = "\n".join(context_previews)
        
        return (
            "⚠️ **Gemini API Key is not set!**\n\n"
            "To enable actual AI-generated summaries, please add your Google Gemini API key to the `backend/.env` file:\n"
            "```env\n"
            "GEMINI_API_KEY=your_actual_api_key\n"
            "```\n\n"
            "### Retrieved Chunks for your query:\n"
            f"{preview_text or 'No chunks retrieved for this query.'}"
        )

    try:
        genai.configure(api_key=api_key)
        # Use gemini-1.5-flash for fast and cost-effective responses
        model = genai.GenerativeModel('gemini-1.5-flash')

        context_blocks = []
        for idx, doc in enumerate(chunks):
            source = doc.metadata.get('source', 'Unknown')
            page = doc.metadata.get('page', '?')
            context_blocks.append(
                f"[Chunk {idx+1}] Source: {source}, Page: {page}\n"
                f"Content: {doc.page_content}"
            )
            
        context_str = "\n\n=========================================\n\n".join(context_blocks)

        prompt = (
            "You are a professional Research Assistant. Your task is to answer the query/summarize "
            "based *only* on the provided context retrieved from PDF research papers.\n\n"
            "Guidelines:\n"
            "1. Be objective, thorough, and highly structured.\n"
            "2. Whenever you state a fact or point, cite the chunk's source and page in brackets, "
            "e.g. [Attention_Is_All_You_Need.pdf, Page 4].\n"
            "3. Format your response in clean Markdown with headers, bullet points, or lists.\n"
            "4. If the provided context does not contain enough information to answer, explain what is missing.\n\n"
            f"Context Chunks:\n{context_str}\n\n"
            f"User Query: {query}\n\n"
            "Response:"
        )

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ **Error generating summary from Gemini API:** {str(e)}"
