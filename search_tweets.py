import sys
from pymongo import MongoClient
from datetime import datetime

def connect_to_mongo(port_number):
    try:
        # Connect to MongoDB server
        client = MongoClient(f"mongodb://localhost:{port_number}")
        db = client["291db"]
        print(f"Connected to MongoDB! Port Number: {port_number}")
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        sys.exit(1)

def json_load(file_path, db):
    tweets_collection = db['tweets']
    
    # Drop existing collection
    tweets_collection.drop()
    
    try:
        with open(file_path, 'r') as file:
            data = [json.loads(line) for line in file]
            
            # Use the 'id' field as the '_id' field
            for tweet in data:
                tweet['_id'] = tweet.pop('_id')
            
            tweets_collection.insert_many(data)
            print(f"Inserted {len(data)} records into the database.")
    except Exception as e:
        print(f"Error loading JSON file: {e}")

def search_tweets(collection):
    '''
    This function searches for tweets based on user-provided keywords (hashtags and text)
    and calls the display function for viewing and interacting with results.
    Only alphanumeric keywords are allowed.
    '''
    while True:
        # Input and parse keywords
        keywords = input("Enter keywords (comma-separated, only alphanumeric characters allowed): ").split(',')
        keywords = [kw.strip() for kw in keywords]

        # Validate keywords
        if all(kw.isalnum() for kw in keywords):
            break
        else:
            print("Error: Keywords must only contain alphanumeric characters. Please try again.")

    # Build MongoDB query
    query = {"$and": []}

    # Match each keyword in the "content" field
    for kw in keywords:
        query["$and"].append({
            "content": {
                "$regex": f"\\b{kw.lower()}\\b",
                "$options": "i"  # Case insensitive
            }
        })

    # Fetch results
    results = list(collection.find(query).sort([("date", -1)]))  # Sort by date descending

    # Remove duplicates by content, user, and date
    unique_results = []
    seen = set()
    for tweet in results:
        unique_key = (tweet['content'], tweet['user']['username'], tweet['date'])
        
        if unique_key not in seen:
            seen.add(unique_key)
            unique_results.append(tweet)

    # Display results and handle pagination
    display_tweets(results, collection)
    return



  

def display_tweets(results, collection):
    '''
    This function displays tweets as paginated results (5 tweets per page),
    and prompts user interaction to view specific tweets, view next page, or quit.
    '''
    if not results:
        print("No tweets or retweets found.")
        return

    results_per_page = 5
    total_results = len(results)
    current_index = 0
    i = 1

    print(f"\nDisplaying tweets {i} to {total_results}")
    for tweet in results:
        print(f"{i}. Tweet ID: {tweet.get('id')}, User: {tweet['user']['username']}")
        print(f"   Date: {tweet['date']}")
        print(f"   Text: {tweet['content']}\n")
        i = i + 1

    # User options
    while True:
        # prompts user to enter the rank of the user to view their profile
        print(f"\nEnter the rank of the tweet to see their full information or 'q' to go quit.")
        choice = input("> ").strip()

        # quits if prompted
        if choice.lower() == 'q':
            return
        
        elif choice.isdigit() and 1 <= int(choice) <= total_results:
            selected_index = current_index + int(choice) - 1
            selected_id = results[selected_index]['id']
            show_tweet_details(selected_id, collection)
            return
        else:
            print("Invalid input. Please try again.")


def show_tweet_details(id, collection):
    '''
    Shows all details of a specific tweet (Tweet ID, username, date, content, and additional metadata).
    '''

    selected_tweet = collection.find_one({"id": id}, {"_id": 0})
    for key, value in selected_tweet.items():
        # Format the display of each key-value pair
        if key == 'user':
            print("User: ")
            for user_key , user_value in selected_tweet['user'].items():
                user_formatted_key = user_key.replace("_", " ").capitalize()
                print(f"\t{user_formatted_key}: {user_value}")
        else:
            formatted_key = key.replace("_", " ").capitalize()
            print(f"{formatted_key}: {value}")
    return

