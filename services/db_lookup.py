from pathlib import Path
import sqlite3

def get_pointslist():
    db_path = Path(__file__).resolve().parent.parent / "database" / "harrysracing.db"
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    query = 'SELECT Position, Points FROM StagePoints;'
    cur.execute(query)
    results = cur.fetchall()
    con.close()
    return results
    