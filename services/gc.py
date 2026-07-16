from pathlib import Path
import sqlite3

def get_topten_gcinfo(series_id):
    db_path = Path(__file__).resolve().parent.parent / "database" / "harrysracing.db"
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    query = ('SELECT G.Position, R.UserName, R.Gender, N.Nationality, A.Label, G.CountingStages, G.Points '
             'FROM GC AS G, Rider AS R, AgeGroup AS A, Nationality AS N '
             'WHERE G.SeriesId = ? '
             'AND R.ID = G.RiderId '
             'AND A.ID = R.AgeGroupId '
             'AND R.Nationality = N.CountryCode '
             'AND G.Position <= 10 '
             'ORDER BY G.Position, G.Points ASC;'             
            ) 
            
    cur.execute(query,(series_id,))
    results = cur.fetchall()
    con.close()
    
    return results
    
def get_full_gcinfo(series_id):
    db_path = Path(__file__).resolve().parent.parent / "database" / "harrysracing.db"
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    query = ('SELECT G.Position, R.UserName, R.Gender, N.Nationality, A.Label, G.CountingStages, G.Points '
             'FROM GC AS G, Rider AS R, AgeGroup AS A, Nationality AS N '
             'WHERE G.SeriesId = ? '
             'AND R.ID = G.RiderId '
             'AND A.ID = R.AgeGroupId '
             'AND R.Nationality = N.CountryCode '
             'ORDER BY G.Position, G.Points ASC;'             
            ) 
            
    cur.execute(query,(series_id,))
    results = cur.fetchall()
    con.close()
    
    return results