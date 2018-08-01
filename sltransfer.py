import tokendicts as tokens
from taggedtoken import TaggedToken

from collections import ChainMap, defaultdict, namedtuple
from pattern import Pattern

BLOCK_START_TAG = "code-block-start"
BLOCK_END_TAG = "code-block-end"
CONDITIONAL_TAG = "conditional"
DECLARATION_TAG = "variable-declaration"
FUNCTION_TAG = "function-declaration"
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
        self.declaration_sp = Pattern(DECLARATION_TAG, [tokens.datatypes], [tokens.tag_semicolon])
        self.function_sp = Pattern(FUNCTION_TAG, [tokens.datatypes, tokens.tag_name_var], [tokens.tag_parenthesis_right])
        self.conditional_sp = Pattern(CONDITIONAL_TAG, [tokens.conditionals])
        self.loop_sp = Pattern(LOOP_TAG, [tokens.loops])
        self.initiation_sp = Pattern(INITIATION_TAG, [tokens.tag_name_var, tokens.tag_assign])

        
        self.declaration_tl = self.TranslationItem(tokens.datatypes, [tokens.tag_variable_type], [tokens.variable_type])
        self.function_tl = self.TranslationItem(tokens.datatypes, [tokens.tag_function_type], [tokens.function_type])
        self.printf_tl = self.TranslationItem(tokens.tag_output_func, 
            [tokens.tag_console_func, tokens.tag_dot, tokens.tag_output_func, tokens.tag_parenthesis_left, tokens.tag_util_func, tokens.tag_dot, tokens.tag_format_func], 
            [tokens.console_func, tokens.dot, tokens.output_func_js, tokens.parenthesis_left, tokens.util_func, tokens.dot, tokens.format_func])
        self.scanf_tl = self.TranslationItem(tokens.tag_input_func,
            [tokens.tag_read_func, tokens.tag_dot, tokens.tag_question_func],
            [tokens.read_func, tokens.dot, tokens.question_func])
    def addbracket(self, statement):
        #TODO: Finish this!
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

        return statement

    def fixinput(self, statement):
        #TODO: Refactor as procedure?
        input_tokens = statement.findall(tokens.tag_read_func)
        empty_string_token = TaggedToken("''", tokens.tag_val_string)
        assign_token = TaggedToken("=", tokens.tag_assign)

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
                closed_bracket_pos = -1
                closed_bracket_count = 0
                open_bracket_count = 0
                variable_found = False
                variable_token = None

                #And finally start iterating!
                for idx, token in enumerate(statement[open_bracket_pos:]):
                    if token.tag == tokens.tag_parenthesis_left:
                        open_bracket_count += 1
                    elif token.tag == tokens.tag_parenthesis_right:
                        closed_bracket_count += 1
                    #If a variable is encountered, capture it, as it needs to be rewritten later. Only capture once, thus set the found flag.
                    elif token.tag == tokens.tag_name_var and not variable_found:
                        variable_token = token
                        variable_found = True

                    #If a bracket is encountered and the set(s) is complete, stop iteration.
                    if open_bracket_count == closed_bracket_count and open_bracket_count > 0:
                        closed_bracket_pos = open_bracket_pos + idx 
                        break
            
                #The operation below will modify scanf-style substatement to proper readlineSync substatement. Example:
                #From: readlineSync.question("%d", &x);
                #To  : x = readlineSync.question('');

                #First get all tokens before the "readlineSync", and append it with variable captured above and an assignment operator
                statement.tokens = (statement.tokens[:question_pos] + [variable_token, assign_token] 
                #Next get all the remaining tokens, and insert an empty string token between the readlineSync.question calling parenthesis, 
                #overwriting any tokens inside of it.
                    + statement.tokens[question_pos:open_bracket_pos+1] + [empty_string_token] + statement.tokens[closed_bracket_pos:])
                
                #We have processed yet another input substatement. Increment. Reiterate.
                processed_input_count += 1

        return statement
                       
                    

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
    
        patterns = [self.block_start_sp, self.block_end_sp, self.preprocessor_sp, self.single_comment_sp, self.multi_comment_sp, 
                    self.input_sp, self.output_sp, self.return_sp, self.declaration_sp, self.function_sp, self.conditional_sp,
                    self.loop_sp, self.initiation_sp]

        for pattern in patterns:
            if pattern.trace(tags):
                statement.tag = pattern.tag
                break
        else:
            statement.tag = "unknown"

        return statement

    def tldict(self, translations):
        result = defaultdict(None)
        for item in translations:
            if isinstance(item.key, str):
                result[item.key] = item
            elif isinstance(item.key, dict) or isinstance(item.key, list):
                for key in item.key:
                    result[key] = item
        return result

    def swap(self, statement, specific_translations=[]):
        default_translations = [self.declaration_tl, self.printf_tl, self.scanf_tl]
        result = []
        translations = ChainMap(self.tldict(specific_translations), self.tldict(default_translations))
        
        for token in statement:
            translation = translations.get(token.tag)
            if translation is not None:
                print(f"Found! {translation}")
                new_tokens = [TaggedToken(new_value, new_key) 
                              for new_key, new_value in zip(translation.new_keys, translation.new_values)]
                result.extend(new_tokens)
            else:
                result.append(token)
      
        statement.tokens = result
        return statement

    def translate(self, statement):
        statement = self.identify(statement)

        if not statement.carryover:
            statement.tokens = []

        if statement.tag == "function-declaration":
            statement = self.swap(statement, [self.function_tl])
        else:
            statement = self.swap(statement)
            #Insert extra closing bracket before semicolon
            statement = self.addbracket(statement)
            statement = self.fixinput(statement)

        return statement


        