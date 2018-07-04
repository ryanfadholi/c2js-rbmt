import tokendicts as tokens

class StructuralLexicalTransfer:
    def __init__(self):
        pass

    def trace(self, pattern, statement):
        """Matches statement to the given pattern."""
        for ptoken, stoken in zip(pattern, statement):
            if ptoken is None:
                pass
            else:
                if ptoken != stoken:
                    return False
            
        return True

    def identify(self, statement):

        tags = list(map(lambda token: token.tag, statement))
        preprocessor_pattern = [tokens.preprocessor, tokens.tag_include_kw] 
        if self.trace(preprocessor_pattern, tags):
            statement.statement_type = "include"
        else:
            statement.statement_type = "unknown"

        return statement


        