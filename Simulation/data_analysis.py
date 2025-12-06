import os
import json

DATA_USERS_FOLDER = "data/users"

def load_all_users(folder=DATA_USERS_FOLDER):
    ''' Load all user JSON files from the specified folder and return a dictionary of user data '''
    users = {}
    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            path = os.path.join(folder, filename)
            with open(path, "r") as f:
                data = json.load(f)
                users[data["user_id"]] = data
    return users

def compute_statistics(users):
    total_followers = 0
    total_mutuals = 0
    n = len(users)

    # Handle case with no users
    if n == 0:
        print("No users found.")
        return 0, 0, None, 0
    
    max_followers = -1

    for user_id, data in users.items():
        followers = set(data["followers"])
        following = set(data["following"])
        total_followers += len(followers)
        
        # Mutual connections: intersection of followers and following
        mutuals = followers & following
        total_mutuals += len(mutuals)

        # Track user with most followers
        if len(followers) > max_followers:
            max_followers = len(followers)
            top_user_name = data["name"]

    avg_followers = total_followers / n
    avg_mutuals = total_mutuals / n
    return avg_followers, avg_mutuals, top_user_name, max_followers

if __name__ == "__main__":
    users = load_all_users()
    avg_followers, avg_mutuals, top_user, max_followers = compute_statistics(users)
    
    # print statistics
    print(f"Total users: {len(users)}")
    print(f"Average followers per user: {avg_followers:.2f}")
    print(f"Average mutual connections per user: {avg_mutuals:.2f}")
    print(f"User with most followers: {top_user} ({max_followers} followers)")
