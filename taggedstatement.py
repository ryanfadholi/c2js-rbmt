import copy

class TaggedStatement:
    def __init__(self, tagged_tokens = []):
        #Ensure copy
        self.tagged_tokens = copy.copy(tagged_tokens)
        self.statement_type = "None"

    def __len__(self):
        return len(self.tagged_tokens)

    def __str__(self):
        result = ""
        result += f"Statement Type: {self.statement_type}\n"
        result += "Tokens: "

        comma_flag = False
        for token in self.tagged_tokens:
            if comma_flag:
                result  += ", "
            result += str(token)
            comma_flag = True
            
        return result

