import copy

no_carryover = ["include-library"]

class TaggedStatement:
    def __init__(self, tokens = [], statement_type = "None"):
        #Ensure copy
        self.carryover = True
        self.tokens = copy.copy(tokens)
        self._type = statement_type

    def __len__(self):
        return len(self.tokens)

    def __iter__(self):
        return iter(self.tokens)
        
    def __str__(self):
        result = ""
        result += f"Statement Type: {self._type}\n"
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

    @property
    def tag(self):
        return self._type

    @tag.setter
    def tag(self, value):
        self._type = value

        if value in no_carryover:
            self.carryover = False

    def findall(self, *args):
        result = {}

        for item in args:
            print(item)
            result[item] = []

        for pos, token in enumerate(self.tokens):
            if token.tag in result:
                result[token.tag].append(pos)

        if len(args) == 1:
            item = args[0]
            return result[item]
        else:
            return tuple(result[item] for item in args)
