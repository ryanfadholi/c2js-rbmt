import tokendicts as tokens
from taggedtoken import TaggedToken

from collections import namedtuple
from pattern import Pattern

class StructuralLexicalTransfer:
    def __init__(self):
        self.PatternPair = namedtuple("PatternPair", ["source", "target"])
        self.TranslationItem = namedtuple("TranslationItem", ["key", "new_key", "new_value"])
        
        self.block_start_sp = Pattern([tokens.tag_curly_left])
        self.block_end_sp = Pattern([tokens.tag_curly_right])
        self.preprocessor_sp = Pattern([tokens.tag_preprocessor], carryover=False)
        self.single_comment_sp = Pattern([tokens.tag_single_comment])
        self.multi_comment_sp = Pattern([tokens.tag_multi_comment])
        self.input_sp = Pattern([tokens.tag_input_func])
        self.output_sp = Pattern([tokens.tag_output_func])
        self.return_sp = Pattern([tokens.tag_return_kw])
        self.declaration_sp = Pattern([tokens.datatypes], [tokens.tag_semicolon])
        self.function_sp = Pattern([tokens.datatypes, tokens.tag_name_var], [tokens.tag_parenthesis_right])
        self.conditional_sp = Pattern([tokens.conditionals])
        self.loop_sp = Pattern([tokens.loops])
        self.initiation_sp = Pattern([tokens.tag_name_var, tokens.tag_assign])

        self.declaration_tl = self.TranslationItem(tokens.datatypes, "var-keyword", "var")
        self.function_tl = self.TranslationItem(tokens.datatypes, "var-function", "function")
        self.printf_tl = self.TranslationItem(tokens.tag_output_func, tokens.tag_output_func, "console.log(util.format")

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
    
        #declaration_sp = [tokens.tag_]
        if self.preprocessor_sp.trace(tags):
            statement.type = "include-library"
        elif self.single_comment_sp.trace(tags):
            statement.type = "single-line-comment"
        elif self.multi_comment_sp.trace(tags):
            statement.type = "multi-line-comment"
        elif self.input_sp.trace(tags):
            statement.type = "input"
        elif self.output_sp.trace(tags):
            statement.type = "output"
        elif self.declaration_sp.trace(tags):
            statement.type = "variable-declaration"
        elif self.block_start_sp.trace(tags):
            statement.type = "code-block-start"
        elif self.block_end_sp.trace(tags):
            statement.type = "code-block-end"
        elif self.conditional_sp.trace(tags):
            statement.type = "conditional"
        elif self.loop_sp.trace(tags):
            statement.type = "loop"
        elif self.function_sp.trace(tags):
            statement.type = "function-declaration"
        elif self.return_sp.trace(tags):
            statement.type = "return-statement"
        else:
            statement.type = "unknown"

        return statement

    def pair(self, token, pair):
        #TODO: Should we extract this to TranslationPair instead?
        """Try to match a TranslationPair to token"""
        pair_key = pair.key
        
        if isinstance(pair_key, str):
            return token.tag == pair_key
        elif isinstance(pair_key, dict) or isinstance(pair_key, list):
            return token.tag in pair_key
        else:
            print("Key have an unknown data type")
        return False

    def swap(self, statement, pairs):
        swaps = []
        for idx, token in enumerate(statement):
            for pair in pairs:
                if self.pair(token, pair):
                    print("Trigger 2!")
                    token = TaggedToken(pair.new_value, pair.new_key)
                    swaps.append((idx, token))
                    break
        
        for swap in swaps:
            pos, new_token = swap
            statement[pos] = new_token
        
        return statement

    def translate(self, statement):
        #TODO: Should I separate the "console.log(util.format" to 3 tokens?
        #TODO: Extend declaration_tl swapping to every other statement EXCEPT function declaration (maybe try adding a "exclude-list" of some sort?)
        statement = self.identify(statement)

        if not statement.carryover:
            statement.tokens = []

        if statement.type == "variable-declaration":
            statement = self.swap(statement, [self.declaration_tl])  
        elif statement.type == "function-declaration":
            statement = self.swap(statement, [self.function_tl])
        elif statement.type == "output":
            statement = self.swap(statement, [self.printf_tl])
            pre_bracket, post_bracket = statement[0:-1], statement[len(statement)-1:len(statement)]
            statement.tokens = pre_bracket + [TaggedToken(")", tokens.tag_bracket_right)] + post_bracket


        return statement


        