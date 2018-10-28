NO_BACKSPACING_TOKEN = [";", ")", "}", ":", ".", ",", "[", "]", "*/", "++", "--"]
NO_FRONTSPACING_TOKEN = ["(", ".", "//", "/*", "{", "}", "[", "write", "Number", "log", "format", "question", "if", "for", "while"]        

class TaggedToken:
    def __init__(self, token, tag):
        self.token = token        
        self.tag = tag
        
        self.bspacing = False if token in NO_BACKSPACING_TOKEN else True
        self.fspacing = False if token in NO_FRONTSPACING_TOKEN else True

    def __repr__(self):
        return f"{repr(self.token)} - {self.tag}"

    def __str__(self):
        return f"{repr(self.token)} - {self.tag}"
