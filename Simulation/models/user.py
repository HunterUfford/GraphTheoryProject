import random
import os
import json

class User:
    def __init__(self, user_id, name=None):
        self.user_id = user_id
        self.name = name or f"User {user_id}"
        self.attributes = []
        self.cliques = []
        self.followers = set()
        self.following = set()
        self.num_followers = 0
        self.num_following = 0

    def get_fame(self):
        ''' Unused function to get the fame of the user based on number of followers 
         We were going to use this in recommendation scoring but decided to use the number of paths instead '''
        return self.num_followers
    
    def get_distance(self, other_user):
        ''' Unused function to compute Euclidean distance between two users based on attributes '''
        if len(self.attributes) != len(other_user.attributes):
            raise ValueError("Users must have the same number of attributes to compute distance.")
        return sum((a - b) ** 2 for a, b in zip(self.attributes, other_user.attributes)) ** 0.5
    

    def add_follower(self, follower_id):
        ''' Add a user ID to the followers set '''
        self.followers.add(follower_id)
        self.num_followers = len(self.followers)

    def add_following(self, following_id):
        ''' Add a user ID to the following set '''
        self.following.add(following_id)
        self.num_following = len(self.following)


    def seed_attributes(self, num_attributes=5):
        ''' Seed user attributes with random values between 0 and 1 '''
        for i in range(num_attributes):
            random_value = random.random()
            self.attributes.append(random_value)

    def add_clique(self, clique_id):
        ''' Add a clique ID to the user's list of cliques '''
        self.cliques.append(clique_id)

    def shift_attributes(self, target_attributes, shift_amount=0.8, shift_chance=0.8):
        ''' Shift attributes towards target_attributes by shift_amount with probability shift_chance 
            This function is used to make clique members more similar '''
        for i, attr in enumerate(target_attributes):
            if random.random() < shift_chance:
                self.attributes[i] = attr * shift_amount + self.attributes[i] * (1 - shift_amount)


    def to_dict(self): 
        ''' Convert user data to a dictionary for JSON file '''
        return {
            "user_id": self.user_id,
            "name": self.name,
            "attributes": self.attributes,
            "cliques": self.cliques,
            "followers": list(self.followers),
            "following": list(self.following),
            "num_followers": self.num_followers,
            "num_following": self.num_following
        }
    
    def from_dict(self, data):
        ''' Load user data from a dictionary, used when loading from JSON '''
        self.user_id = data["user_id"]
        self.name = data["name"]
        self.attributes = data["attributes"]
        self.cliques = data["cliques"]
        self.followers = set(data["followers"])
        self.following = set(data["following"])
        self.num_followers = len(self.followers)
        self.num_following = len(self.following)

    def change_name(self, new_name):
        ''' Change the users name'''
        self.name = new_name

    @staticmethod
    def load_user_data(user_id, folder="data/users"):
        ''' Used to load a users data from a JSON file'''
        path = os.path.join(folder, f"user_{user_id}.json")
        with open(path, "r") as f:
            return json.load(f)