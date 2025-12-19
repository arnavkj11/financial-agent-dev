from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.schemas.transaction import ExtractedFinancialData
from app.core.config import settings

def clean_data_with_llm(raw_text: str) -> ExtractedFinancialData:
    """
    Uses OpenAI to parse raw text into structured JSON.
    """
    if not settings.OPENAI_API_KEY:
        print("WARNING: No OpenAI API Key found. Returning empty data.")
        return ExtractedFinancialData(transactions=[], summary="No API Key")

    llm = ChatOpenAI(model="gpt-4o", api_key=settings.OPENAI_API_KEY)
    
    # We use the 'with_structured_output' method which is the modern (LangChain 0.1+) way
    # to guarantee JSON output matching our Pydantic schema.
    structured_llm = llm.with_structured_output(ExtractedFinancialData)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a specialized Data Extraction Assistant. "
                   "Extract financial transactions from the following raw text. "
                   "Standardize dates to YYYY-MM-DD. "
                   "IMPORTANT: Infer the category for each transaction based on the merchant name "
                   "(e.g., 'Groceries', 'Dining', 'Utilities', 'Entertainment', 'Shopping', 'Gas', 'Insurance', 'Health', 'Education', 'Subscription', 'Travel', 'Other'). "
                   "Do not leave category as null."),
        ("user", "Raw Text:\n{raw_text}")
    ])

    chain = prompt | structured_llm
    
    try:
        return chain.invoke({"raw_text": raw_text})
    except Exception as e:
        print(f"Error during LLM extraction: {e}")
        return ExtractedFinancialData(transactions=[], summary="Extraction Failed")
