# test_env.py
from dotenv import load_dotenv
import os

load_dotenv()  # Load the .env file

# Test if TOKEN is loaded
token = os.getenv("TOKEN")
print("TOKEN:", token)
