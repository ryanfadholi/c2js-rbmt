import transrules as rules
import re 

class POSTagger:

    def __init__(self):
        self.rules = rules.TranslationHelper()

        self.rule_ws_incl = re.compile(r"(\s+)")
        self.rule_ws = re.compile(r"\s+")
        self.rule_alphanum = re.compile(r"\w+")
        pass

    def extract_special_tokens(self, string):
        """
        Splits and returns valid symbol tokens from a string of symbol characters.
        Unknown symbols will be treated as single-character token.
        
        For example, "++);" would return ["++", ")", ";"]
        """
        result = []
        while len(string) > 0:

            #If the string starts with a sequence of known token, e.g ++, +=, cut as needed.
            #Otherwise treat the first character as a standalone symbol.
            for token in self.rules.multichar_symbol_tokens:
                if(string.startswith(token)):
                    cut_len = len(token)
                    break
            else:
                cut_len = 1
            
            next_token, string = string[:cut_len], string[cut_len:]
            result.append(next_token)

        return result

    def merge_tokens(self, tokens):
        #TODO: Add string and comment merging mechanism.
        if tokens[0] == "//":
            return [tokens[0], "".join(tokens[1:])]
        elif tokens[0] == "/*":
            return [tokens[0], "".join(tokens[1:-1]), tokens[-1]]
        else:
            return tokens

    def tokenize(self, text, preserve_whitespace=False):
        """
        Tokenizes a given string into strings of whitespace, alphanumeric, and valid symbol tokens in C.
        If preserve_whitespace is set to True, all whitespaces will be treated as tokens; 
        otherwise whitespaces will be skipped.
        """

        splitter = re.compile(r"(\w+|\s+)")
        
        result = []

        #Filter empty tokens, and loop through it.
        for token in filter(lambda token: len(token) > 0, splitter.split(text)):
            if(self.rule_ws.match(token)):
                if preserve_whitespace:
                    result.append(token)
            elif(self.rule_alphanum.match(token)):
                result.append(token)
            #it's neither alphanumeric or whitespace, assume it's a symbol string.
            else:
                result.extend(self.extract_special_tokens(token))

        return result

    def tag(self, statement):
         #TODO: Add string and comment merging mechanism.
         #TODO: Consider escaped single-quote & double-quote.

        #Check if there is single-quote/double-quote token in the statement.
        quote_exists = '"' in statement or "'" in statement
        #If there's quote in the statement, or it's a comment statement, set as True.
        is_ws_preserved = quote_exists or self.rules.is_singlecomment(statement) or self.rules.is_multicomment(statement)
        
        tokens = self.tokenize(statement, is_ws_preserved)

        if is_ws_preserved:
            tokens = self.merge_tokens(tokens)

        return tokens
        

if __name__ == "__main__":
    #When run, run c2js instead
    import c2js