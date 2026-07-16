from pathlib import Path
import sqlite3

def get_stagesinfo():
    db_path = Path(__file__).resolve().parent.parent / "database" / "harrysracing.db"
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    query = ('SELECT Name, RouteName, date(StartDate), date(EndDate), Country, Distance, Ascent '
             'FROM Stage '
             'WHERE SeriesId IN (SELECT Id '
             '                    FROM Series '
             '                    WHERE StartDate <= datetime("now") '
             '                    AND EndDate > datetime("now") '
             '                    );' 
            ) 
    cur.execute(query)
    results = cur.fetchall()
    con.close()
    return results
    