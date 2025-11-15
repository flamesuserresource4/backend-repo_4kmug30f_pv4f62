import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Expense, Category, Budget

app = FastAPI(title="Smart Expense Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Utilities
class ObjectIdStr(BaseModel):
    id: str


def to_serializable(doc):
    if not doc:
        return doc
    d = dict(doc)
    if "_id" in d:
        d["id"] = str(d.pop("_id"))
    return d


@app.get("/")
def read_root():
    return {"message": "Smart Expense Tracker Backend Running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response


# -----------------------------
# Category Endpoints
# -----------------------------
@app.post("/api/categories", response_model=dict)
def create_category(category: Category):
    try:
        inserted_id = create_document("category", category)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/categories", response_model=List[dict])
def list_categories():
    try:
        docs = get_documents("category")
        return [to_serializable(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# Expense Endpoints
# -----------------------------
@app.post("/api/expenses", response_model=dict)
def create_expense(expense: Expense):
    try:
        inserted_id = create_document("expense", expense)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/expenses", response_model=List[dict])
def list_expenses(category: Optional[str] = None, limit: int = 50):
    try:
        filter_dict = {"category": category} if category else {}
        docs = get_documents("expense", filter_dict=filter_dict, limit=limit)
        return [to_serializable(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# Budget Endpoints
# -----------------------------
@app.post("/api/budgets", response_model=dict)
def create_budget(budget: Budget):
    try:
        inserted_id = create_document("budget", budget)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/budgets", response_model=List[dict])
def list_budgets():
    try:
        docs = get_documents("budget")
        return [to_serializable(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
