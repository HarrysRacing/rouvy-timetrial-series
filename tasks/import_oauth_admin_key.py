# 
# This script is used to load the OAuthKey data for the Admin user to the (production) database
#

from pathlib import Path

import sqlite3
import traceback

DB_PATH = Path(__file__).resolve().parent.parent / "database" / "harrysracing.db"

FILE_PATH = Path(__file__).resolve().parent.parent / "database" / "oauth_token_data.txt"

try:

   #check that the file exists in the database directory


   #read the lines from the file in a for loop
   with open(FILE_PATH, 'r') as f:  # Open file for read
      line_num = 1
      for line in f:           # Read line-by-line
        line = line.strip()  # Strip the leading/trailing whitespaces and newline
        # Process the line
        if line_num == 1:
            accesstoken = line
        elif line_num == 2:
            refreshtoken = line
        else:
            expiresat = line
            
        line_num = line_num + 1
    
      #update the OAuthKey table in harrysracing.db 
      with sqlite3.connect(DB_PATH) as conn:
         cursor = conn.cursor()
      
         query = ('UPDATE OAuthKey '
                  'SET AccessToken = ?, '
                  '    RefreshToken = ?, '
                  '    ExpiresAt = ? '
                  'WHERE Id = 1;'
                  )

         cursor.execute(query,(accesstoken,refreshtoken,expiresat))
         
except Exception as e:
    print('Error occurred -', e)
    traceback.print_exc()         