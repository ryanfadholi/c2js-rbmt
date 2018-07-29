class TaggedToken:
    def __init__(self, token, tag):
        self.token = token        
        self.tag = tag

        no_bspacing = [")", ";", ".", ",", "[", "]", "*/"]
        no_fspacing = ["(", ".", "//", "/*", "{", "}", "log", "format"]
        
        self.bspacing = False if token in no_bspacing else True
        self.fspacing = False if token in no_fspacing else True

    def __str__(self):
        return f"{self.tag} - {repr(self.token)}"
