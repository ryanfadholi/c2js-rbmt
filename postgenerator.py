class PostGenerator:
    def __init__(self, filepath):
        self.filepath = filepath

    def join(self, tokens):
        result = ""

        fspacing = False
        for token in tokens:
            if fspacing and token.bspacing:
                result += " "
            result += token.token
            fspacing = token.fspacing
        
        return result

    def write(self, statements):
        with open(self.filepath, "w") as file_output:
            for statement in statements:
                line = self.join(statement.tokens)
                if line: #Only writes if the ine is not empty
                    file_output.write(line)
                    file_output.write("\n")
        