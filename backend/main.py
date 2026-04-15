from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import text
from backend.database import SessionLocal
import os

app = FastAPI(title="AI Flight Matcher")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class SearchReq(BaseModel):
    budget: float
    days: int
    interests: list[str]
    departure: str

@app.get("/")
def root():
    return {"status": "API работает", "version": "1.1"}

@app.get("/debug/db")
def debug_db():
    """Проверка базы данных"""
    try:
        db = SessionLocal()
        rows = db.execute(text("SELECT * FROM flights")).fetchall()
        db.close()
        
        flights_list = []
        for r in rows:
            flights_list.append({
                "id": r[0],
                "airline": r[1],
                "price": r[2],
                "duration": r[3],
                "stops": r[4],
                "destination": r[5]
            })
        
        return {
            "total_flights": len(rows),
            "flights": flights_list[:10]  # первые 10 рейсов
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/search")
def search(req: SearchReq):
    print(f"\n{'='*50}")
    print(f"📩 ЗАПРОС: бюджет={req.budget}, дней={req.days}, интересы={req.interests}")
    print(f"{'='*50}")
    
    try:
        # Загружаем все рейсы из БД
        db = SessionLocal()
        rows = db.execute(text("SELECT * FROM flights")).fetchall()
        db.close()
        
        print(f"✅ Загружено рейсов из БД: {len(rows)}")
        
        if len(rows) == 0:
            return {"error": "База данных ПУСТАЯ!", "status": "error"}
        
        # Показываем первые 5 рейсов для отладки
        print("\n📋 Первые 5 рейсов в БД:")
        for i, r in enumerate(rows[:5]):
            print(f"  {i+1}. {r[1]} → {r[5]}, {r[2]}₽, {r[3]}ч, пересадок: {r[4]}")
        
        # Фильтрация по бюджету
        affordable = [r for r in rows if r[2] <= req.budget]
        
        if len(affordable) == 0:
            print(f"\n⚠️  Нет рейсов в бюджете {req.budget}₽! Берем самый дешевый.")
            affordable = [min(rows, key=lambda x: x[2])]
        else:
            print(f"\n💰 Рейсов в бюджете до {req.budget}₽: {len(affordable)}")
        
        # Ранжирование с помощью ИИ
        print("\n🧮 Оценка рейсов нейросетью:")
        scored_flights = []
        
        for r in affordable:
            try:
                from ml.inference import score_flight
                sc = score_flight(req.dict(), r)
            except Exception as e:
                print(f"  ⚠️  Ошибка в score_flight: {e}")
                # Упрощенная оценка если модель не работает
                sc = (1 - r[2]/100000) * 0.5 + (1 - r[3]/15) * 0.3 + (1 - r[4]/3) * 0.2
            
            scored_flights.append((sc, r))
            print(f"  {r[1]} → {r[5]}: {r[2]}₽, score={sc:.3f}")
        
        # Сортировка по убыванию score
        scored_flights.sort(key=lambda x: x[0], reverse=True)
        
        print(f"\n🏆 ТОП-3 рейса:")
        for i, (sc, r) in enumerate(scored_flights[:3]):
            print(f"  {i+1}. {r[1]} → {r[5]}, {r[2]}₽, score={sc:.3f}")
        
        # Лучший рейс
        best_score, best_row = scored_flights[0]
        
        best_flight = {
            "airline": best_row[1],
            "price": best_row[2],
            "duration": best_row[3],
            "stops": best_row[4],
            "destination": best_row[5]
        }
        
        print(f"\n✅ ВОЗВРАЩАЕМ: {best_flight['airline']} → {best_flight['destination']}, {best_flight['price']}₽")
        print(f"{'='*50}\n")
        
        return {
            "status": "ok",
            "best_flight": best_flight,
            "score": round(best_score, 3),
            "debug": {
                "total_flights": len(rows),
                "affordable_flights": len(affordable),
                "top_3": [
                    {"airline": r[1], "destination": r[5], "price": r[2], "score": round(sc, 3)}
                    for sc, r in scored_flights[:3]
                ]
            }
        }
        
    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e), "status": "error"}