BEGIN TRANSACTION;

/*
select Race info  ans SeriesId for all races that are in Completed Satges in Active Series */
 

 SELECT R.*, S.SeriesId 
 FROM Race as R JOIN Stage AS S
 WHERE R.StageId = S.Id 
 AND S.EndDate <= datetime('now')
 AND S.SeriesId IN (SELECT Id 
	    FROM Series 
	    WHERE StartDate <= datetime('now') 
	    AND EndDate > datetime('now')
	    );
 
 /* Run a check to ensure only 1 Series Active - if more flag data error... */
 
 
/* Select the list of Riders who are Participants in the Series */
 
SELECT R.* 
FROM Rider AS R
JOIN Participant AS P
WHERE R.Id = P.RiderId
AND P.SeriesId = 1;   -- use a Python variable for the Series

 /* 
   For each Stage in the LIST
   {
     Create a list of all Races for the Stage
	 Create list of all Riders who are Participants in the Series
	 For each rider
	 {
	   For each EventId in the list of Races
	   {
	      *** Call the API to see if the Rider participated in the Race (Event) if so return the result ***
	      Select the results from RaceResult where UserId = UserId of Rider and EventId - EventId of Race
		  
		  Insert into StageResult all info, 
		     BUT only where the the FinishTime is less than the FinishTime of any existing entry for this Rider for this Stage.
		  
	   }
	 }
   }




Build StageResult table in multiple passes

BEGIN TRANSACTION

*** Pass 1 ***

For all StageId + RiderId combos that do not exist in the StageResult table

INSERT INTO StageResult
   StageId + RiderId (this is a Unique key) 
   FinishTime
   RaceId
   LastCalc

*** Pass 2 ***
   
For all StageId + RiderId combos that already exist in teh StageResult table 

UPDATE StageResult
SET FinishTime = new FinishTime only if new FinishTime < existing FinishTime
plus update RaceId and LastCalc time

*** Pass 3 ***

Read through StageResult table and recalculate Postion and Points only for Stages being worked on

For all StageId's in Stage list
  *** Do we have a points look up? ***



*/


COMMIT;