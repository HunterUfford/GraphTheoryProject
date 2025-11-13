
class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.following = set()
        self.followers = set()

    def follow(self, other_user):
        self.following.add(other_user)
        other_user.followers.add(self)




    