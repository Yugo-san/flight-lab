from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import text
from backend.database import SessionLocal
from ml.inference import score_flight

app = FastAPI(title="AI Flight Matcher")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class SearchReq(BaseModel):
    budget: float; days: int; interests: list[str]; departure: str

@app.post("/api/search")
def search(req: SearchReq):
    db = SessionLocal()
    rows = db.execute(text("SELECT * FROM flights")).fetchall()
    db.close()
    best_flight, best_score = None, -1
    for r in rows:
        sc = score_flight(req.dict(), r)
        if sc > best_score: best_score, best_flight = sc, {"airline":r[1], "price":r[2], "duration":r[3], "stops":r[4], "destination":r[5]}
    return {"status":"ok", "best_flight": best_flight, "score": round(best_score, 3)}