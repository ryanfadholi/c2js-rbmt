NO_BACKSPACING_TOKEN = [")", "}", ";", ".", ",", "[", "]", "*/", "++", "--"]
NO_FRONTSPACING_TOKEN = ["(", ".", "//", "/*", "{", "}", "log", "format", "question", "if", "for", "while"]        

class TaggedToken:
    def __init__(self, token, tag):
        self.token = token        
        self.tag = tag
        
        self.bspacing = False if token in NO_BACKSPACING_TOKEN else True
        self.fspacing = False if token in NO_FRONTSPACING_TOKEN else True

    def __repr__(self):
        return f"{self.tag} - {repr(self.token)}"

    def __str__(self):
        return f"{self.tag} - {repr(self.token)}"
