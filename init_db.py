import sqlite3, random, os
os.makedirs("backend", exist_ok=True)
conn = sqlite3.connect("backend/flights.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS flights (id INTEGER PRIMARY KEY, airline TEXT, price INTEGER, duration REAL, stops INTEGER, destination TEXT)")
airlines = ["Aeroflot", "S7", "Pobeda", "Turkish", "Emirates"]
dests = ["Сочи", "Казань", "Тбилиси", "Дубай", "Пхукет", "Минск"]
for _ in range(50):
    c.execute("INSERT INTO flights VALUES (NULL,?,?,?,?,?)", (
        random.choice(airlines), random.randint(5000, 85000),
        round(random.uniform(1.5, 14.0), 1), random.choice([0,0,1,2]), random.choice(dests)
    ))
conn.commit(); conn.close()
print(" БД создана: backend/flights.db")