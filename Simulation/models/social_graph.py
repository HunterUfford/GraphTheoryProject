# models/social_graph.py
import networkx as nx
import random
import os
import json
from .user import User

# Class to manage the user/user connections graph
class SocialGraph:
    def __init__(self):
        self.graph = nx.DiGraph() # Uses the networkx directed graph
        self.users = {}

    # Create user objects
    def generate_users(self, num_users):
        for i in range(num_users):
            self.users[i] = User(i)
            self.graph.add_node(i)

    # Generate connections using BA method
    def generate_connections(self, avg_connections=3):
        ba_graph = nx.barabasi_albert_graph(len(self.users), avg_connections)

        for u, v in ba_graph.edges():

            rand_num = random.random()
            if rand_num < 0.05: # 5% chance of mutual connection
                self.graph.add_edge(u, v)
                self.graph.add_edge(v, u)
            elif rand_num < 0.90: # 85% chance of one-way connection
                self.graph.add_edge(v, u)
            else: # 10% chance of other one-way connection
                self.graph.add_edge(u, v)

    # Manually add cliques for more mutual connections/realism
    def add_friend_cliques(self, num_cliques=20, min_size=3, max_size=8, mutual_prob=0.8):
        nodes = list(self.graph.nodes())
        for _ in range(num_cliques):
            size = random.randint(min_size, max_size)
            clique = random.sample(nodes, size)
            for i in clique:
                for j in clique:
                    if i != j:
                        self.graph.add_edge(i, j)
                        if random.random() < mutual_prob:
                            self.graph.add_edge(j, i) # mutual connection

    # Save users to json files
    def save_users_individual(self, folder="data/users"):
        os.makedirs(folder, exist_ok=True)
        for user_id, user in self.users.items():
            user_data = {
                "user_id": user_id,
                "name": user.name,
                "followers": list(self.graph.predecessors(user_id)),
                "following": list(self.graph.successors(user_id))
            }
            path = os.path.join(folder, f"{user_id}.json")
            with open(path, "w") as f:
                json.dump(user_data, f, indent=4)

    # Method to load a single users data
    @staticmethod
    def load_user(user_id, folder="data/users"):
        path = os.path.join(folder, f"{user_id}.json")
        with open(path, "r") as f:
            return json.load(f)

    # Example method of looking through followers
    @staticmethod
    def explore_followers(user_id, max_hops=2, folder="data/users"):
        visited = set()
        queue = [(user_id, 0)]

        while queue:
            current_id, hop = queue.pop(0)
            if current_id in visited or hop > max_hops:
                continue
            visited.add(current_id)
            user_data = SocialGraph.load_user(current_id, folder)
            print(f"User {current_id}, hop {hop}, followers: {user_data['followers']}")
            for follower in user_data["followers"]:
                queue.append((follower, hop + 1))
