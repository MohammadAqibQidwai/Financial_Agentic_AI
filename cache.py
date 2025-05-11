import os
import redis
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Redis client
try:
    redis_client = redis.Redis(
        host="localhost",  # Change this if Redis is running on another machine
        port=6379,
        db=0,
        decode_responses=True
    )
    redis_client.ping()  # Test connection
    redis_enabled = True
except redis.ConnectionError:
    print("⚠️ Warning: Redis is not running. Caching will be disabled.")
    redis_enabled = False

# Function to get cached response (Only for Web Search)
def get_cached_response(query):
    if redis_enabled:
        cached_data = redis_client.get(query)
        if cached_data:
            return json.loads(cached_data)
    return None

# Function to store response in cache (Only for Web Search, expires in 1 hour)
def cache_response(query, response, expiry=3600):
    if redis_enabled:
        redis_client.set(query, json.dumps(response), ex=expiry)
