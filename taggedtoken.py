class TaggedToken:
    def __init__(self, tag, token):
        
        self.tag = tag
        self.token = token

    def __contains__(self, item):
        pass