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
    
        #declaration_pattern = [tokens.tag_]
        block_end_pattern = [tokens.tag_curly_right]
        preprocessor_pattern = [tokens.tag_preprocessor] 
        single_comment_pattern = [tokens.tag_single_comment]
        multi_comment_pattern = [tokens.tag_multi_comment]
        input_pattern = [tokens.tag_input_func]
        output_pattern = [tokens.tag_output_func]
        return_pattern = [tokens.tag_return_kw]
        if self.trace(preprocessor_pattern, tags):
            statement.statement_type = "include-library"
        elif self.trace(single_comment_pattern, tags):
            statement.statement_type = "single-line-comment"
        elif self.trace(multi_comment_pattern, tags):
            statement.statement_type = "multi-line-comment"
        elif self.trace(input_pattern, tags):
            statement.statement_type = "input"
        elif self.trace(output_pattern, tags):
            statement.statement_type = "output"
        elif self.trace(block_end_pattern, tags):
            statement.statement_type = "code-block-end"
        elif self.trace(return_pattern, tags):
            statement.statement_type = "return-statement"
        else:
            statement.statement_type = "unknown"

        return statement


        