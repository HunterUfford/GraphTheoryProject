
class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.following = set()
        self.followers = set()

    def follow(self, other_user):
        self.following.add(other_user)
        other_user.followers.add(self)

    def unfollow(self, other_user):
        self.following.discard(other_user)
        other_user.followers.discard(self)

    def get_followers(self):
        return self.followers
    
    def get_following(self):
        return self.following
    
    def is_mutual(self, other_user):
        return other_user in self.following and self in other_user.following
    


if __name__ == "__main__":
    user1 = User(1, "Alice")
    user2 = User(2, "Bob")
    
    user1.follow(user2)
    print(f"{user1.name} is following {user2.name}: {user2 in user1.get_following()}")
    print(f"{user2.name} has followers: {[user.name for user in user2.get_followers()]}")
    
    user2.follow(user1)
    print(f"Are {user1.name} and {user2.name} mutual followers? {user1.is_mutual(user2)}")

    