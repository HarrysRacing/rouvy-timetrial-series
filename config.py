from dotenv import load_dotenv
import os

load_dotenv()

DATABASE = os.getenv("DATABASE")
CLIENT_ID = os.getenv("ROUVY_CLIENT_ID")
CLIENT_SECRET = os.getenv("ROUVY_CLIENT_SECRET")