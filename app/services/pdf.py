import os
from datetime import date, datetime
from pypdf import PdfReader
from sqlalchemy.future import select

from app.core.database import SessionLocal
from app.models.sql import Document, Transaction
from app.services.extraction import clean_data_with_llm

def extract_text(file_path: str) -> str:
    """
    Synchronously extracts text from a PDF file.
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

async def process_document_task(file_path: str, user_id: int):
    """
    Extraction + Persistence Worker.
    """
    filename = os.path.basename(file_path)
    print(f"--- [Worker] Starting processing for: {filename} ---")

    async with SessionLocal() as db:
        # 1. Create Document Record
        new_doc = Document(
            filename=filename,
            upload_date=datetime.now(),
            status="processing",
            user_id=user_id
        )
        db.add(new_doc)
        await db.commit()
        await db.refresh(new_doc)

        try:
            # 2. Extract Text
            raw_text = extract_text(file_path)
            
            # 3. Clean Data (LLM)
            structured_data = clean_data_with_llm(raw_text)
            
            # 4. Save Transactions & Prepare Vector Data
            print(f"--- [Worker] Saving {len(structured_data.transactions)} items to DB & Vector Store ---")
            
            from app.core.vector import get_transaction_collection
            collection = get_transaction_collection()

            ids = []
            documents = []
            metadatas = []

            for i, tx in enumerate(structured_data.transactions):
                # Unique ID for vector store
                vec_id = f"{new_doc.id}_{i}"
                
                # Robust date parsing
                try:
                    tx_date = datetime.strptime(tx.date, "%Y-%m-%d").date()
                except ValueError:
                    tx_date = date.today()

                # SQL Record
                db_tx = Transaction(
                    document_id=new_doc.id,
                    date=tx_date,
                    merchant=tx.merchant,
                    amount=tx.amount,
                    currency=tx.currency,
                    category=tx.category,
                    description_embedding_id=vec_id # Linked!
                )
                db.add(db_tx)
                
                # Vector Data
                ids.append(vec_id)
                # The "Text" we search against: "Starbucks (Food) on 2024-01-01"
                documents.append(f"{tx.merchant} ({tx.category}) on {tx.date}. Amount: {tx.amount} {tx.currency}")
                
                # Metadata for filtering
                metadatas.append({
                    "merchant": tx.merchant,
                    "category": tx.category or "Unknown",
                    "amount": tx.amount,
                    "date": tx.date, # String format YYYY-MM-DD
                    "doc_id": new_doc.id
                })

            # Batch Insert to Vector DB
            if ids:
                collection.add(ids=ids, documents=documents, metadatas=metadatas)

            new_doc.status = "completed"
            await db.commit()
            print(f"--- [Worker] Detailed Success: {filename} processed and indexed. ---")
            
        except Exception as e:
            print(f"!!! [Worker] Error processing {filename}: {e}")
            new_doc.status = "failed"
            await db.commit()
