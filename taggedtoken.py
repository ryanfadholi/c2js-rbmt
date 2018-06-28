class TaggedToken:
    def __init__(self, tag, token):
        self.tag = tag
        self.token = token

    def __str__(self):
        return f"{self.tag} - {repr(self.token)}"