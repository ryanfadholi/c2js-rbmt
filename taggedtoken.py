class TaggedToken:
    def __init__(self, token, tag):
        self.token = token        
        self.tag = tag

    def __str__(self):
        return f"{self.tag} - {repr(self.token)}"