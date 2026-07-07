DROP TABLE IF EXISTS Series;

CREATE TABLE Series (	
  Id	INTEGER PRIMARY KEY,
  Name	TEXT,
  StartDate	TEXT,
  EndDate	TEXT,
  CountingStages	INTEGER,  -- number of Stages that count towards GC
  UNIQUE (StartDate,EndDate)
  );

DROP TABLE IF EXISTS Stage;
  
 CREATE TABLE Stage (	
  Id	INTEGER PRIMARY KEY,
  SeriesId INTEGER, -- FK to Series table
  Name	TEXT,
  RouteId TEXT, -- FK to ROUVY Route infomation accessed via API
  RouteName TEXT, -- pulled from ROUVY API
  StartDate	TEXT,
  EndDate	TEXT,
  UNIQUE (StartDate,EndDate)
  );
 
 DROP TABLE IF EXISTS Race;

 CREATE TABLE Race (	
  Id	INTEGER PRIMARY KEY,
  StageId INTEGER, -- FK to Stage table
  EventId	TEXT UNIQUE, -- FK to ROUVY Event infomation accessed via API
  StartTime	TEXT, -- Date & Time for Race start
  Name TEXT,
  Country TEXT,
  Distance REAL,
  Ascent REAL,
  MaxSlope REAL
  );

DROP TABLE IF EXISTS GC;

 CREATE TABLE GC (	
  Id	INTEGER PRIMARY KEY,
  SeriesId INTEGER, -- FK to Series table
  RiderId	INTEGER, -- FK to Rider table
  Position INTEGER, -- current Position in GC  for Rider
  Points INTEGER, -- current Points in GC for Rider
  CountingStages INTEGER, -- num of Stages Counting to GC for Rider
  LastCalc TEXT, -- date & time that the GC record was last calculated
  UNIQUE (SeriesId,RiderId)
  ); 
 
 DROP TABLE IF EXISTS StageResult;
 
 CREATE TABLE StageResult (	
  Id	INTEGER PRIMARY KEY,
  StageId INTEGER, -- FK to Stage table
  RiderId	INTEGER, -- FK to Rider table
  FinishTime FLOAT, -- Race Time in seconds for fastest race Rider rode for Stage
  Position INTEGER, -- Rider's Position in Stage
  Points INTEGER, -- Rider's Points in Stage
  RaceId INTEGER, -- FK to Race table where Rider acheived FinishTime
  LastCalc TEXT, -- date & time that the StageResult record was last calculated
  UNIQUE (StageId, RiderId)
  ); 

DROP TABLE IF EXISTS Rider;

 CREATE TABLE Rider (	
  Id	INTEGER PRIMARY KEY,
  UserId TEXT UNIQUE, -- FK to ROUVY User accessible via API
  UserName	TEXT UNIQUE, -- Rouvy Username pulled via API
  AgeGroupId INTEGER, -- FK to AgeGroup lookup table
  Gender TEXT, 
  Nationality TEXT, 
  Weight REAL, -- in kgs
  FTP INTEGER
  );

DROP TABLE IF EXISTS Participant;

 CREATE TABLE Participant (	
  -- rowid (implicit system row-count)
  SeriesId INTEGER, -- FK to Series table
  RiderId	INTEGER, -- FK to Rider table
  UNIQUE (SeriesId, RiderId)
  );

/* Lookup tables 
   - table creation followed by population statements*/

DROP TABLE IF EXISTS AgeGroup;

 CREATE TABLE AgeGroup (	
  Id	INTEGER PRIMARY KEY,
  Label TEXT -- e.g "0-18", "19-34" etc.
  );

INSERT INTO AgeGroup (Label)
VALUES 
   ('0-18'),
   ('19-34'),
   ('35-39'),
   ('40-44'),
   ('45-49'),
   ('50-54'),
   ('55-59'),
   ('60-64'),
   ('65-69'),
   ('70-74'),
   ('75-79'),
   ('80-84'),
   ('85-89'),
   ('90+');
		
DROP TABLE IF EXISTS StagePoints;

 CREATE TABLE StagePoints (	
  Position	INTEGER PRIMARY KEY,  -- 1 to x
  Points Integer -- 200, 185, 170, 160, 150, 145, 140... 10, 9, 8, 7, 6, 5, 5, 5, 5 etc.
  );

INSERT INTO StagePoints (Points)
VALUES 
   (200),
   (190),
   (180),
   (170),
   (165),
   (160),
   (155),
   (150),
   (145),
   (140),
   (135),
   (130),
   (125),
   (120),
   (115),
   (110),
   (105),
   (100),
   (95),
   (90),
   (85),
   (80),
   (75),
   (70),
   (65),
   (60),
   (55),
   (50),
   (45),
   (40),
   (35),
   (30),
   (25),
   (20),
   (19),
   (18),
   (17),
   (16),
   (15),
   (14),
   (13),
   (12),
   (11),
   (10),
   (9),
   (8),
   (7),
   (6),
   (5),   
   (5);		

   





  
  
  
