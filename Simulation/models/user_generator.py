import networkx as nx
import random
import os
import json
from user import User

class UserGenerator:
    ''' Class to generate users, their attributes, connections, and cliques'''

    def __init__(self):
        self.users = {} # Dictionary of all users
        self.curr_clique_id = 0 # Keeps track of clique IDs


    def generate_users(self, num_users, num_attributes=5):
        ''' Add users to the users dictionary, generate user objects and seeds their attributes '''
        for i in range(num_users):
            self.users[i] = User(i)
            self.users[i].seed_attributes(num_attributes=num_attributes)

    def generate_connections(self, avg_connections=3):
        ''' Generate connections (followers and following) using barabasi albert method from netwrokx '''
        ba_graph = nx.barabasi_albert_graph(len(self.users), avg_connections)
        # BA graph generates undirected edges, so we need to convert to directed with some randomness
        for u, v in ba_graph.edges():
            rand_num = random.random()
            if rand_num < 0.05: # 5% chance of mutual connection, low chance because cliques will add more
                self.create_mutual_connection(self.users[u], self.users[v])
            else: # 95% chance of one-way connection
                self.create_follower_connection(self.users[v], self.users[u])
                
    def add_friend_cliques(self, num_attributes, num_cliques=20, min_size=3, max_size=8, mutual_prob=0.8, fail_prob=0.1, attribute_shift=0.8, attribute_shift_chance=0.8):
        ''' Overcomplex method to add friend/family cliques with mutual connections and attribute shifting 
            num_attributes: number of attributes each user has
            num_cliques: number of cliques to create
            min_size: minimum size of each clique
            max_size: maximum size of each clique
            mutual_prob: probability that a connection between two clique members is mutual
            fail_prob: probability that a connection between two clique members fails to be created, used to add randomness
            attribute_shift: amount to shift attributes towards clique target attributes, between 0 and 1
            attribute_shift_chance: chance to shift each attribute towards clique target attributes, used to add randomness
        '''
        nodes = list(self.users.keys())
        for _ in range(num_cliques): # For each clique
            self.curr_clique_id += 1
            size = random.randint(min_size, max_size) # Random size between min and max for clique
            clique = random.sample(nodes, size) # Randomly sample users for clique
            clique_attributes = [random.random() for _ in range(num_attributes)] # New random target attributes for clique members

            for groupie_a in clique: 
                # Add clique ID to user
                self.users[groupie_a].add_clique(clique_id=self.curr_clique_id)

                # Shift attributes towards clique target
                self.users[groupie_a].shift_attributes(target_attributes=clique_attributes, shift_amount=attribute_shift, shift_chance=attribute_shift_chance)
                for groupie_b in clique:
                    if groupie_a != groupie_b: # For each pair of users in clique
                        if random.random() > fail_prob: # chance to fail adding connection
                            self.create_follower_connection(self.users[groupie_a], self.users[groupie_b])
                            if random.random() < mutual_prob:
                                self.create_mutual_connection(self.users[groupie_a], self.users[groupie_b]) # mutual connection

    def save_users_individual(self, folder="data/users"):
        ''' Save each user as an individual JSON file, uses the to_dict method of User '''
        os.makedirs(folder, exist_ok=True)
        for user_id, user in self.users.items():
            path = os.path.join(folder, f"user_{user_id}.json")
            with open(path, "w") as f:
                json.dump(user.to_dict(), f, indent=4)

    def create_follower_connection(self, user_a, user_b):
        ''' Create a follower connection such that user_a follows user_b '''
        user_a.add_following(user_b.user_id)
        user_b.add_follower(user_a.user_id)

    def create_mutual_connection(self, user_a, user_b):
        ''' Create a mutual connection between user_a and user_b '''
        self.create_follower_connection(user_a, user_b)
        self.create_follower_connection(user_b, user_a)
    
''' End of UserGenerator class '''




if __name__ == "__main__":


    generator = UserGenerator()
    generator.generate_users(num_users=100, num_attributes=2)
    generator.generate_connections(avg_connections=3)
    generator.add_friend_cliques(num_attributes=2, num_cliques=10, min_size=5, max_size=10, mutual_prob=0.8, fail_prob=0.1, attribute_shift=0.9, attribute_shift_chance=0.8)
    generator.save_users_individual(folder="data/users")
