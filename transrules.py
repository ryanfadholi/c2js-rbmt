import tokendicts as tokens

#TODO: When all rules are in dictionary, delete unnecessary instance checks.

class TranslationHelper:

    def __init__(self):
        self.multichar_symbol_tokens = tokens.multichar_symbol

    def findfirst(self, text, tokens):
        """
        Find the first instance of any token from the tokens list on the text string. 
        Returns -1 when there is no instance of any token in the string.
        """

        if isinstance(tokens, dict):
            findall = [text.find(token) for key, token in tokens.items()]
        elif isinstance(tokens, list):
            findall = [text.find(token) for token in tokens]
        
        found = list(filter(lambda pos: pos > -1, findall))

        return min(found) if len(found) > 0 else -1

    findcomment = lambda self, text: self.findfirst(text, tokens.comments)

    def stmt_validate(self, text, tokens):
        """
        A template function to check if text starts with the tokens (if it's string),
        or if the text starts with any token from the tokens (if it's list).
        """
        if isinstance(tokens, dict):
            return True in (text.startswith(token) for key, token in tokens.items())
        elif isinstance(tokens, list):
            return True in (text.startswith(token) for token in tokens)
        elif isinstance(tokens, str):
            return text.startswith(tokens)
        else:
            return False
        
    #Functions to check the type of a statement.
    is_block_end = lambda self, text: self.stmt_validate(text, tokens.block_end)
    is_conditional = lambda self, text: self.stmt_validate(text, tokens.conditionals)
    is_declaration = lambda self, text: self.stmt_validate(text, tokens.datatypes)
    is_include = lambda self, text: self.stmt_validate(text, tokens.include)
    is_loop = lambda self, text: self.stmt_validate(text, tokens.loops)
    is_multicomment = lambda self, text: self.stmt_validate(text, tokens.multi_comment)
    is_singlecomment = lambda self, text: self.stmt_validate(text, tokens.single_comment)