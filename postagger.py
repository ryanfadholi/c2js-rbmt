import transrules as rules
import re 

class POSTagger:

    #TODO: Design decision: split per special character and merge as needed, or split chunks at once and split when needed?
    #First option is good when special characters are lined up, e.g ("% but it costs more computation as it splits everything.
    #Second option need less computation, but need to mitigate cases where special cases are lined up. 
    #TODO: Add string and comment merging mechanism.

    def __init__(self):
        self.rule_ws_incl = re.compile(r"(\s+)")
        self.rule_ws = re.compile(r"\s+")
        self.rule_alphanum = re.compile(r"\w+")
        pass

    def extract_special_tokens(self, string):
        """
        Splits and returns valid tokens from a string of symbol characters.
        Unknown symbols will be treated as single-character token.
        
        For example, "++);" would return ["++", ")", ";"]
        """
        result = []
        while len(string) > 0:

            for token in rules.multichar_symbol_token:
                if(string.startswith(token)):
                    cut_len = len(token)
                    break
            else:
                cut_len = 1
            
            next_token, string = string[:cut_len], string[cut_len:]
            result.append(next_token)

        return result

    def tokenize(self, text, preserve_whitespace=False):
        #TODO: Split the tokens further into whitespaces and non whitespaces
        splitter = re.compile(r"(\w+|\s+)")    
        non_ws = re.compile(r"\S+")
        #Filter empty tokens.
        # for token in splitter
        result = []

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

    def tag(self, text):
        if True in (text.startswith(token) for token in rules.comments):
            pass

if __name__ == "__main__":
    #When run, run c2js instead
    import c2js