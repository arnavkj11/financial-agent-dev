from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from app.api.deps import get_current_user
from app.models.sql import User
from app.core.database import SessionLocal
from app.schemas.dashboard import DashboardStats, TimeRange, CategoryStat, TrendPoint

router = APIRouter()

@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    time_range: TimeRange = Query(TimeRange.LAST_30D),
    categories: Optional[List[str]] = Query(None)
):
    """
    Get aggregated dashboard statistics with filters.
    """
    # 1. Calculate Start Date
    start_date = None
    today = datetime.now().date()
    
    if time_range == TimeRange.LAST_24H:
        start_date = today - timedelta(days=1)
    elif time_range == TimeRange.LAST_7D:
        start_date = today - timedelta(days=7)
    elif time_range == TimeRange.LAST_30D:
        start_date = today - timedelta(days=30)
    elif time_range == TimeRange.LAST_3M:
        start_date = today - timedelta(days=90)
    elif time_range == TimeRange.LAST_6M:
        start_date = today - timedelta(days=180)
    elif time_range == TimeRange.LAST_1Y:
        start_date = today - timedelta(days=365)
    # ALL_TIME -> start_date remains None

    # 2. Build Query Filters
    filters = ["user_id = :uid"]
    params = {"uid": current_user.id}

    if start_date:
        filters.append("date >= :start_date")
        params["start_date"] = start_date

    if categories:
        # Handling list IN clause safely with SQLAlchemy text is tricky with bind params for lists in some drivers.
        # We will expand keys like :cat_0, :cat_1
        cat_clauses = []
        for i, cat in enumerate(categories):
            key = f"cat_{i}"
            cat_clauses.append(f":{key}")
            params[key] = cat
        if cat_clauses:
            filters.append(f"category IN ({','.join(cat_clauses)})")

    where_clause = " WHERE " + " AND ".join(filters)

    async with SessionLocal() as session:
        # --- A. Total Spent & Top Category ---
        # Note: We can reuse the result of Category Breakdown to avoid extra queries, 
        # but a direct sum is cleaner for the 'total' if categories filter excludes items.
        # Actually, total should respect filters.
        
        # --- B. Category Breakdown ---
        cat_query = f"""
        SELECT category, SUM(amount) as total
        FROM transactions
        {where_clause}
        GROUP BY category
        ORDER BY total DESC
        """
        cat_result = await session.execute(text(cat_query), params)
        cat_rows = cat_result.fetchall()

        total_spent = sum(row.total for row in cat_rows)
        top_category = cat_rows[0].category if cat_rows else None
        
        breakdown = []
        for row in cat_rows:
            pct = (row.total / total_spent * 100) if total_spent > 0 else 0
            breakdown.append(CategoryStat(
                category=row.category or "Uncategorized", 
                amount=row.total, 
                percentage=round(pct, 1)
            ))

        # --- C. Monthly/Daily Trend ---
        # If range is small (< 3m), group by Day. Else Month.
        is_long_range = time_range in [TimeRange.LAST_6M, TimeRange.LAST_1Y, TimeRange.ALL_TIME]
        
        if is_long_range:
            # Group by Month (YYYY-MM)
            date_col = "strftime('%Y-%m', date)" 
        else:
            # Group by Day (YYYY-MM-DD)
            date_col = "date"

        trend_query = f"""
        SELECT {date_col} as period, SUM(amount) as total
        FROM transactions
        {where_clause}
        GROUP BY period
        ORDER BY period ASC
        """
        trend_result = await session.execute(text(trend_query), params)
        trend_rows = trend_result.fetchall()
        
        trend = [TrendPoint(period=str(row.period), amount=row.total) for row in trend_rows]

    return DashboardStats(
        total_spent=total_spent,
        top_category=top_category,
        category_breakdown=breakdown,
        monthly_trend=trend
    )
