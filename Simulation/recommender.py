import random
import math
import json
from models.user import User

DATA_USERS_FOLDER = "data/users"
ROOT_USER_ID = 1  # Default root user ID for recommendations

# Connection Limits
MAX_MUTUALS = 1000  # limit mutuals connections to avoid explosion when searching paths
MAX_FOLLOWERS = 200  # limit followers connections to avoid explosion when searching paths
MAX_FOLLOWING = 200  # limit following connections to avoid explosion when searching paths

class Recommender:
    def __init__(self, root_user, folder=DATA_USERS_FOLDER):
        self.folder = folder
        self.users = {}
        self.root_user = self.load_user(root_user)
        

    def load_user(self, user_id):
        # Return cached user if already loaded
        if user_id in self.users:
            return self.users[user_id]

        # load from file
        data = User.load_user_data(user_id, folder=self.folder)
        user_obj = User(user_id)
        user_obj.from_dict(data)

        # Store in cache
        self.users[user_id] = user_obj

        return user_obj
    

    def create_recommendation_set(self, max_hops=3, alpha=0.8):
        """
        Discover recommendations based on a user's social graph.
        Stores ALL unique paths and produces a final score:
            final_score = best_path_score + alpha * log(1 + num_paths)
        Includes weighted edges: follower > following, mutual strongest.
        """
        all_paths = {}

        # BFS queue: (current_id, hop_count, path_list)
        queue = [(self.root_user.user_id, 0, [("root", self.root_user.user_id)])]
        visited = set()

        print("Running BFS to explore connections...")
        while queue:
            current_id, hop, path = queue.pop(0)

            if hop > max_hops: # exceeded max hops
                continue

            if current_id in visited and hop != 0: # already visited (except root)
                continue

            visited.add(current_id)
            user_data = self.load_user(current_id)

            neighbors = []
            mutuals_found = 0
            followers_found = 0
            following_found = 0

            # Followers → inbound relation
            for f in user_data.followers:
                if current_id in self.load_user(f).followers:  
                    if mutuals_found < MAX_MUTUALS / (hop + 1): # limit mutuals
                        mutuals_found += 1
                        neighbors.append(("mutual", f))   # both follow each other
                else:
                    if followers_found < MAX_FOLLOWERS / (hop + 1): # limit followers
                        followers_found += 1
                        neighbors.append(("follower", f))

            # Following → outbound relation
            for f in user_data.following:
                if current_id in self.load_user(f).following:
                    pass
                    # neighbors.append(("mutual", f))
                else:
                    if following_found < MAX_FOLLOWING / (hop + 1): # limit following
                        following_found += 1
                        neighbors.append(("following", f))

            # Explore neighbors
            for relation, neighbor_id in neighbors:
                new_path = path + [(relation, neighbor_id)]

                if (
                    neighbor_id != self.root_user.user_id
                    and neighbor_id not in self.root_user.following
                ):
                    all_paths.setdefault(neighbor_id, [])
                    if new_path not in all_paths[neighbor_id]:
                        all_paths[neighbor_id].append(new_path)


                queue.append((neighbor_id, hop + 1, new_path))
        # End of BFS loop

        EDGE_WEIGHTS = {
            "root": 1.0,
            "following": 0.75,
            "follower": 0.85,
            "mutual": 0.95
        }

        def path_weight(path):
            ''' Inside function to calculate weight of a given path '''
            hop_count = len(path) - 1
            if hop_count == 0:
                return 0

            prev_id = path[0][1] # start with root user
            weight = 1.0
            for relation, curr_id in path[1:]:
                weight *= self.calculate_similarity_weight(prev_id, curr_id) ## apply similarity weight
                weight *= EDGE_WEIGHTS.get(relation, 1.0) # apply edge type weight
                prev_id = curr_id

            weight = weight * weight # favor stronger connections more heavily
            return weight

        # Calculate recommendation scores
        recommendations = {}
        print("Calculating recommendation scores...")
        for user_id, paths in all_paths.items():
            path_scores = [path_weight(p) for p in paths]

            best_score = max(path_scores)
            num_paths = len(paths)

            final_score = best_score * math.log(1 + num_paths)

            recommendations[user_id] = {
                "paths": paths,
                "best_path": paths[path_scores.index(best_score)],
                "num_paths": num_paths,
                "best_path_score": best_score,
                "final_score": final_score
            }

        # Sort final output
        sorted_recommendations = dict(
            sorted(
                recommendations.items(),
                key=lambda x: x[1]["final_score"],
                reverse=True,
            )
        )

        return sorted_recommendations

    
    def custom_similarity(self, a, b):
        """
        Computes a similarity score between 0 and 1.
        a and b must be same-length lists of values in [0,1].
        Similarity = mean( (1 - |a_i - b_i|)^2 )
        1 = identical, 0 = completely different
        """
        if len(a) != len(b):
            raise ValueError("Attribute vectors must be same length")
        
        sim_sum = 0.0
        for i in range(len(a)):
            diff = 1 - abs(a[i] - b[i])
            sim_sum += diff * diff

        return sim_sum / len(a)

        
    def calculate_similarity_weight(self, user_id, follower_id):
        """
        Computes a final edge weight between 0 and 1.
        Combines similarity and normalized fame.
        """
        follower = self.load_user(follower_id)
        user = self.load_user(user_id)

        # Similarity in [0,1]
        similarity = self.custom_similarity(user.attributes, follower.attributes)

        # Clamp to [0,1] just in case floating point drift occurs
        similarity = max(0.0, min(1.0, similarity))

        return similarity

def save_best_paths_to_json(recommendations, filename="best_paths.json"):
    """
    Save only the best path for each recommended user to a JSON file.
    """
    best_paths_data = {}
    for user_id, data in recommendations.items():
        best_paths_data[user_id] = {
            "final_score": data["final_score"],
            "best_path_score": data["best_path_score"],
            "num_paths": data["num_paths"],
            "best_path": data["best_path"]
        }

    with open(filename, "w") as f:
        json.dump(best_paths_data, f, indent=4)
    print(f"Best paths saved to {filename}")





if __name__ == "__main__":
    random.seed(0)  # For reproducibility
    recommender = Recommender(root_user=ROOT_USER_ID, folder=DATA_USERS_FOLDER)
    potential_recommendations = recommender.create_recommendation_set(max_hops=3)
    ## print total amount of recommendations
    print(f"Total recommendations found: {len(potential_recommendations)}")
    ## Print total amount of paths explored
    total_paths = sum([data["num_paths"] for data in potential_recommendations.values()])
    print(f"Total unique paths explored: {total_paths}")

    ## Top 10 recommendations
    print("Top 10 Recommendations:")
    for i, (user_id, data) in enumerate(potential_recommendations.items()):
        if i >= 10:
            break
        print(f"User {user_id}: Final Score = {data['final_score']:.4f}, Best Path Score = {data['best_path_score']:.4f}, Num Paths = {data['num_paths']}")

    save_best_paths_to_json(potential_recommendations, "data/recommendations/user" + str(ROOT_USER_ID) + "_recommendation.json")

