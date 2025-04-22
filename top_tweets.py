""""
List top tweets functionality implemented in this file.
3. List top tweets 
The user should be able to list top n tweets based on any of the fields retweetCount, likeCount, quoteCount, to 
be selected by the user. The value of n will be also entered by the user. The result will be ordered in a 
descending order of the selected field. For each matching tweet, display the id, date, content, and username of 
the person who posted it. The user should be able to select a tweet and see all fields. 

"""
def get_top_tweets_input():
    while True:
        print("Enter the number of top tweets to diplay or 'q' to exit to menu.")
        n = input(">")
        if n == 'q':
            return None, None
        elif n == '0':
            print("No tweets shown since choice was 0.")
            return None, None
        elif n.isdigit():
            n = int(n)
            break
        else:
            print("Input error. PLease input q or a positive number")
    while True:
        print("\n\nChoose the field you want to order your tweets based on by selecting from the following:")
        print("1. retweetCount")
        print("2. likeCount")
        print("3. quoteCount")
        print("Enter the number of your desired chioce or 'q' to exit to menu.")
        field_choice = input(">")
        if field_choice == 'q':
            return None, None
        elif field_choice == '1':
            field = "retweetCount"
            return n, field
        elif field_choice == '2':
            field = "likeCount"
            return n, field
        elif field_choice == '3':
            field = "quoteCount"
            return n, field
        else:
            print("Input error. Please enter a number from 1-3 or 'q' to exit to menu.")

def list_top_tweets(collection):
    """
    Will Print top n tweets based on field chosen by user.
    """
    print("\n\n=====================================================")
    print("==================List top tweets====================")
    n, field = get_top_tweets_input()
    if n is None or field is None:
        print("Exiting to menu...")
        return 
    
    # query n tweets in descending order by chosen field
    # order by chosen field in descending
    tweet_documents = list(
        collection.aggregate([
            {
                "$sort": {field: -1}  # Sort by chosen field in descending order
            },
            {
                "$limit": int(n)  # Retrieve only the top n tweets
            }
        ])
    )
    # feedback if no tweets found
    if not tweet_documents:
        print("No tweets found.")
        return
    
    # displays feedback if requested amount of tweets are not found
    if len(tweet_documents) < n:
        n = len(tweet_documents)
        print(f"\nCould only find {n} tweets...")

    # displays how many users will appear
    print(f"\nTop {n} tweets by {field}:")
    tweet_ids = []
    # show id, date, content, and username
    for i, tweet in enumerate(tweet_documents):
        # attempts to get username, displayname, and followers count from the tweet document
        try:
            t_id = tweet['id']
        except:
            t_id = 'Not found'
        try:
            t_date = tweet['date']
        except:
            t_date = 'Not found'
        try:
            t_content = tweet['content']
        except:
            t_content = 'Not found'
        try:
            t_username = tweet['user']['username']
        except:
            t_username = 'Not found'  
        try:
            t_rank = tweet[field] 
        except:
            t_rank = 'Not found'

        # prints the required info for each user
        print(f"{i+1}) ID: {t_id}, Username: {t_username}, Date: {t_date}, {field}: {t_rank}\n\t\t Content: \n{t_content}")
        tweet_ids.append(t_id)

    # let user choose a tweet and show all fields
    while True:
        # prompts user to enter the rank of the user to view their profile
        print(f"\n\nEnter the rank of the tweet to see its full information or 'q' to exit to menu.")
        choice = input("> ").strip()

        # quits if prompted
        if choice.lower() == 'q':
            return
        
        # displays all info from user if command is valid
        if choice.isdigit() and 1 <= int(choice) <= len(tweet_documents):
            index = int(choice) - 1
            selected_tweet = collection.find_one({"id": tweet_ids[index]}, {"_id": 0})
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
        
        # prompts user to try again due to invalidity of command
        else:
            print("Your input was invalid. Try again.")


                
            
