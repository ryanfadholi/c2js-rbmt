import tokendicts as tokens
from taggedtoken import TaggedToken

from collections import ChainMap, namedtuple
from pattern import Pattern

BLOCK_START_TAG = "code-block-start"
BLOCK_END_TAG = "code-block-end"
CONDITIONAL_TAG = "conditional"
DECLARATION_TAG = "variable-declaration"
FUNCTION_TAG = "function-declaration"
FUNCTION_DEFINITION_TAG = "function-definition"
INITIATION_TAG = "variable-initiation"
INPUT_TAG = "input"
LOOP_TAG = "loop"
MULTI_COMMENT_TAG = "multi-line-comment"
OUTPUT_TAG = "output"
PREPROCESSOR_TAG = "include-library"
RETURN_TAG = "return-statement"
SINGLE_COMMENT_TAG = "single-line-comment"
UNKNOWN_TAG = "unknown"

class StructuralLexicalTransfer:
    def __init__(self):
        self.CallbackPair = namedtuple("CallbackPair", ["trigger", "function"])
        self.PatternPair = namedtuple("PatternPair", ["source", "target"])
        self.TranslationItem = namedtuple("TranslationItem", ["key", "new_keys", "new_values"])
        
        self.block_start_sp = Pattern(BLOCK_START_TAG, [tokens.tag_curly_left])
        self.block_end_sp = Pattern(BLOCK_END_TAG, [tokens.tag_curly_right])
        self.preprocessor_sp = Pattern(PREPROCESSOR_TAG, [tokens.tag_preprocessor], carryover=False)
        self.single_comment_sp = Pattern(SINGLE_COMMENT_TAG, [tokens.tag_single_comment])
        self.multi_comment_sp = Pattern(MULTI_COMMENT_TAG, [tokens.tag_multi_comment])
        self.input_sp = Pattern(INPUT_TAG, [tokens.tag_input_func])
        self.output_sp = Pattern(OUTPUT_TAG, [tokens.tag_output_func])
        self.return_sp = Pattern(RETURN_TAG, [tokens.tag_return_kw])
        self.function_sp = Pattern(FUNCTION_TAG, [tokens.datatypes, tokens.tag_name_var, tokens.tag_parenthesis_left], [tokens.tag_parenthesis_right])
        self.function_definition_sp = Pattern(FUNCTION_DEFINITION_TAG, [tokens.datatypes, tokens.tag_name_var, tokens.tag_parenthesis_left], [tokens.tag_semicolon], carryover=False)
        self.declaration_sp = Pattern(DECLARATION_TAG, [tokens.datatypes], [tokens.tag_semicolon])
        self.conditional_sp = Pattern(CONDITIONAL_TAG, [tokens.conditionals])
        self.loop_sp = Pattern(LOOP_TAG, [tokens.loops])
        self.initiation_sp = Pattern(INITIATION_TAG, [tokens.tag_name_var, tokens.tag_assign])
        self.initiation_pointer_sp = Pattern(INITIATION_TAG, [tokens.tag_op_multiply])

        self.input_cb = self.CallbackPair(tokens.tag_input_func, self.fixinput)
        self.output_cb = self.CallbackPair(tokens.tag_output_func, self.addbracket)
        self.param_cb = self.CallbackPair(tokens.tag_function_type, self.fixparam)
        self.pointer_cb = self.CallbackPair(tokens.tag_op_multiply, self.skippointers)
        self.reference_cb = self.CallbackPair(tokens.tag_op_binary_and, self.helper_reference)

        self.declaration_tl = self.TranslationItem(tokens.datatypes, [tokens.tag_variable_type], [tokens.variable_type])
        self.function_tl = self.TranslationItem(tokens.datatypes, [tokens.tag_function_type], [tokens.function_type])
        self.printf_tl = self.TranslationItem(tokens.tag_output_func, 
            [tokens.tag_console_func, tokens.tag_dot, tokens.tag_output_func, tokens.tag_parenthesis_left, tokens.tag_util_func, tokens.tag_dot, tokens.tag_format_func], 
            [tokens.console_func, tokens.dot, tokens.output_func_js, tokens.parenthesis_left, tokens.util_func, tokens.dot, tokens.format_func])
        self.scanf_tl = self.TranslationItem(tokens.tag_input_func,
            [tokens.tag_read_func, tokens.tag_dot, tokens.tag_input_func],
            [tokens.read_func, tokens.dot, tokens.input_func_js])
        self.reference_start = [TaggedToken(tokens.curly_left, tokens.tag_curly_left), TaggedToken(tokens.ptr_access, tokens.tag_ptr_access), TaggedToken(tokens.colon, tokens.tag_colon)]
        self.reference_end = [TaggedToken(tokens.curly_right, tokens.tag_curly_right)]
        self.js_pointer = [TaggedToken(tokens.dot, tokens.tag_dot), TaggedToken(tokens.ptr_access, tokens.tag_ptr_access)]

    def addbracket(self, statement):
        """Adds extra brackets for output statements. (JS's output has one extra bracket from its C counterpart)"""
        obrs, cbrs, fstmts = statement.findall(tokens.tag_parenthesis_left, tokens.tag_parenthesis_right, tokens.tag_format_func)
        to_add = []

        for format_pos in fstmts:
            #Get all closing bracket positions after the current "format" function call.
            cur_close_brackets = list(filter(lambda pos: pos > format_pos, cbrs))
            for idx, close_pos in enumerate(cur_close_brackets):
                #The first closing bracket is in the 0th index, the second is in the 1st index, etc. 
                #(Add 1 to current position to determine how many closing bracket we have passed.)
                close_bracket_count = idx + 1
                cur_open_brackets = list(filter(lambda pos: close_pos > pos > format_pos, obrs))
                open_bracket_count = len(cur_open_brackets)

                if open_bracket_count == close_bracket_count:
                    to_add.append(close_pos)
                    break

        add_offset = 0
        for add_offset, pos in enumerate(to_add):
            statement.tokens.insert(pos + add_offset, TaggedToken(tokens.parenthesis_right, tokens.tag_parenthesis_right))

    def fixinput(self, statement):
        """Fixes translated input statements."""
        input_tokens = statement.findall(tokens.tag_read_func)
        empty_string_token = TaggedToken("''", tokens.tag_val_string)
        assign_token = TaggedToken(tokens.assign, tokens.tag_assign)
        dot_token = TaggedToken(tokens.dot, tokens.tag_dot)
        ptr_access_token = TaggedToken(tokens.ptr_access, tokens.tag_ptr_access)

        if input_tokens:
            #At start, we haven't processed anything.
            processed_input_count = 0
            while True:

                #Rerun the positioning check for every loop, as the position may change after the previous loop.
                obrs, input_tokens = statement.findall(tokens.tag_parenthesis_left, tokens.tag_read_func)
                #If we have processed the same number of input tokens as there is input tokens in the statement, end the loop.
                if processed_input_count == len(input_tokens):
                    break

                #Otherwise, get the first instance of unprocessed input token. (Notice how we sliced the list?)
                question_pos = min(input_tokens[processed_input_count:])
                #Then reset every flags and counters
                cur_open_brackets = list(filter(lambda pos: pos > question_pos, obrs))
                open_bracket_pos = min(cur_open_brackets)
                next_input_part = statement[open_bracket_pos:]
                closed_bracket_pos = -1
                closed_bracket_count = 0
                open_bracket_count = 0
                variable_found = False
                variable_pointer = False
                variable_token = None

                #And finally start iterating!
                for idx, token in enumerate(next_input_part):
                    if token.tag == tokens.tag_parenthesis_left:
                        open_bracket_count += 1
                    elif token.tag == tokens.tag_parenthesis_right:
                        closed_bracket_count += 1
                    #If a variable is encountered, capture it, as it needs to be rewitten later. Only capture once, thus set the found flag.
                    elif token.tag == tokens.tag_name_var and not variable_found:
                        variable_token = token
                        variable_found = True
                        #If previous token is not "&", this variable is a pointer variable
                        if next_input_part[idx-1].tag != tokens.tag_op_binary_and:
                            variable_pointer = True

                    #If a bracket is encountered and the set(s) is complete, stop iteration.
                    if open_bracket_count == closed_bracket_count and open_bracket_count > 0:
                        closed_bracket_pos = open_bracket_pos + idx 
                        break
            
                #The operation below will modify scanf-style substatement to proper readlineSync substatement. Example:
                #From: readlineSync.question("%d", &x);
                #To  : x = readlineSync.question('');

                #First get all tokens before the "readlineSync", and append it with variable captured above and an assignment operator
                statement.tokens = (statement.tokens[:question_pos] + [variable_token]
                    + ([dot_token, ptr_access_token] if variable_pointer else [])
                    + [assign_token] 
                #Next get all the remaining tokens, and insert an empty string token between the readlineSync.question calling parenthesis, 
                #overwriting any tokens inside of it.
                    + statement.tokens[question_pos:open_bracket_pos+1] + [empty_string_token] + statement.tokens[closed_bracket_pos:])
                

                #We have processed yet another input substatement. Increment. Reiterate.
                processed_input_count += 1

    def fixparam(self, statement):
        result = []
        declaration_passed = False
        for token in statement:
            if token.tag == tokens.tag_function_type:
                if declaration_passed:
                    continue
                else:
                    declaration_passed = True
            result.append(token)

        statement.tokens = result

    def helper_reference(self, statement):
        result = []
        is_referenced = False
        for idx, token in enumerate(statement):
            if token.tag == tokens.tag_op_binary_and:
                if idx == 0 or statement[idx-1].tag not in tokens.possible_lefthand_operations:    
                    is_referenced = True
                    continue
            if is_referenced:
                result.extend(self.reference_start)
                result.append(token)
                result.extend(self.reference_end)
                is_referenced = False
                continue
            result.append(token)

        statement.tokens = result
        
    def skippointers(self, statement):
        result = []
        is_lefthand = True
        is_pointer_variable = False
        for idx, token in enumerate(statement):    
            if token.tag == tokens.tag_op_multiply:
                if idx == 0 or statement[idx-1].tag not in tokens.possible_lefthand_operations:
                    is_pointer_variable = True
                    continue
            elif token.tag == tokens.tag_assign:
                is_lefthand = False
            result.append(token)
            if is_pointer_variable:
                if not ((statement.tag == DECLARATION_TAG and is_lefthand) or statement.tag == FUNCTION_TAG):
                    result.extend(self.js_pointer)
                is_pointer_variable = False
        statement.tokens = result

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
    
        #NOTE: function_declaration MUST be checked BEFORE declaration! 
        #Because declaration essentially checks a subset of function_declaration, if declaration are put before it everything will be identified as declaration.
        patterns = [self.block_start_sp, self.block_end_sp, self.preprocessor_sp, self.single_comment_sp, self.multi_comment_sp, 
                    self.input_sp, self.output_sp, self.return_sp, self.function_sp, self.function_definition_sp, self.declaration_sp, self.conditional_sp,
                    self.loop_sp, self.initiation_sp, self.initiation_pointer_sp]

        for pattern in patterns:
            if pattern.trace(tags):
                statement.tag = pattern.tag
                if not pattern.carryover:
                    statement.carryover = False
                break
        else:
            statement.tag = "unknown"

        return statement

    def cbdict(self, callbacks):
        result = {}
        for callback in callbacks:
            result[callback.trigger] = callback.function
        return result

    def tldict(self, translations):
        result = {}
        for item in translations:
            if isinstance(item.key, str):
                result[item.key] = item
            elif isinstance(item.key, dict) or isinstance(item.key, list):
                for key in item.key:
                    result[key] = item
        return result

    def swap(self, statement, specific_translations=[], specific_helpers=[]):
        default_helpers = [self.input_cb, self.output_cb, self.param_cb, self.pointer_cb, self.reference_cb]
        default_translations = [self.declaration_tl, self.printf_tl, self.scanf_tl]

        #Prioritize helpers and translations from parameter. Convert them to dicts first.
        helpers = ChainMap(self.cbdict(specific_helpers), self.cbdict(default_helpers))
        translations = ChainMap(self.tldict(specific_translations), self.tldict(default_translations))

        helper_functions = []
        result = []

        for token in statement:
            translation = translations.get(token.tag)
            if translation is not None:
                new_tokens = [TaggedToken(new_value, new_key) 
                              for new_key, new_value in zip(translation.new_keys, translation.new_values)]
                result.extend(new_tokens)
            else:
                result.append(token)

        statement.tokens = result

        for token in statement:
            #If there's a helper function defined for the function, add them to the list to call later.
            helper = helpers.get(token.tag)
            if helper is not None and helper not in helper_functions:
                helper_functions.append(helper)
        
        for helper in helper_functions:
            helper(statement)

        return statement

    def translate(self, statement):
        statement = self.identify(statement)

        if not statement.carryover:
            statement.tokens = []

        if statement.tag == "function-declaration":
            statement = self.swap(statement, [self.function_tl])
        else:
            statement = self.swap(statement)

        return statement


        