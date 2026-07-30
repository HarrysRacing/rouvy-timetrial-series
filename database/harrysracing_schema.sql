DROP TABLE IF EXISTS Series;

CREATE TABLE Series (	
  Id	INTEGER PRIMARY KEY,
  Name	TEXT,
  StartDate	TEXT, -- ISO8601,'', 'YYYY-MM-DDTHH,'',MM,'',SSZ'
  EndDate	TEXT, -- ISO8601,'', 'YYYY-MM-DDTHH,'',MM,'',SSZ'
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
  Country TEXT,
  Distance REAL, -- in kms
  Ascent REAL, -- in metres
  MaxSlope REAL, -- percentage
  StartDate	TEXT, -- ISO8601,'', 'YYYY-MM-DDTHH,'',MM,'',SSZ'
  EndDate	TEXT, -- ISO8601,'', 'YYYY-MM-DDTHH,'',MM,'',SSZ'
  UNIQUE (StartDate,EndDate)
  );
 
 DROP TABLE IF EXISTS Race;

 CREATE TABLE Race (	
  Id	INTEGER PRIMARY KEY,
  StageId INTEGER, -- FK to Stage table
  EventId	TEXT UNIQUE, -- FK to ROUVY Event infomation accessed via API
  StartTime	TEXT, -- Date & Time for Race start -- ISO8601,'', 'YYYY-MM-DDTHH,'',MM,'',SSZ'
  Name TEXT
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
  Weight FLOAT, -- Weight at time of race
  FTP INTEGER, -- FTP at time of race
  FinishTime FLOAT, -- Race Time in seconds for fastest race Rider rode for Stage
  Position INTEGER, -- Rider's Position in Stage
  Points INTEGER, -- Rider's Points in Stage
  RaceId INTEGER, -- FK to Race table where Rider acheived FinishTime
  LastCalc TEXT, -- date & time that the StageResult record was last calculated -- ISO8601,'', 'YYYY-MM-DDTHH,'',MM,'',SSZ'
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
  CurrentWeight REAL, -- in kgs
  CurrentFTP INTEGER,
  TimeZone TEXT
  );

DROP TABLE IF EXISTS Participant;

 CREATE TABLE Participant (	
  -- rowid (implicit system row-count)
  SeriesId INTEGER, -- FK to Series table
  RiderId	INTEGER, -- FK to Rider table
  UNIQUE (SeriesId, RiderId)
  );

DROP TABLE IF EXISTS OAuthKey;

 CREATE TABLE OAuthKey (	
  Id INTEGER PRIMARY KEY,
  RiderId INTEGER UNIQUE, -- FK to Rider table
  AccessToken TEXT UNIQUE,
  RefreshToken TEXT UNIQUE,
  ExpiresAt TEXT -- Datetime
  );

/* Lookup tables 
   - table creation followed by population statements*/

DROP TABLE IF EXISTS AgeGroup;

 CREATE TABLE AgeGroup (	
  Id INTEGER PRIMARY KEY,
  StartAge INTEGER UNIQUE, -- ie 0, 19, 35 etc
  EndAge INTEGER UNIQUE -- ie 18, 34, 39, 44, 49 etc
  );

INSERT INTO AgeGroup (StartAge,EndAge)
VALUES 
   (0,18),
   (19,34),
   (35,39),
   (40,44),
   (45,49),
   (50,54),
   (55,59),
   (60,64),
   (65,69),
   (70,74),
   (75,79),
   (80,84),
   (85,89),
   (90,200);
		
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

   
DROP TABLE IF EXISTS Nationality;

 CREATE TABLE Nationality (	
  Id INTEGER PRIMARY KEY,  -- 1 to x
  CountryCode TEXT UNIQUE, -- ISO 3166
  Country TEXT UNIQUE,
  Nationality TEXT
  );

