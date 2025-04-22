import sys
import json
from pymongo import MongoClient


def create_db(json_file,port_number):
    try:
        # Connect to MongoDB
        client = MongoClient(f"mongodb://localhost:{port_number}")
        print(f"Connected to MongoDB at port_number {port_number}")


        # Drop the collection if it exists
        db = client["291db"]
        if "tweets" in db.list_collection_names():
            db["tweets"].drop()
            print("Existing 'tweets' collection dropped.")
        
        # Create new collection
        tweets_collection = db["tweets"]
        print("New 'tweets' collection created.")
    
        # Read JSON file and insert in batches
        batch_size = 1000
        with open(json_file, "r") as file:
            batch = []
            for line in file:
                try:
                    tweet = json.loads(line)
                    batch.append(tweet)
                    # Insert when batch size is reached
                    if len(batch) == batch_size:
                        tweets_collection.insert_many(batch)
                        print(f"Inserted a batch of {batch_size} tweets.")
                        batch = []  # Clear the batch
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid JSON line: {e}")
            
            # Insert any remaining tweets in the last batch
            if batch:
                tweets_collection.insert_many(batch)
                print(f"Inserted the last batch of {len(batch)} tweets.")


        print("All tweets inserted into MongoDB.")
    except Exception as e:
        print(f"An error occurred: {e}")


    finally:
        client.close()
        print("MongoDB connection closed.")




def main():
    # checks command line arguments
    if len(sys.argv) != 3:
        print("Usage: python load-json.py <json_file_name> <port_number>")
        sys.exit(1)
        
    json_file = sys.argv[1]
    port_number = sys.argv[2]


        # Validate port_number number
    if not port_number.isdigit():
        print("Error: Port number must be an integer.")
        sys.exit(1)
    
    create_db(json_file, int(port_number))




if __name__ == "__main__":
  main()

