import re
import tokens as tkn

from taggedtoken import TaggedToken
from taggedstatement import TaggedStatement

RULE_ALPHANUM = re.compile(r"^\w+$")
RULE_DIGIT = re.compile(r"^\d+$")
RULE_WHITESPACE = re.compile(r"^\s+$")

class POSTagger:

    def _break_apart(self, string):
        """
        Splits and returns valid symbol tokens from a string of symbol characters.
        Unknown symbols will be treated as single-character token.

        For example, "++);" would return ["++", ")", ";"]
        """
        result = []
        while len(string) > 0:

            #If the string starts with a sequence of known token, e.g ++, +=, cut as needed.
            #Otherwise treat the first character as a standalone symbol.
            for token in tkn.multichar_symbol:
                if(string.startswith(token)):
                    cut_len = len(token)
                    break
            else:
                cut_len = 1

            next_token, string = string[:cut_len], string[cut_len:]
            result.append(next_token)

        return result

    def _floatify(self, tokens):
        """
        Merges every [digit, dot, digit] or [digit, dot] token sequence into one floating-point token.
        """
        index = 0
        last_check = len(tokens) - 1 #Check until there is at least one remaining tokens.
        result = []

        #Check until the last two tokens. (Checking further than this will cause index error :) )
        while index < last_check:
            #Merge dots of floating-point numbers (e.g "3.", "4.14")
            if tokens[index+1] == "." and RULE_DIGIT.match(tokens[index]):
                #At this point, there's a number followed by a dot.
                to_join = 2 #Number of token to join
                if (index+2 < len(tokens)) and RULE_DIGIT.match(tokens[index+2]):
                    #If the dot is in turn followed by a digit, assume that it's the decimal part of the float
                    to_join = 3

                result.append("".join(tokens[index:index+to_join]))
                index += to_join
            #Merge dots of library names in include statements.
            elif tokens[0] == "#" and tokens[index+1] == ".":
                result.append("".join(tokens[index:index+3]))
                index += 3                
            else:
                result.append(tokens[index])
                index += 1

        #After the checking is done, append the remaining last three tokens.
        while index < len(tokens):
            result.append(tokens[index])
            index += 1

        return result

    def _has_dot(self, tokens):
        """Returns True for any dot in tokens"""
        return '.' in tokens

    def _has_quote(self, tokens):
        """Returns True for any single or double quote in tokens"""
        return '"' in tokens or "'" in tokens

    def _match(self, token):
        """Determines the tag of the respective token (according to the token dictionary constants)"""
        token_dicts = [tkn.arithmetic_operator, tkn.bitwise_operator, tkn.relational_operator, 
            tkn.compound_assignment_operator, tkn.logical_operator, tkn.misc_operator, tkn.comments, 
            tkn.conditionals, tkn.datatypes, tkn.loops, tkn.special_functions, tkn.keywords ]

        for token_dict in token_dicts:
            for key, value in token_dict.items():
                if token == value:
                    return key
        
        return "unknown"

    def _measure_string(self, text):
        """
        Returns an index in which the first string in the text ends. Returns -1 if no string are ending.
        (The text parameter must start with either single or double quotes)
        """
        
        #Do a sanity check; is the text really a string?
        if(not self._starts_with(tkn.string_identifiers, text)):
            print(f"ERROR! The text ({text}) is not a string, but skip_text() is called on it.")
            return -1

        #What we're looking for is either single or double token; check the first character to determine which.
        cur_string_delimiter = text[0]
        found = False
        idx = -1

        #Start from one to account for the first character (the first single/double quote)
        for idx, char in enumerate(text[1:], 1):
            #If the current token is the same as the one starting the string
            #(either single or double quote)
            if char == cur_string_delimiter:
                #If the last character in current string is backslash, it means
                #that the delimiter is escaped; continue.
                if text[idx-1] == "\\":
                    pass
                #else it means that the current string is ending. Break from loop
                else:
                    found = True
                    break
        
        return idx if found else -1

    def _rebuild(self, tokens):
        """
        Accepts these as parameter:
        1. List of tokenized single or multi-line comment.
        2. List of tokenized statement containing single or double quotes.
        3. List of tokenized statement containing dots.

        Returns the same list, but with some parts merged (when needed)
        """
        if self._starts_with(tkn.single_comment, tokens):
            return [tokens[0], "".join(tokens[1:])] 
        elif self._starts_with(tkn.multi_comment, tokens):
            return [tokens[0], "".join(tokens[1:-1]), tokens[-1]]
        else:
            #If it's not a comment statement, assume it's a statement containing a string or dots.
            if self._has_quote(tokens): 
                tokens = self._stringify(tokens)    
            
            if self._has_dot(tokens):
                tokens = self._floatify(tokens)

            return tokens

    def _split(self, text, preserve_whitespace=False):
        """
        Splits a given string into strings of whitespace, alphanumeric, and valid symbol tokens in C.
        If preserve_whitespace is set to True, all whitespaces will be treated as tokens; 
        otherwise whitespaces will be skipped.
        """

        splitter = re.compile(r"(\w+|\s+)")
        
        result = []

        #Filter empty tokens, and loop through it.
        for token in filter(lambda token: len(token) > 0, splitter.split(text)):
            if RULE_WHITESPACE.match(token):
                if preserve_whitespace:
                    result.append(token)
            elif RULE_ALPHANUM.match(token):
                result.append(token)
            #it's neither alphanumeric or whitespace, assume it's a symbol string.
            else:
                result.extend(self._break_apart(token))

        return result

    def _starts_with(self, tokens, statement):
        """
        Returns True if the list of A template function to check if a statement (either as a string or a list of string)
        starts with the tokens variable (tokens might be a dict, list, or string)
        """
        if isinstance(statement, list):
            start_token = None
            if statement:
                start_token = statement[0]
            return start_token in tokens
        elif isinstance(statement, str):
            return True in (statement.startswith(token) for token in tokens)
        else:
            raise ValueError("Statement is neither a list or string object")

    def _stringify(self, tokens):
        """
        Merges every tokens between single or double quotes (including the quotes) into one. 
        Leave the rest as it is, except that whitespaces outside quotes is removed.
        
        Will handle escaped quotes correctly, but fails silently if there is non-even number of quotes 
        (the last quote and all quote afterwards will be dumped)
        """

        limit = -1
        result_tokens = []

        for idx, token in enumerate(tokens):
            #Do nothing if the token is inside of a string's range, OR it's only whitespace.
            if idx < limit or RULE_WHITESPACE.match(token):
                pass
            elif token == "'" or token == '"':
                str_length = self._measure_string(tokens[idx:])
                limit = idx + str_length + 1 #Extra 1 is the offset of single/double quotes
                result_tokens.append("".join(tokens[idx:limit]))
            else:
                result_tokens.append(token)
                    
        return result_tokens

    def tokenize(self, statement):
        """
        Tokenizes C statement given as parameter into tagging-ready tokens.
        """

        #If there's quote in the statement, or it's a comment statement, set as True.
        is_ws_sensitive = (self._has_quote(statement) or 
                            self._starts_with([tkn.single_comment, tkn.multi_comment], statement))        
        tokens = self._split(statement, preserve_whitespace=is_ws_sensitive)

        if is_ws_sensitive or self._has_dot(statement):
            tokens = self._rebuild(tokens)

        return tokens

    def tag(self, statement):
        """Tokenizes and tags each token from the statement. Returns a TaggedStatement object"""

        id_int = re.compile(r"^\d+$")
        id_float = re.compile(r"^\d+\.(\d+)?$")
        id_var = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
        id_char = re.compile(r"^'.*'$", re.DOTALL)
        id_string = re.compile(r'^".*"$', re.DOTALL)

        tokens = self.tokenize(statement)
        
        #This only matches known tokens
        matched_tokens = TaggedStatement(list(map(lambda x: TaggedToken(x, self._match(x)), tokens)))

        #While this match the rest ("dynamic" tokens)
        for idx, token in enumerate(matched_tokens):
            if token.tag == "unknown":
                token_str = token.token
                #Match library names (stdio.h, conio.h)
                if token_str.lower().endswith(".h"):
                    token.tag = tkn.tag_name_preproc
                #Match integers (1234, 5454, 5)
                elif id_int.match(token_str):
                    token.tag = tkn.tag_val_int
                #Match floating-point (1.1, 3.14, 2.)
                elif id_float.match(token_str):
                    token.tag = tkn.tag_val_float
                #Match variable names (x, result, _hero9, y2)
                elif id_var.match(token_str):
                    token.tag = tkn.tag_name_var
                #Match characters ('a', 'b')
                elif id_char.match(token_str):
                    token.tag = tkn.tag_val_char
                #Match strings ("abc", "def")
                elif id_string.match(token_str):
                    token.tag = tkn.tag_val_string

                #Match comment string (comments doesn't have any pattern, match based on position of comment tags)
                if idx == 1:
                    prev_token = matched_tokens[0].tag
                    if prev_token == tkn.tag_single_comment or prev_token == tkn.tag_multi_comment:
                        token.tag = "comment"
        
        return matched_tokens

    