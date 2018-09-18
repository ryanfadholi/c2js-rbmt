import itertools
import re

import tokendicts as tokens

#TODO: When everything's said and done, is it better to spread this file to each project that need each individual function instead?

class TranslationHelper:

    def __init__(self):
        #tokendicts redirects
        self.singlecomment_token = tokens.single_comment
        self.multicomment_token = tokens.multi_comment
        self.multicomment_token_end = tokens.multi_comment_end
        self.multichar_symbol_tokens = tokens.multichar_symbol

        self.variable_list = []
        self.function_list = []

    def identify(self, input_tokens):

        id_int = re.compile(r"^\d+$")
        id_float = re.compile(r"^\d+\.(\d+)?$")
        id_var = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

        id_char = re.compile(r"^'.*'$", re.DOTALL)
        id_string = re.compile(r'^".*"$', re.DOTALL)

        for idx, token in enumerate(input_tokens):
            if token.tag == "unknown":
                token_str = token.token
                #Match library names (stdio.h, conio.h)
                if token_str.lower().endswith(".h"):
                    token.tag = tokens.tag_name_preproc
                #Match integers (1234, 5454, 5)
                elif id_int.match(token_str):
                    token.tag = tokens.tag_val_int
                #Match floating-point (1.1, 3.14, 2.)
                elif id_float.match(token_str):
                    token.tag = tokens.tag_val_float
                #Match variable names (x, result, _hero9, y2)
                elif id_var.match(token_str):
                    token.tag = tokens.tag_name_var
                #Match characters ('a', 'b')
                elif id_char.match(token_str):
                    token.tag = tokens.tag_val_char
                #Match strings ("abc", "def")
                elif id_string.match(token_str):
                    token.tag = tokens.tag_val_string

                #Match comment string (comments doesn't have any pattern, match based on position of comment tags)
                if idx == 1:
                    prev_token = input_tokens[0].tag
                    if prev_token == tokens.tag_single_comment or prev_token == tokens.tag_multi_comment:
                        token.tag = "comment"

        return input_tokens

    def get_string_length(self, text):
        """
        Returns an index in which the first string in the text ends. Returns -1 if no string are ending.
        (The text parameter must start with either single or double quotes)
        """
        
        #Do a sanity check; is the text really a string?
        if(not self.is_string(text)):
            print(f"ERROR! The text ({text}) is not a string, but skip_text() is called on it.")
            return -1

        #What we're looking for is either single or double token; check the first character to determine which.
        cur_string_delimiter = text[0]
        found = False

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

    def tokens_validate(self, text_tokens, rule_tokens):
        """
        A template function to check if text_tokens list of string's first element
        is rule_tokens (if it's string), or if it's in rule_tokens if the text starts 
        with any token from the tokens (if it's list or dictionary).
        """
        start_token = text_tokens[0]
        if isinstance(rule_tokens, dict):
            return start_token in rule_tokens.values()
        elif isinstance(rule_tokens, list):
            return start_token in rule_tokens
        elif isinstance(rule_tokens, str):
            return start_token == rule_tokens
        else:
            return False
            
    def text_validate(self, text, tokens):
        """
        A template function to check if text string starts with the tokens (if it's string),
        or if the text starts with any token from the tokens (if it's list or dictionary).
        """
        if isinstance(tokens, dict):
            return True in (text.startswith(token) for token in tokens.values())
        elif isinstance(tokens, list):
            return True in (text.startswith(token) for token in tokens)
        elif isinstance(tokens, str):
            return text.startswith(tokens)
        else:
            return False

    def stmt_validate(self, statement, tokens):
        """
        A template function to check if a statement (either as a string or a list of string)
        starts with the tokens variable (tokens might be a dict, list, or string)
        """
        if isinstance(statement, list):
            return self.tokens_validate(statement, tokens)
        elif isinstance(statement, str):
            return self.text_validate(statement, tokens)
        else:
            raise ValueError("Statement is neither a list or string object")
        
    #Functions to check the type of a statement.
    is_block_end = lambda self, text: self.stmt_validate(text, tokens.curly_right)
    is_block_start = lambda self, text: self.stmt_validate(text, tokens.curly_left)
    is_conditional = lambda self, text: self.stmt_validate(text, tokens.conditionals)
    is_declaration = lambda self, text: self.stmt_validate(text, tokens.datatypes)
    is_include = lambda self, text: self.stmt_validate(text, tokens.preprocessor)
    is_loop = lambda self, text: self.stmt_validate(text, tokens.loops)
    is_multicomment = lambda self, text: self.stmt_validate(text, tokens.multi_comment)
    is_singlecomment = lambda self, text: self.stmt_validate(text, tokens.single_comment)
    is_comment = lambda self, text: self.is_singlecomment(text) or self.is_multicomment(text) #Returns true for both single and multi-line comments
    is_string = lambda self, text: self.stmt_validate(text, tokens.string_identifiers)

    is_do = lambda self, text: self.stmt_validate(text, tokens.dowhile_loop)
    is_for = lambda self, text: self.stmt_validate(text, tokens.for_loop)
    is_while = lambda self, text: self.stmt_validate(text, tokens.while_loop)