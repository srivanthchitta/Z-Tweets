import sys
import os
import platform
from luis import compose_tweet, top_users, connect_to_mongo
from joao import list_top_tweets
from srivanth import search_tweets
from juan import search_users

def first_screen():
   """
   Welcome page for Z
   Asks users to exit, sign up, or log in
   return: (str) command choice
   """
   print("--------------------------------------------------")
   print("------------------Welcome to Z--------------------")
   print("--------------------------------------------------")

   return

def print_menu():
    """
    prints the programs 'Main Menu'
    contains a list of 'tasks' users are able to perform
    return: (str) users requested command
    """
    print("\n--------------------------------------------------")
    print(f"------------------Main Menu----------------------")
    print("--------------------------------------------------")
    print(f"Hi! Select any of the following options:")
    
    # repeatedly prompts user for a valid task
    while True:
        print("0) Exit")
        print("1) Search for tweets")
        print("2) Search for users")
        print("3) List top tweets")
        print("4) List top users")
        print("5) Compose a tweet")
        command = input("Enter your choice: ")
        if command in ['0','1','2','3','4','5']:
            return command
        else:
            print("\nInvalid choice. Please try again")

def clear_screen():
    """
    clears the screen before program begins
    """
    system_name = platform.system().lower()
    if system_name == 'windows':
        os.system('cls')
    else:
        os.system('clear')

def main():
    # clears screen to initiate program
    clear_screen()

    # ensures db file is provided
    if len(sys.argv) != 2:
        print("Please type the following into the terminal: python3 main.py <port_number>")
        sys.exit(1)

    # retieves db file from command line
    port = int(sys.argv[1])

    # connects to sql database
    db = connect_to_mongo(port)
    collection = db["tweets"]

    first_screen()

    while True:

        # prints the menu
        command = print_menu()

        if command == '0':
            # user is logged out and taken back to home page
            print("We hope to see you again soon!")
            break
        elif command == '1': # users asks to search tweets
            search_tweets(collection)
        elif command == '2': # users asks to search users
            search_users(collection)
        elif command == '3': # users asks to make a tweet
            list_top_tweets(collection)
        elif command == '4': # users asks to list his followers
            top_users(collection)
        elif command == '5':
            compose_tweet(collection)

    print("\nThanks for using 'Z'!\n")


if __name__ == "__main__":
   main()