INSERT INTO Nationality (CountryCode, Country, Nationality)
VALUES 
    ('AF','Afghanisthan','Afghan'),
    ('AL','Albania','Albanian'),
    ('DZ','Algeria','Algerian'),
    ('AS','American Samoa', 'American Samoan'),
    ('AD','Andora', 'Andorran'),
    ('AO','Angola', 'Angolan'),
    ('AG','Antigua & Barbados', 'Antiguan or Barbudan'),
    ('AR','Argentina', 'Argentine'),
    ('AM','Armenia', 'Armenian'),
    ('AU','Australia', 'Australian'),
    ('AT','Austria', 'Austrian'),
    ('AZ','Azerbaijan', 'Azerbaijani'),
    ('BS','Bahamas', 'Bahamian'),
    ('BH','Bahrain', 'Bahraini'),
    ('BD','Bangladesh', 'Bangladeshi'),
    ('BB','Barbados', 'Barbadian'),
    ('BY','Belarus', 'Belarusian'),
    ('BE','Belgium', 'Belgian'),
    ('BZ','Belize', 'Belizean'),
    ('BJ','Benin', 'Beninese'),
    ('BT','Bhutan', 'Bhutanese'),
    ('BO','Bolivia', 'Bolivian'),
    ('BA','Bosnia & Herzegovinia', 'Bosnian or Herzegovinian'),
    ('BW','Botswana', 'Botswanan'),
    ('BR','Brazil', 'Brazilian'),
    ('BN','Brunei', 'Bruneian'),
    ('BG','Bulgaria', 'Bulgarian'),
    ('BF','Burkina Faso', 'Burkinabé'),
    ('BI','Burundi', 'Burundian'),
    ('KH','Cambodia', 'Cambodian'),
    ('CM','Cameroon', 'Cameroonian'),
    ('CA','Canada', 'Canadian'),
    ('CV','Cape Verde', 'Cape Verdean'),
    ('CF','Central African Republic', 'Central African'),
    ('TD','Chad', 'Chadian'),
    ('CL','Chile', 'Chilean'),
    ('CN','China', 'Chinese'),
    ('CO','Colombia', 'Colombian'),
    ('KM','Comoros', 'Comorian'),
    ('CG','Republic of the Congo', 'Congolese (Congo-Brazzaville)'),
    ('CD','Democratic Republic of the Congo', 'Congolese (Congo-Kinshasa)'),
    ('CR','Costa Rica', 'Costa Rican'),
    ('CI','Ivory Coast', 'Ivorian'),
    ('HR','Croatia', 'Croatian'),
    ('CU','Cuba', 'Cuban'),
    ('CY','Cyress', 'Cypriot'),
    ('CZ','Czechia', 'Czech'),
    ('DK','Denmark', 'Danish'),
    ('DJ','Dijibouti', 'Djiboutian'),
    ('DM','Dominica', 'Dominican'),
    ('DO','Dominican Republic', 'Dominican'),
    ('EC','Ecuador', 'Ecuadorian'),	
    ('EG','Egypt', 'Egyptian'),
    ('SV','Salvador', 'Salvadoran'),
    ('GQ','Equatorial Guinea', 'Equatorial Guinean'),
    ('ER','Eritrea', 'Eritrean'),
    ('EE','Estonia', 'Estonian'),
    ('SZ','Eswatini', 'Eswatini'),
    ('ET','Ethiopia', 'Ethiopian'),
    ('FJ','Fiji', 'Fijian'),
    ('FI','Finalnd', 'Finnish'),
    ('FR','France', 'French'),
    ('GA','Gabon', 'Gabonese'),
    ('GM','Gambia', 'Gambian'),
    ('GE','Georgia', 'Georgian'),
    ('DE','Germany', 'German'),
    ('GH','Ghana', 'Ghanaian'),
    ('GR','Greece', 'Greek'),
    ('GD','Grenada', 'Grenadian'),
    ('GT','Guatemala', 'Guatemalan'),
    ('GN','Guinea', 'Guinean'),
    ('GW','Bissau-Guinea', 'Bissau-Guinean'),
    ('GY','Guyana', 'Guyanese'),
    ('HT','Haiti', 'Haitian'),
    ('HN','Honduras', 'Honduran'),
    ('HU','Hungary', 'Hungarian'),
    ('IS','Iceland', 'Icelandic'),
    ('IN','India', 'Indian'),
    ('ID','Indonesia', 'Indonesian'),
    ('IR','Iran', 'Iranian'),
    ('IQ','Iraq', 'Iraqi'),
    ('IE','Ireland', 'Irish'),
    ('IL','Israel', 'Israeli'),
    ('IT','Italy', 'Italian'),
    ('JM','Jamaica', 'Jamaican'),
    ('JP','Japan', 'Japanese'),
    ('JO','Jordan', 'Jordanian'),
    ('KZ','Kazakhstan', 'Kazakhstani'),
    ('KE','Kenya', 'Kenyan'),
    ('KI','Kiribati', 'I-Kiribati'),
    ('KR','South Korea', 'South Korean'),
    ('KW','Kuwait', 'Kuwaiti'),
    ('KG','Kyrgyzstan', 'Kyrgyz'),
    ('LA','Laos', 'Lao'),
    ('LV','Latvia', 'Latvian'),
    ('LB','Lebanon', 'Lebanese'),
    ('LS','Basotho', 'Basotho'),
    ('LR','Liberia', 'Liberian'),
    ('LY','Libya', 'Libyan'),
    ('LI','Liechtenstein', 'Liechtensteiner'),
    ('LT','Lithuania', 'Lithuanian'),
    ('LU','Luxembourg', 'Luxembourger'),
    ('MG','Madagascar', 'Malagasy'),
    ('MW','Malawai', 'Malawian'),
    ('MY','Malaysia', 'Malaysian'),
    ('MV','Maldives', 'Maldivian'),
    ('ML','Mali', 'Malian'),
    ('MT','Malta', 'Maltese'),
    ('MH','Marshall Islands', 'Marshallese'),
    ('MU','Mauritius', 'Mauritian'),
    ('MX','Mexico', 'Mexican'),
    ('FM','Micronesia', 'Micronesian'),
    ('MD','Moldova', 'Moldovan'),
    ('MC','Monaco', 'Monégasque'),
    ('MN','Mongolia', 'Mongolian'),
    ('ME','Montenegro', 'Montenegrin'),
    ('MA','Morroco', 'Moroccan'),
    ('MZ','Mozambique', 'Mozambican'),
    ('MM','Mayanma', 'Burmese'),
    ('NA','Nambia', 'Namibian'),
    ('NR','Nauru', 'Nauruan'),
    ('NP','Nepal', 'Nepalese'),
    ('NL','Netherlands', 'Dutch'),
    ('NZ','New Zealand', 'New Zealander'),
    ('NI','Nicaragua', 'Nicaraguan'),
    ('NE','Niger', 'Nigerien'),
    ('NG','Nigeria', 'Nigerian'),
    ('NO','Norway', 'Norwegian'),
    ('OM','Oman', 'Omani'),
    ('PK','Pakisthan', 'Pakistani'),
    ('PW','Palau', 'Palauan'),
    ('PA','Panama', 'Panamanian'),
    ('PG','Papa New Guinea', 'Papua New Guinean'),
    ('PY','Paraguy', 'Paraguayan'),
    ('PE','Peru', 'Peruvian'),
    ('PH','Philippines', 'Filipino'),
    ('PL','Poland', 'Polish'),
    ('PT','Portugal', 'Portuguese'),
    ('QA','Qatar', 'Qatari'),
    ('RO','Romania', 'Romanian'),
    ('RU','Russia', 'Russian'),
    ('RW','Rwanda', 'Rwandan'),
    ('WS','Samoa', 'Samoan'),
    ('SA','Saudi Arabia', 'Saudi Arabian'),
    ('SN','Senegal', 'Senegalese'),
    ('RS','Serbia', 'Serbian'),
    ('SC','Seychelles', 'Seychellois'),
    ('SL','Sierra Leon', 'Sierra Leonean'),
    ('SG','Singapore', 'Singaporean'),
    ('SK','Slovakia', 'Slovak'),
    ('SI','Slovenia', 'Slovenian'),
    ('SB','Solomon Islands', 'Solomon Islander'),
    ('SO','Somali', 'Somali'),
    ('ZA','South Africa', 'South African'),
    ('ES','Spain', 'Spanish'),
    ('LK','Sri Lanka', 'Sri Lankan'),
    ('SD','Sudan', 'Sudanese'),
    ('SR','Surinam', 'Surinamese'),
    ('SE','Sweden', 'Swedish'),
    ('CH','Switzerland', 'Swiss'),
    ('SY','Syria', 'Syrian'),
    ('TW','Taiwan', 'Taiwanese'),
    ('TJ','Tajikistan', 'Tajik'),
    ('TZ','Tanzania', 'Tanzanian'),
    ('TH','Thailand', 'Thai'),
    ('TL','Timor', 'Timorese'),
    ('TG','Togo', 'Togolese'),
    ('TO','Tongo', 'Tongan'),
    ('TT','Trinidad & Tobago', 'Trinidadian or Tobagonian'),
    ('TN','Tunisia', 'Tunisian'),
    ('TR','Türkiye', 'Turkish'),
    ('TM','Turkmenistan', 'Turkmen'),
    ('TV','Tuvalu', 'Tuvaluan'),
    ('UG','Uganda', 'Ugandan'),
    ('UA','Ukraine', 'Ukrainian'),
    ('AE','United Arab Emirates', 'Emirati'),
    ('GB','United Kingdom', 'British'),
	('GB-ENG','England','English'),	
	('GB-SCT','Scotland','Scotish'),	
	('GB-CMY','Wales','Welsh'),
	('GB-NIR','Northern Ireland','Northern Irish'),
	('IM','Isle of Man','Manx'),
    ('US','United States of America', 'American'),
    ('UY','Uruguay', 'Uruguayan'),
    ('UZ','Uzbekisthan', 'Uzbek'),
    ('VU','Vanuatu', 'Ni-Vanuatu'),
    ('VE','Venezuela', 'Venezuelan'),
    ('VN','Vietnam', 'Vietnamese'),
    ('YE','Yemen', 'Yemeni'),
    ('ZM','Zambia', 'Zambian'),
    ('ZW','Zimbabwe', 'Zimbabwean');



  
  
  
