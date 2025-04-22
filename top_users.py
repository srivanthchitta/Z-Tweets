import sys
from datetime import datetime, timezone
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

def top_users(collection):
    # obtains number of users prompted to be displayed or 'q'
    n = prompt_number()

    # quits if prompted
    if n == 'q':
        return
    
    else:
        try:
            # Retrieve top n users sorted by followersCount in descending order
            tweet_documents = list(
                collection.aggregate([
                    {
                        "$group": {
                            "_id": "$user.id",  # Group by user ID
                            "user": {"$first": "$user"},  # Grab the entire user object
                            "followersCount": {"$max": "$user.followersCount"}  # Use max to get the highest followersCount
                        }
                    },
                    {
                        "$sort": {"followersCount": -1}  # Sort by followersCount in descending order
                    },
                    {
                        "$limit": n  # Retrieve only the top n users
                    }
                ])
            )

            # feedback if no users found
            if not tweet_documents:
                print("No users found.")
                return
            
            # displays feedback if requested amount of users are not found
            if len(tweet_documents) != n:
                n = len(tweet_documents)
                print(f"\nCould only find {n} users...")

            # displays how many users will appear
            print(f"\nTop {n} users by follower count:")
            i = 1

            for tweet in tweet_documents:
                # attempts to get username, displayname, and followers count from the tweet document
                try:
                    username = tweet['user']['username']
                except:
                    username = 'Not found'
                try:
                    display_name = tweet['user']['displayname']
                except:
                    display_name = 'Not found'
                try:
                    followers_count = tweet['user']['followersCount']
                except:
                    followers_count = 'Not found'

                # prints the required info for each user
                print(f"{i}) Username: {username}, Display Name: {display_name}, Followers: {followers_count}")
                i = i + 1

            
            while True:
                # prompts user to enter the rank of the user to view their profile
                print(f"\nEnter the rank of the user to see their full information or 'q' to go quit.")
                choice = input("> ").strip()

                # quits if prompted
                if choice.lower() == 'q':
                    return
                
                # displays all info from user if command is valid
                if choice.isdigit() and 1 <= int(choice) <= len(tweet_documents):
                    index = int(choice) - 1
                    selected_user = collection.find_one({"user.username": tweet_documents[index]["user"]["username"]}, {"_id": 0})
                    for key, value in selected_user["user"].items():
                        # Format the display of each key-value pair
                        formatted_key = key.replace("_", " ").capitalize()
                        print(f"{formatted_key}: {value}")
                    return
                
                # prompts user to try again due to invalidity of command
                else:
                    print("Your input was invalid. Try again.")

        except Exception as e:
            print(f"Error listing top users: {e}")

def prompt_number():
    print("Enter the number of top users to display or 'q' to go back.")
    while True:
        try:
            # prompts user for command and returns command
            n = input("> ").strip()
            if n == 'q':
                return n
            elif int(n) > 0:
                return int(n)
            
            # prompts user to try again due to invalid command
            else:
                print("\nInvalid input. Please input a positive number or 'q' to go back.")
        except:
            print("\nInvalid input. Please input a positive number or 'q' to go back.")


def compose_tweet(collection):
    print(f"\nWhat would you like to post on 'Z'?")
    tweet_content = input("> ").strip()

    if not tweet_content:
        print("Tweets on 'Z' cannot be empty.")
        return
    
    # Create the tweet document
    tweet = {
        "url": None,
        "date": f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')}+00:00",
        "content": tweet_content,
        "renderedContent": None,
        "id": None,
        "user": {
            "username": "291user",
            "displayname": None,
            "id": None,
            "description": None,
            "rawDescription": None,
            "descriptionUrls": None,
            "verified": None,
            "created": None,
            "followersCount": None,
            "friendsCount": None,
            "statusesCount": None,
            "favouritesCount": None,
            "listedCount": None,
            "mediaCount": None,
            "location": None,
            "protected": None,
            "linkUrl": None,
            "linkTcourl": None,
            "profileImageUrl": None,
            "profileBannerUrl": None,
            "url": None
        },
        "outlinks": None,
        "tcooutlinks": None,
        "replyCount": None,
        "retweetCount": None,
        "likeCount": None,
        "quoteCount": None,
        "conversationId": None,
        "lang": None,
        "source": None,
        "sourceUrl": None,
        "sourceLabel": None,
        "media": None,
        "retweetedTweet": None,
        "quotedTweet": None,
        "mentionedUsers": None
        }


    # Insert the tweet into the database
    result = collection.insert_one(tweet)

