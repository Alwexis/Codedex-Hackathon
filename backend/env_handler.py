from dotenv import load_dotenv
import os

# Load environment variables from the .env file (if present)
load_dotenv()

# Access environment variables as if they came from the actual environment
env = {
    "DB_URL": os.getenv('DATABASE_URL'),
    "DB_NAME": os.getenv('DB_NAME'),
    "CYPH_SECRET_KEY": os.getenv('CYPH_SECRET_KEY'),
    "IMGDB_KEY": os.getenv('IMGDB_KEY'),
    "IMGDB_URL": os.getenv('IMGDB_URL'),
}