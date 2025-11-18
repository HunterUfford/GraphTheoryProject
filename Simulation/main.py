# main.py
from models.social_graph import SocialGraph

DATA_USERS_FOLDER = "data/users"

def create_simulation():
    sg = SocialGraph()
    
    # Step 1: generate users
    sg.generate_users(num_users=500)
    sg.users[0].change_name("Hunter")
    sg.users[1].change_name("Madison")
    sg.users[2].change_name("Kefir")
    # Step 2: generate realistic connections using BA model
    sg.generate_connections(avg_connections=5)

    # Step 3: add mutual friend/family cliques
    sg.add_friend_cliques(num_cliques=20, min_size=3, max_size=8, mutual_prob=0.9) ## Tight cliques
    sg.add_friend_cliques(num_cliques=20, min_size=8, max_size=20, mutual_prob=0.5) ## Looser cliques

    # Step 4: save each user individually
    sg.save_users_individual(folder=DATA_USERS_FOLDER)
    print("Simulation created and individual users saved.")

if __name__ == "__main__":
    create_simulation()
    
    # Example: explore followers lazily
    SocialGraph.explore_followers(user_id=0, max_hops=1, folder=DATA_USERS_FOLDER)
