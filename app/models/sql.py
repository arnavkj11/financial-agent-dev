from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    
    documents = relationship("Document", back_populates="user")

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending") # pending, processed, failed
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="documents")
    transactions = relationship("Transaction", back_populates="document")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    
    date = Column(Date)
    merchant = Column(String)
    amount = Column(Float)
    currency = Column(String, default="USD")
    category = Column(String) # Inferred by LLM
    description_embedding_id = Column(String, nullable=True) # Link to VectorDB
    
    document = relationship("Document", back_populates="transactions")
