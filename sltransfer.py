import tokendicts as tokens

from pattern import Pattern

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
        block_start_pattern = Pattern([tokens.tag_curly_left])
        block_end_pattern = Pattern([tokens.tag_curly_right])
        preprocessor_pattern = Pattern([tokens.tag_preprocessor] )
        single_comment_pattern = Pattern([tokens.tag_single_comment])
        multi_comment_pattern = Pattern([tokens.tag_multi_comment])
        input_pattern = Pattern([tokens.tag_input_func])
        output_pattern = Pattern([tokens.tag_output_func])
        return_pattern = Pattern([tokens.tag_return_kw])
        declaration_pattern = Pattern([tokens.datatypes, tokens.tag_name_var], [tokens.tag_semicolon])
        conditional_pattern = Pattern([tokens.conditionals])
        loop_pattern = Pattern([tokens.loops])
        initiation_pattern = Pattern([tokens.tag_name_var, tokens.tag_assign])

        if preprocessor_pattern.trace(tags):
            statement.statement_type = "include-library"
        elif single_comment_pattern.trace(tags):
            statement.statement_type = "single-line-comment"
        elif multi_comment_pattern.trace(tags):
            statement.statement_type = "multi-line-comment"
        elif input_pattern.trace(tags):
            statement.statement_type = "input"
        elif output_pattern.trace(tags):
            statement.statement_type = "output"
        elif block_start_pattern.trace(tags):
            statement.statement_type = "code-block-start"
        elif block_end_pattern.trace(tags):
            statement.statement_type = "code-block-end"
        elif conditional_pattern.trace(tags):
            statement.statement_type = "conditional"
        elif loop_pattern.trace(tags):
            statement.statement_type = "loop"
        elif return_pattern.trace(tags):
            statement.statement_type = "return-statement"
        else:
            statement.statement_type = "unknown"

        return statement


        