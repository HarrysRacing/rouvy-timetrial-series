DELETE FROM Series;

INSERT INTO Series (	
  Name,
  StartDate, -- 'YYYY-MM-DD HH:MM:SS'
  EndDate, -- 'YYYY-MM-DD HH:MM:SS'
  CountingStages -- number of Stages that count towards GC
  )
VALUES
  ('Harrys Dummy Race Series','2026-05-01 00:00:01','2026-08-03 23:59:59',2);

DELETE FROM Stage;
  
INSERT INTO Stage (	
  SeriesId, -- FK to Series table
  Name,
  RouteId, -- FK to ROUVY Route infomation accessed via API
  RouteName, -- pulled from ROUVY API
  StartDate,
  EndDate
  )
VALUES
  (1,'HR Stage 1 Dummy','81141','Bormio to Tirano | Italy','2026-05-01 00:00:01','2026-05-31 11:00:00'),
  (1,'HR Stage 2 Dummy','297637','Santo Stefano to Sant Ambrogio | Sicily','2026-06-01 00:00:01','2026-06-30 23:59:59'),
  (1,'HR Stage 3 Dummy','252521','Los Gigantes | Tenerife','2026-07-01 00:00:01','2026-07-04 20:00:59'),
  (1,'HR Stage 4 Dummy','252145','Pampas | Bolivia','2026-08-01 00:00:01','2026-08-31 23:59:59');
 
 DELETE FROM Race;

INSERT INTO Race (	
  StageId, -- FK to Stage table
  EventId, -- FK to ROUVY Event infomation accessed via API
  StartTime, -- Date & Time for Race start
  Name,
  Country,
  Distance,
  Ascent,
  MaxSlope
  )
VALUES
  (1,'bfff5371-dd90-4d64-b39f-7eb6bf0709b4','2026-05-10 19:00:00','Stage 1 Race 1','Italy',16.0,364.7,15.2),
  (1,'bfff5371-dd90-4d64-b39f-7eb6bf0709b5','2026-05-15 06:00:00','Stage 1 Race 2','Italy',16.0,364.7,15.2),
  (1,'bfff5371-dd90-4d64-b39f-7eb6bf0709b6','2026-05-20 11:00:00','Stage 1 Race 3','Italy',16.0,364.7,15.2),
  (2,'cfff5371-dd90-4d64-b39f-7eb6bf0709b4','2026-06-10 05:00:00','Stage 2 Race 1','Sicily',17.1,264.7,7.1),
  (2,'cfff5371-dd90-4d64-b39f-7eb6bf0709b5','2026-06-15 15:30:00','Stage 2 Race 2','Sicily',17.1,264.7,7.1),
  (2,'cfff5371-dd90-4d64-b39f-7eb6bf0709b6','2026-06-20 21:00:00','Stage 2 Race 3','Sicily',17.1,264.7,7.1),
  (2,'cfff5371-dd90-4d64-b39f-7eb6bf0709b7','2026-06-25 12:00:00','Stage 2 Race 4','Sicily',17.1,264.7,7.1),
  (3,'dfff5371-dd90-4d64-b39f-7eb6bf0709b4','2026-07-01 19:00:00','Stage 3 Race 1','Spain',14.9,64.3,2.2),
  (3,'dfff5371-dd90-4d64-b39f-7eb6bf0709b5','2026-07-03 06:00:00','Stage 3 Race 2','Spain',14.9,64.3,2.2),
  (3,'dfff5371-dd90-4d64-b39f-7eb6bf0709b6','2026-07-04 11:00:00','Stage 3 Race 3','Spain',14.9,64.3,2.2),
  (4,'efff5371-dd90-4d64-b39f-7eb6bf0709b4','2026-08-10 05:00:00','Stage 4 Race 1','Bolivia',22.5,564.7,9.1),
  (4,'efff5371-dd90-4d64-b39f-7eb6bf0709b5','2026-08-15 15:30:00','Stage 4 Race 2','Bolivia',22.5,564.7,9.1),
  (4,'efff5371-dd90-4d64-b39f-7eb6bf0709b6','2026-08-20 21:00:00','Stage 4 Race 3','Bolivia',22.5,564.7,9.1),
  (4,'efff5371-dd90-4d64-b39f-7eb6bf0709b7','2026-08-25 12:00:00','Stage 4 Race 4','Bolivia',22.5,564.7,9.1);


DELETE FROM Rider;

INSERT INTO Rider (	
  UserId, -- FK to ROUVY User accessible via API
  UserName, -- Rouvy Username pulled via API
  AgeGroupId, -- FK to AgeGroup lookup table
  Gender, 
  Nationality, 
  Weight, -- in kgs
  FTP
  )
VALUES 
  ('616e77e23b291ca7ebb5c989','Old-Harry',8,'male','CA',59.42055199999999,212),
  ('616e77e23b291ca7ebb5c990','Rider 2',5,'male','FR',47.6750,186),
  ('616e77e23b291ca7ebb5c991','Rider 3',2,'female','CH',77.7,286),
  ('616e77e23b291ca7ebb5c992','Rider 4',4,'female','BE',97.4,386),
  ('616e77e23b291ca7ebb5c993','Rider 5',1,'male','AU',67.89,206),
  ('616e77e23b291ca7ebb5c994','Rider 6',5,'male','CA',81.45,265),
  ('616e77e23b291ca7ebb5c995','Rider 7',7,'female','ES',64.78,236),
  ('616e77e23b291ca7ebb5c996','Rider 8',7,'male','FR',75.78,246),
  ('616e77e23b291ca7ebb5c997','Rider 9',8,'male','NZ',81.0,226),
  ('616e77e23b291ca7ebb5c998','Rider 10',4,'male','BE',71.23,196),
  ('616e77e23b291ca7ebb5c999','Rider 11',6,'male','CH',69.18,252);

