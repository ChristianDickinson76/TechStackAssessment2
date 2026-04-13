"""
Purpose: Seed MongoDB with sample users, resources, and comments for development/testing.
Data handled:
- Input: none (hardcoded sample data)
- MongoDB write: users, resources, comments collections
- Output: console log of inserted documents
"""

import os
import sys
from datetime import datetime, timedelta
from bson import ObjectId
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DB", "skillhub")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

users = db["users"]
resources = db["resources"]
comments = db["comments"]

def seed_database():
    """
    Purpose: Insert sample data into MongoDB collections.
    Data handled:
    - Creates 3 sample users with hashed passwords
    - Creates 12 sample resources across 4 hobbies
    - Creates 8 sample comments on resources
    """
    
    try:
        # Clear existing data (optional - comment out to append instead)
        print("Clearing existing collections...")
        users.delete_many({})
        resources.delete_many({})
        comments.delete_many({})
        
        # Create sample users
        print("\n--- Seeding Users ---")
        sample_users = [
            {
                "fullname": "Alice Johnson",
                "username": "alice_coder",
                "email": "alice@example.com",
                "password": generate_password_hash("password123"),
                "profileImage": "",
                "hobbies": ["coding", "aitools"],
                "createdAt": datetime.utcnow()
            },
            {
                "fullname": "Bob Smith",
                "username": "bob_chef",
                "email": "bob@example.com",
                "password": generate_password_hash("password456"),
                "profileImage": "",
                "hobbies": ["cooking", "football"],
                "createdAt": datetime.utcnow()
            },
            {
                "fullname": "Carol Davis",
                "username": "carol_musician",
                "email": "carol@example.com",
                "password": generate_password_hash("password789"),
                "profileImage": "",
                "hobbies": ["music"],
                "createdAt": datetime.utcnow()
            }
        ]
        
        user_result = users.insert_many(sample_users)
        print(f"✓ Inserted {len(user_result.inserted_ids)} users")
        user_ids = user_result.inserted_ids
        
        # Create sample resources
        print("\n--- Seeding Resources ---")
        sample_resources = [
            # Coding hobby
            {
                "title": "Python Beginners Guide",
                "description": "A comprehensive guide to learning Python from scratch. Covers variables, loops, functions, and more.",
                "hobby": "coding",
                "category": "Coding",
                "link": "https://www.python.org/about/gettingstarted/",
                "image": "",
                "authorId": user_ids[0],
                "votes": 5,
                "userVotes": {str(user_ids[1]): 1, str(user_ids[2]): 1},
                "createdAt": datetime.utcnow() - timedelta(days=3)
            },
            {
                "title": "JavaScript ES6 Features",
                "description": "Learn modern JavaScript including arrow functions, destructuring, and async/await.",
                "hobby": "coding",
                "category": "Coding",
                "link": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference",
                "image": "",
                "authorId": user_ids[0],
                "votes": 8,
                "userVotes": {str(user_ids[1]): 1},
                "createdAt": datetime.utcnow() - timedelta(days=2)
            },
            {
                "title": "Web Development Bootcamp",
                "description": "Full-stack web development course covering HTML, CSS, JavaScript, and backend frameworks.",
                "hobby": "coding",
                "category": "Coding",
                "link": "https://www.udemy.com/topic/web-development/",
                "image": "",
                "authorId": user_ids[0],
                "votes": 12,
                "userVotes": {},
                "createdAt": datetime.utcnow() - timedelta(days=1)
            },
            # Cooking hobby
            {
                "title": "Easy Pasta Recipes",
                "description": "Collection of simple yet delicious pasta dishes perfect for beginners.",
                "hobby": "cooking",
                "category": "Cooking",
                "link": "https://www.bbcgoodfood.com/recipes/collection/pasta-recipes",
                "image": "",
                "authorId": user_ids[1],
                "votes": 7,
                "userVotes": {str(user_ids[0]): 1},
                "createdAt": datetime.utcnow() - timedelta(days=3)
            },
            {
                "title": "Baking Sourdough Bread",
                "description": "Step-by-step guide to making authentic sourdough bread from scratch at home.",
                "hobby": "cooking",
                "category": "Cooking",
                "link": "https://www.kingarthurbaking.com/recipes/sourdough",
                "image": "",
                "authorId": user_ids[1],
                "votes": 10,
                "userVotes": {str(user_ids[0]): 1, str(user_ids[2]): 1},
                "createdAt": datetime.utcnow() - timedelta(days=2)
            },
            {
                "title": "Vegetarian Meal Prep",
                "description": "Quick and healthy vegetarian meals you can prepare in advance for the week.",
                "hobby": "cooking",
                "category": "Cooking",
                "link": "https://www.healthline.com/nutrition/vegetarian-meal-prep",
                "image": "",
                "authorId": user_ids[1],
                "votes": 6,
                "userVotes": {},
                "createdAt": datetime.utcnow() - timedelta(days=1)
            },
            # Football hobby
            {
                "title": "Improve Your Passing Accuracy",
                "description": "Training drills and techniques to enhance your passing precision and consistency on the field.",
                "hobby": "football",
                "category": "Football",
                "link": "https://www.footballfancast.com/passing-drills",
                "image": "",
                "authorId": user_ids[1],
                "votes": 4,
                "userVotes": {str(user_ids[0]): -1},
                "createdAt": datetime.utcnow() - timedelta(days=3)
            },
            {
                "title": "Defensive Positioning Guide",
                "description": "Master the fundamentals of defensive positioning and tactical awareness in football.",
                "hobby": "football",
                "category": "Football",
                "link": "https://www.uefa.com/training",
                "image": "",
                "authorId": user_ids[1],
                "votes": 9,
                "userVotes": {str(user_ids[2]): 1},
                "createdAt": datetime.utcnow() - timedelta(days=2)
            },
            {
                "title": "Fitness Routine for Athletes",
                "description": "Comprehensive workout plans designed to build strength and endurance for footballers.",
                "hobby": "football",
                "category": "Football",
                "link": "https://www.healthline.com/health/fitness-exercise/football-conditioning",
                "image": "",
                "authorId": user_ids[1],
                "votes": 11,
                "userVotes": {},
                "createdAt": datetime.utcnow() - timedelta(days=1)
            },
            # AI Tools hobby
            {
                "title": "ChatGPT Prompt Engineering",
                "description": "Learn how to write effective prompts to get better results from AI language models.",
                "hobby": "aitools",
                "category": "AI Tools",
                "link": "https://openai.com/blog/prompt-engineering",
                "image": "",
                "authorId": user_ids[0],
                "votes": 15,
                "userVotes": {str(user_ids[1]): 1, str(user_ids[2]): 1},
                "createdAt": datetime.utcnow() - timedelta(days=3)
            },
            {
                "title": "Introduction to Machine Learning",
                "description": "Beginner-friendly guide to machine learning concepts, algorithms, and practical applications.",
                "hobby": "aitools",
                "category": "AI Tools",
                "link": "https://www.coursera.org/learn/machine-learning",
                "image": "",
                "authorId": user_ids[0],
                "votes": 13,
                "userVotes": {str(user_ids[1]): 1},
                "createdAt": datetime.utcnow() - timedelta(days=2)
            },
            {
                "title": "AI Tools for Content Creation",
                "description": "Explore AI tools like DALL-E, Midjourney, and other generative models for creative projects.",
                "hobby": "aitools",
                "category": "AI Tools",
                "link": "https://www.midjourney.com/",
                "image": "",
                "authorId": user_ids[0],
                "votes": 18,
                "userVotes": {},
                "createdAt": datetime.utcnow() - timedelta(days=1)
            }
        ]
        
        resource_result = resources.insert_many(sample_resources)
        print(f"✓ Inserted {len(resource_result.inserted_ids)} resources")
        resource_ids = resource_result.inserted_ids
        
        # Create sample comments
        print("\n--- Seeding Comments ---")
        sample_comments = [
            {
                "resourceId": resource_ids[0],
                "authorId": user_ids[1],
                "authorName": "bob_chef",
                "text": "Great introduction! Really helped me get started with Python.",
                "createdAt": datetime.utcnow() - timedelta(days=2)
            },
            {
                "resourceId": resource_ids[0],
                "authorId": user_ids[2],
                "authorName": "carol_musician",
                "text": "Clear explanations. Would love more examples.",
                "createdAt": datetime.utcnow() - timedelta(days=1)
            },
            {
                "resourceId": resource_ids[1],
                "authorId": user_ids[1],
                "authorName": "bob_chef",
                "text": "ES6 features are powerful. This guide makes them easy to understand.",
                "createdAt": datetime.utcnow() - timedelta(days=1)
            },
            {
                "resourceId": resource_ids[3],
                "authorId": user_ids[0],
                "authorName": "alice_coder",
                "text": "Love these pasta recipes! Simple and tasty.",
                "createdAt": datetime.utcnow() - timedelta(days=2)
            },
            {
                "resourceId": resource_ids[4],
                "authorId": user_ids[0],
                "authorName": "alice_coder",
                "text": "Sourdough is tricky but this guide made it manageable!",
                "createdAt": datetime.utcnow() - timedelta(days=1)
            },
            {
                "resourceId": resource_ids[8],
                "authorId": user_ids[1],
                "authorName": "bob_chef",
                "text": "Prompt engineering is a skill everyone should learn.",
                "createdAt": datetime.utcnow() - timedelta(days=2)
            },
            {
                "resourceId": resource_ids[8],
                "authorId": user_ids[2],
                "authorName": "carol_musician",
                "text": "Mind blown by what good prompts can achieve!",
                "createdAt": datetime.utcnow() - timedelta(days=1)
            },
            {
                "resourceId": resource_ids[10],
                "authorId": user_ids[1],
                "authorName": "bob_chef",
                "text": "DALL-E is incredible for visual ideas. Highly recommend.",
                "createdAt": datetime.utcnow() - timedelta(hours=12)
            }
        ]
        
        comment_result = comments.insert_many(sample_comments)
        print(f"✓ Inserted {len(comment_result.inserted_ids)} comments")
        
        print("\n✓ Database seeding complete!")
        print(f"  - {len(user_result.inserted_ids)} users")
        print(f"  - {len(resource_result.inserted_ids)} resources")
        print(f"  - {len(comment_result.inserted_ids)} comments")
        
    except Exception as e:
        print(f"✗ Seeding failed: {e}")
        sys.exit(1)
    finally:
        client.close()

if __name__ == "__main__":
    seed_database()