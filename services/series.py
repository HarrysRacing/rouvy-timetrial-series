from pathlib import Path
import sqlite3

def get_active_series():
    db_path = Path(__file__).resolve().parent.parent / "database" / "harrysracing.db"
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    query = 'SELECT Id, Name, date(StartDate), date(EndDate), CountingStages FROM Series WHERE StartDate <= datetime("now") AND EndDate > datetime("now");'
    cur.execute(query)
    results = cur.fetchall()
    con.close()
    return results
    