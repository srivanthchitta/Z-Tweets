import sys
import json
import re
from pymongo import MongoClient

def connect_to_mongo(port_number):
    try:
        # Connect to MongoDB server
        client = MongoClient(f"mongodb://localhost:{port_number}")
        db = client["291db"]
        print(f"Connected to MongoDB! Port Number:{port_number}")
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        sys.exit(1)

def extract_keywords(input_string):
    """Extract alphanumeric keywords from the input."""
    return re.findall(r"[a-zA-Z0-9]+", input_string)

def search_users(collection):
    while True:
        print("\nEnter a keyword to search for users (or 'q' to quit):")
        keyword_input = input("> ").strip()

        # Quit if 'q' is entered
        if keyword_input.lower() == 'q':
            print("Exiting search.")
            break

        try:
            # Extract alphanumeric keywords
            keywords = extract_keywords(keyword_input)

            if not keywords:
                print("No valid keywords found. Please enter alphanumeric keywords.")
                continue  # Prompt user again

            # Build $or condition with individual $regex patterns
            regex_conditions = [
                {"user.displayname": {"$regex": f"\\b{keyword}\\b", "$options": "i"}} for keyword in keywords
            ] + [
                {"user.location": {"$regex": f"\\b{keyword}\\b", "$options": "i"}} for keyword in keywords
            ]

            # Define aggregation pipeline for case-insensitive keyword matching
            pipeline = [
                {
                    "$match": {
                        "$or": regex_conditions
                    }
                },
                {
                    "$group": {
                        "_id": "$user.username",  # Group by username to remove duplicates
                        "username": {"$first": "$user.username"},
                        "displayname": {"$first": "$user.displayname"},
                        "location": {"$first": "$user.location"}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "username": 1,
                        "displayname": 1,
                        "location": 1
                    }
                }
            ]


            # Execute aggregation pipeline
            users = list(collection.aggregate(pipeline))

            if not users:
                print("\nNo users found for the given keywords.")
                continue  # Prompt user again

            print("\nResults:")
            for i, user in enumerate(users, start=1):
                username = user.get("username", "Not found")
                displayname = user.get("displayname", "Not found")
                location = user.get("location", "Not found")
                print(f"{i}. Username: {username}, Display Name: {displayname}, Location: {location}")

            while True:
                # View full details of a user
                print("\nEnter the number of the user to view full information, or 'q' to quit:")
                choice = input("> ").strip()

                # Quit if 'q' is entered
                if choice.lower() == 'q':
                    break

                # Display full details of a selected user
                if choice.isdigit() and 1 <= int(choice) <= len(users):
                    index = int(choice) - 1
                    selected_user = users[index]
                    full_user = collection.find_one(
                        {"user.username": selected_user["username"]},
                        {"_id": 0, "user": 1}
                    )
                    if full_user:
                        print("\nFull details:")
                        for key, value in full_user["user"].items():
                            print(f"{key.capitalize()}: {value}")
                    else:
                        print("Details not found.")
                    break
                else:
                    print("Invalid input. Please try again.")

        except Exception as e:
            print(f"Error searching for users: {e}")

        while True:
            print("\nDo you want to search again? (y/n)")
            choice = input("> ").strip().lower()
            if choice == 'y':
                break  # Continue to the next search
            elif choice == 'n':
                print("Exiting search.")
                return  # Exit the function
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

def test_search_users(file_path, port_number):
    """Load data into MongoDB and test search_users"""
    # Connect to MongoDB
    db = connect_to_mongo(port_number)
    collection = db["tweets"]
    collection.drop()  # Clear any existing data

    # Load data from JSON file
    try:
        with open(file_path, 'r') as f:
            data = [json.loads(line) for line in f]
        collection.insert_many(data)
        print(f"Loaded {len(data)} records into MongoDB.")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # Call search_users for testing
    print("\n--- Testing search_users ---")
    search_users(collection)

    print("Exiting test.")

