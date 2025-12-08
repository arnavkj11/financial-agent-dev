import os
from pypdf import PdfReader

def extract_text(file_path: str) -> str:
    """
    Synchronously extracts text from a PDF file.
    NOTE: This is CPU bound. FastAPI runs normal 'def' functions in a threadpool,
    so it won't block the event loop.
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

async def process_document_task(file_path: str):
    """
    The Background Task. 
    1. Extract Text
    2. (TODO) Clean Data
    3. (TODO) Save to Vector DB
    """
    print(f"--- [Worker] Starting processing for: {file_path} ---")
    
    # 1. Extraction
    raw_text = extract_text(file_path)
    print(f"--- [Worker] Extracted {len(raw_text)} characters ---")
    
    # 2. Data Cleaning (LLM)
    from app.services.extraction import clean_data_with_llm
    structured_data = clean_data_with_llm(raw_text)
    
    print(f"--- [Worker] Found {len(structured_data.transactions)} transactions ---")
    for tx in structured_data.transactions:
        print(f"   - {tx.date} | {tx.merchant} | ${tx.amount} ({tx.category})")

    print(f"--- [Worker] Finished processing for: {file_path} ---")
