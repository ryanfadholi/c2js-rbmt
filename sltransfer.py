import tokendicts as tokens

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
        self.declaration_sp = Pattern([tokens.datatypes, tokens.tag_name_var], [tokens.tag_semicolon])
        self.function_sp = Pattern([tokens.datatypes, tokens.tag_name_var], [tokens.tag_parenthesis_right])
        self.conditional_sp = Pattern([tokens.conditionals])
        self.loop_sp = Pattern([tokens.loops])
        self.initiation_sp = Pattern([tokens.tag_name_var, tokens.tag_assign])

        self.declaration_tl = self.TranslationItem(tokens.datatypes, "var-keyword", "var")
        self.function_tl = self.TranslationItem(tokens.datatypes, "var-function", "function")

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
            statement.statement_type = "include-library"
        elif self.single_comment_sp.trace(tags):
            statement.statement_type = "single-line-comment"
        elif self.multi_comment_sp.trace(tags):
            statement.statement_type = "multi-line-comment"
        elif self.input_sp.trace(tags):
            statement.statement_type = "input"
        elif self.output_sp.trace(tags):
            statement.statement_type = "output"
        elif self.declaration_sp.trace(tags):
            statement.statement_type = "variable-declaration"
        elif self.block_start_sp.trace(tags):
            statement.statement_type = "code-block-start"
        elif self.block_end_sp.trace(tags):
            statement.statement_type = "code-block-end"
        elif self.conditional_sp.trace(tags):
            statement.statement_type = "conditional"
        elif self.loop_sp.trace(tags):
            statement.statement_type = "loop"
        elif self.function_sp.trace(tags):
            statement.statement_type = "function-declaration"
        elif self.return_sp.trace(tags):
            statement.statement_type = "return-statement"
        else:
            statement.statement_type = "unknown"

        return statement

    def pair(self, token, pairs):
        #TODO: Should we extract this to TranslationPair instead?
        """Try to match a TranslationPair to token"""

        pass

    def swap(self, statement, pairs):
        for token in statement:
            for pair in pairs:
                
        pass

    def translate(self, statement):
        statement = self.identify(statement)

        if not statement.carryover:
            statement.tokens = []

        if statement == "variable-declaration":
            statement = self.swap(statement, [self.declaration_tl])
        pass

        return statement


        