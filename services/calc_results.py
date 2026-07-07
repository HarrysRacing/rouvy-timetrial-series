import sqlite3

from datetime import datetime, timezone

#now = datetime.now(timezone.utc)
#print('UTC Current Time', now)

# Calc the StageResult table

try:
    # Connect to SQLite Database and create a cursor
    dbConnection = sqlite3.connect(r'C:\Users\Harry\Documents\Updated Docs to Sync\Cycling\HarrysRacing\Database\harrysracing.db')
    cursor = dbConnection.cursor()
    print('Connected to harrysracing.db')

    # SELECT all Races and SeriesId for completed Stages for the (should only be one) active Series 
    query = ('SELECT S.SeriesId, R.* '
             'FROM Race as R JOIN Stage AS S '
             'WHERE R.StageId = S.Id '
             'AND S.EndDate <= datetime("now") '
             ' AND S.SeriesId IN (SELECT Id '
             '                    FROM Series '
             '                    WHERE StartDate <= datetime("now") '
             '                    AND EndDate > datetime("now") '
             '                    );' 
             )      
    
    cursor.execute(query)

    # Fetch and store the Race info for all completed Stages in the active Series
    RaceInfo = cursor.fetchall() 
    #print('Races/Series selected ',RaceInfo)
    #print('Number of rows is', len(RaceInfo))
 
 
    one_Series = False
    idx = 0

    if RaceInfo:
        first = RaceInfo[0][idx]
        one_Series = all(r[idx] == first for r in RaceInfo)
 
    # one_Series will be false if either no Races were selected or multiple active Series were found, otherwise one_Series is true
 
 
    if one_Series == False:  
       print('No Race Info or more than one active Series found... exiting')
    else:  
       
       series_Id = RaceInfo[0][idx]
       
       # SELECT the Riders who are Particpants in the Series 
       query = ('SELECT R.* '
                 ' FROM Rider AS R '
                 ' JOIN Participant AS P '
                 ' WHERE R.Id = P.RiderId '
                 ' AND P.SeriesId = ?;'
                )               
                 
       cursor.execute(query, (series_Id,))

       # Fetch and store the Race info for all completed Stages in the active Series
       RiderInfo = cursor.fetchall() 
       
       #print('Riders selected ',RiderInfo)
       print('Number of Riders found is', len(RiderInfo))       
       
        
       #For each Rider in RiderInfo loop through RaceInfo
       for rider in RiderInfo:

           rider_Id = rider[0]
           user_Id = rider[1]
           
           for race in RaceInfo:
               race_Id = race[1]
               stage_Id = race[2]
               event_Id = race[3]  

               #print('Processing Race : ',race_Id, 'for Rider : ',rider[2])               
           
               #Use the EventId to call the ROUVY API to retrieve the Event results

               #  *** Temporarily query the RaceResult table using EventId  ***
               query = ('SELECT RR.* '
                        ' FROM RaceResult AS RR '
                        ' WHERE RR.EventId = ? '
                        ' AND RR.UserId = ?;'
                       )               

               cursor.execute(query, (event_Id, user_Id))

               RaceResult = cursor.fetchone() #Only one RaceResult can exist for any EventId/UserId key
               
               #print('RaceResult : ',RaceResult)
               
               if RaceResult:  #there is a RaceResult for this Race for this Rider
                
                  query = ('SELECT FinishTime FROM StageResult '
                           'WHERE StageId = ? '
                           'AND RiderId = ?;'
                           )
                           
                  cursor.execute(query, (stage_Id, rider_Id))

                  StageResult = cursor.fetchone()
                  
                  if StageResult: 
                      if RaceResult[2] < StageResult[0]: #Check FinishTime's to know if StageResult table needs updating?
 
                        query = ('UPDATE StageResult '
                                 'SET FinishTime = ?, '
                                 'Position = 0, '
                                 'Points = 0, '
                                 'RaceId = ?, '
                                 'LastCalc = datetime("now") '
                                 'WHERE StageId = ? '
                                 'AND RiderId = ?;'
                                 )
                                 
                        cursor.execute(query, (RaceResult[2],race_Id,stage_Id,rider_Id))
                        
                        
                      #else do nothing as StageResult contains fastest FinishTime for this Rider in this Stage already  
                     
                  else:
                      
                      query = ('INSERT INTO StageResult(StageId, RiderId, FinishTime, Position, Points, RaceId, LastCalc) '
                               'VALUES(?,?,?,0,0,?,datetime("now"))'
                               )
                               
                      cursor.execute(query, (stage_Id,rider_Id,RaceResult[2],race_Id))    

                     
       # (re)Calculate Position and Points in StageResult table for all StageIds
        
       #for each Stage in StageResults for the active Series 
 
       stage_Ids = [] #create a list of all stageIds for current Series
       
       l = len(RaceInfo)
       for x in range(l):
          if RaceInfo[x][2] not in stage_Ids: 
             stage_Ids.append(RaceInfo[x][2]) 
       
       l = len(stage_Ids)
       for x in range(l):
          
          query = ('SELECT Id FROM StageResult WHERE StageId = ? ORDER BY FinishTime ASC ')

          cursor.execute(query,(stage_Ids[x],))

          stgRes_Ids = cursor.fetchall()
        
          ln = len(stgRes_Ids)
          for y in range(ln):
             if y >= 50:
                pts_Pos = 50  #50 rows in Points table, all positions after 50 get the same points as position 50.
             else:
                pts_Pos = y+1                 
             
             position = y+1
             
             query = ('UPDATE StageResult '
                         'SET Position = ?, '
                         'Points = sp.Points, '
                         'LastCalc = datetime("now") '
                         'FROM (SELECT * FROM StagePoints) AS sp '
                         'WHERE StageResult.Id = ? '
                         'AND sp.Position = ?;'
                        )
              
             cursor.execute(query, (pts_Pos, stgRes_Ids[y][0], position))                

       # (re)Calculate Position and Points in GC table for StageResult entries for Series
       # for the Series get the num of counting Stages
       query = ('SELECT CountingStages FROM SERIES WHERE Id = ?;')
       
       cursor.execute(query,(series_Id,))
       
       countingStages = cursor.fetchone()
       
       print('counting Stages :',countingStages[0],' series : ',series_Id)
       
       # for Riders in current Series with results in StageResult table
       # collect their points and for all counting stages ie: the ones with the higest points, add them up
       
       query = ('SELECT sr.StageId, sr.RiderId, sr.Points '
                'FROM StageResult AS sr, Stage AS s '
                'WHERE s.Id = sr.StageId '
                'AND s.SeriesId = ?;')
                
       cursor.execute(query,(series_Id,))
       
       gc_points = cursor.fetchall()
       
       #sort gc_points list in points order descending
       gc_points.sort(key=lambda x:x[2],reverse=True)
       
       print('gc_points :',gc_points)      
       
       # stage, rider, points - find the riders and for each rider 
       
       riders = []
       
       l = len(gc_points)
       
       # create list of riders with Stage Results
       for x in range(l):
          if gc_points[x][1] not in riders: 
              riders.append(gc_points[x][1]) 
       
       l = len(riders)
       
       for x in range(l):

           #calc points for each rider, only count points for counting Stages 
           
           stg_count = 0
           rider_stgs = 0
           pts = 0
           
           ln = len(gc_points)

           for y in range(ln):
               if gc_points[y][1] == x+1:
                  stg_count = stg_count+1
                  if stg_count <= countingStages[0]:
                     pts = pts + gc_points[y][2]
                     rider_stgs = rider_stgs+1
                  
           print('points for rider ',x+1,' = ',pts)
           # if there is a row in GC table for the Rider / Series then perform UPDATE otherwise need to INSERT
           query = ('SELECT Id FROM GC '
                    'WHERE RiderId = ? '
                    'AND SeriesId = ? '
                    'ORDER BY ROWID ASC LIMIT 1;'
                    )
                    
           cursor.execute(query,(x+1,series_Id))
           
           rider_found = cursor.fetchone()
                  
           if rider_found:  
              query = ('UPDATE GC '
                       'SET Points = ?, '
                       'Position = 0, '
                       'CountingStages = ?, '
                       'LastCalc = datetime("now") '
                       'WHERE SeriesId = ?'
                       'AND RiderId = ?;'                       
                       )                     
           
           else:
              query = ('INSERT INTO GC(Points, Position, CountingStages, LastCalc, SeriesId, RiderId) '
                       'VALUES(?,0,?,datetime("now"),?,?)'
                       )  

           cursor.execute(query,(pts,rider_stgs,series_Id,x+1))                       
 
        # then update the position column in the GC table, **if any riders have equal points in the active Series**

           query = ('WITH ranked_GC AS ( '
                    '                   SELECT Id, '
                    '                   SeriesId, '
                    '                   RANK() OVER (ORDER BY Points DESC) AS rnk '
                    '                   FROM GC '
                    '                   WHERE SeriesId = ? '
                    '                   ) '
                    'UPDATE GC '
                    'SET Position = ranked_GC.rnk '
                    'FROM ranked_GC '
                    'WHERE GC.Id = ranked_GC.Id;'
                    )
                 
           cursor.execute(query,(series_Id,))
        
    # Close the cursor after use
    cursor.close()


except sqlite3.Error as error:
    print('Error occurred -', error)

finally:
    # Ensure the database connection is closed
    if dbConnection:
        dbConnection.commit()
        dbConnection.close()
        
  