DELETE FROM Participant;

INSERT INTO Participant (	
  SeriesId, -- FK to Series table
  RiderId -- FK to Rider table
  )
VALUES
  (1,1),
  (1,2),
  (1,3),
  (1,4),
  (1,5),
  (1,6),
  (1,7),
  (1,8),
  (1,9),
  (1,10),
  (1,11);



/* For dev and testing of the GC and StageResults tables calc, 
   need to dummy a Race Results set that would normally be pulled from the ROUVY API */

DROP TABLE IF EXISTS RaceResult;

 CREATE TABLE RaceResult (	
  -- rowid - implicit system row count
  EventId TEXT,
  UserId TEXT,
  FinishTime REAL, -- seconds
  AvgPower INTEGER, -- watts
  AvgSpeed REAL -- m/s
  ); 

DELETE FROM RaceResult;

INSERT INTO RaceResult (
  EventId,
  UserId,
  FinishTime, -- seconds
  AvgPower, -- watts
  AvgSpeed -- m/s
  )
VALUES 
  ('bfff5371-dd90-4d64-b39f-7eb6bf0709b4','616e77e23b291ca7ebb5c989',1360,221,7.5),  
  ('bfff5371-dd90-4d64-b39f-7eb6bf0709b6','616e77e23b291ca7ebb5c989',1345,223,7.6), 
  ('cfff5371-dd90-4d64-b39f-7eb6bf0709b4','616e77e23b291ca7ebb5c989',1460,190,6.5),
  ('cfff5371-dd90-4d64-b39f-7eb6bf0709b7','616e77e23b291ca7ebb5c989',1455,192,6.7),
  ('cfff5371-dd90-4d64-b39f-7eb6bf0709b6','616e77e23b291ca7ebb5c989',1500,185,6.0), 
  ('dfff5371-dd90-4d64-b39f-7eb6bf0709b4','616e77e23b291ca7ebb5c989',1660,190,6.5),
  ('dfff5371-dd90-4d64-b39f-7eb6bf0709b5','616e77e23b291ca7ebb5c989',1655,192,6.7),
  ('dfff5371-dd90-4d64-b39f-7eb6bf0709b6','616e77e23b291ca7ebb5c989',1600,185,6.0),

  
  ('bfff5371-dd90-4d64-b39f-7eb6bf0709b4','616e77e23b291ca7ebb5c990',1560,218,6.5), 
  ('cfff5371-dd90-4d64-b39f-7eb6bf0709b4','616e77e23b291ca7ebb5c990',1400,240,7.0), 
  ('dfff5371-dd90-4d64-b39f-7eb6bf0709b4','616e77e23b291ca7ebb5c990',1800,240,7.0),  
  ('dfff5371-dd90-4d64-b39f-7eb6bf0709b5','616e77e23b291ca7ebb5c990',1850,240,7.0),
  
  ('bfff5371-dd90-4d64-b39f-7eb6bf0709b5','616e77e23b291ca7ebb5c991',1745,186,5.5),   
  ('cfff5371-dd90-4d64-b39f-7eb6bf0709b5','616e77e23b291ca7ebb5c991',1745,186,5.5),  
  ('cfff5371-dd90-4d64-b39f-7eb6bf0709b7','616e77e23b291ca7ebb5c991',1745,186,5.5),

  ('bfff5371-dd90-4d64-b39f-7eb6bf0709b5','616e77e23b291ca7ebb5c992',1545,186,5.5),   
  ('bfff5371-dd90-4d64-b39f-7eb6bf0709b6','616e77e23b291ca7ebb5c992',1540,186,5.5),  

  ('bfff5371-dd90-4d64-b39f-7eb6bf0709b4','616e77e23b291ca7ebb5c993',1260,221,7.5),  
  ('bfff5371-dd90-4d64-b39f-7eb6bf0709b6','616e77e23b291ca7ebb5c993',1245,223,7.6), 
  ('cfff5371-dd90-4d64-b39f-7eb6bf0709b4','616e77e23b291ca7ebb5c993',1450,190,6.5),
  ('cfff5371-dd90-4d64-b39f-7eb6bf0709b7','616e77e23b291ca7ebb5c993',1543,192,6.7),
  ('cfff5371-dd90-4d64-b39f-7eb6bf0709b6','616e77e23b291ca7ebb5c993',1657,185,6.0), 
  ('dfff5371-dd90-4d64-b39f-7eb6bf0709b4','616e77e23b291ca7ebb5c993',1655,190,6.5),
  ('dfff5371-dd90-4d64-b39f-7eb6bf0709b5','616e77e23b291ca7ebb5c993',1650,192,6.7),
  ('dfff5371-dd90-4d64-b39f-7eb6bf0709b6','616e77e23b291ca7ebb5c993',1599,185,6.0); 
  
