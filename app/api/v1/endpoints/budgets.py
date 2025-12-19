from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List

from app.api.deps import get_current_user
from app.core.database import SessionLocal
from app.models.sql import User, Budget, Transaction, Document
from app.schemas.budget import BudgetCreate, BudgetOut, BudgetStatus

router = APIRouter()

@router.post("/", response_model=BudgetOut)
async def create_or_update_budget(
    budget_in: BudgetCreate,
    current_user: User = Depends(get_current_user)
):
    async with SessionLocal() as session:
        # Check if budget exists for this category
        result = await session.execute(
            select(Budget).where(
                Budget.user_id == current_user.id,
                Budget.category == budget_in.category
            )
        )
        existing_budget = result.scalars().first()
        
        if existing_budget:
            existing_budget.amount = budget_in.amount
            await session.commit()
            await session.refresh(existing_budget)
            return existing_budget
        else:
            new_budget = Budget(
                user_id=current_user.id,
                category=budget_in.category,
                amount=budget_in.amount
            )
            session.add(new_budget)
            await session.commit()
            await session.refresh(new_budget)
            return new_budget

@router.get("/", response_model=List[BudgetOut])
async def read_budgets(
    current_user: User = Depends(get_current_user)
):
    async with SessionLocal() as session:
        result = await session.execute(
            select(Budget).where(Budget.user_id == current_user.id)
        )
        return result.scalars().all()

@router.get("/status", response_model=List[BudgetStatus])
async def get_budget_status(
    current_user: User = Depends(get_current_user)
):
    """
    Compares set budgets vs actual spending (Global/All-time for now).
    """
    async with SessionLocal() as session:
        # 1. Get all budgets
        budget_result = await session.execute(
            select(Budget).where(Budget.user_id == current_user.id)
        )
        budgets = budget_result.scalars().all()
        
        status_list = []
        
        for budget in budgets:
            # 2. Sum transactions for this category (User specific)
            # Join Transaction -> Document -> User
            stmt = select(func.sum(Transaction.amount)).join(Document).where(
                Document.user_id == current_user.id,
                Transaction.category == budget.category
            )
            spent_result = await session.execute(stmt)
            spent = spent_result.scalar() or 0.0
            
            remaining = budget.amount - spent
            percent_used = (spent / budget.amount) * 100 if budget.amount > 0 else 0.0
            
            status_list.append(BudgetStatus(
                category=budget.category,
                limit=budget.amount,
                spent=spent,
                remaining=remaining,
                percent_used=round(percent_used, 1)
            ))
            
        return status_list
