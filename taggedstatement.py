class TaggedStatement:
    
    def __init__(self, tokens=None, statement_type="None"):
        if tokens is None:
            tokens = []

        #Ensure copy
        self.carryover = True
        self.tokens = tokens
        self.tag = statement_type

    def __len__(self):
        return len(self.tokens)

    def __iter__(self):
        return iter(self.tokens)

    def __str__(self):
        result = ""
        result += f"Statement Type: {self.tag}\n"
        result += "Tokens: "

        comma_flag = False
        for token in self.tokens:
            if comma_flag:
                result  += ", "
            result += str(token)
            comma_flag = True

        return result

    def __getitem__(self, key):
        return self.tokens.__getitem__(key)

    def __setitem__(self, key, value):
        self.tokens.__setitem__(key, value)

    def find_all(self, *args):
        """
        Returns a list of every argument occurrences if there is only one argument,
        Returns a tuple of lists which containts every arguments occurrences otherwise
        (every argument has their own occurrence list)
        """

        result = {}

        for item in args:
            result[item] = []

        for pos, token in enumerate(self.tokens):
            if token.tag in result:
                result[token.tag].append(pos)

        if len(args) == 1:
            item = args[0]
            return result[item]
        else:
            return tuple(result[item] for item in args)
