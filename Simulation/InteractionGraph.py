class InteractionGraph:
    def __init__(self):
        self.posts = set()
        self.users = set()
        self.likes = dict()  # key: post, value: set of users who liked the post
        self.comments = dict()  # key: post, value: set of users who commented on the post
    
    def add_post(self, post):
        self.posts.add(post)
        self.views[post] = set()
        self.likes[post] = set()
        self.comments[post] = set()

    def add_user(self, user):
        self.users.add(user)
