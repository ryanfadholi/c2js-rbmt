import constants
import tokens

from collections import ChainMap, namedtuple

from taggedtoken import TaggedToken
from pattern import Pattern

#---------------------------------------------------------------------------
#CONSTANTS START
ARRAY_JS_DECL = [TaggedToken(tokens.assign, tokens.tag_assign),
                 TaggedToken(tokens.bracket_left, tokens.tag_bracket_left),
                 TaggedToken(tokens.bracket_right, tokens.tag_bracket_right)]

#------------------------------------
# TOKENS
#------------------------------------
# Universal tokens
ABS_FUNC_TOKEN = TaggedToken(tokens.abs_func, tokens.tag_abs_func)
ADD_TOKEN = TaggedToken(tokens.op_add, tokens.tag_op_add)
ASSIGN_TOKEN = TaggedToken(tokens.assign, tokens.tag_assign)
BRACKET_LEFT_TOKEN = TaggedToken(tokens.bracket_left, tokens.tag_bracket_left)
BRACKET_RIGHT_TOKEN = TaggedToken(tokens.bracket_right, tokens.tag_bracket_right)
COLON_TOKEN = TaggedToken(tokens.colon, tokens.tag_colon)
COS_FUNC_TOKEN = TaggedToken(tokens.cos_func, tokens.tag_cos_func)
CURLY_LEFT_TOKEN = TaggedToken(tokens.curly_left, tokens.tag_curly_left)
CURLY_RIGHT_TOKEN = TaggedToken(tokens.curly_right, tokens.tag_curly_right)
DIVIDE_TOKEN = TaggedToken(tokens.op_divide, tokens.tag_op_divide)
DOT_TOKEN = TaggedToken(tokens.dot, tokens.tag_dot)
MINUS_TOKEN = TaggedToken(tokens.op_minus, tokens.tag_op_minus)
MODULO_TOKEN = TaggedToken(tokens.op_modulo, tokens.tag_op_modulo)
MULTIPLY_TOKEN = TaggedToken(tokens.op_multiply, tokens.tag_op_multiply)
PARENTHESIS_LEFT_TOKEN = TaggedToken(tokens.parenthesis_left, tokens.tag_parenthesis_left)
PARENTHESIS_RIGHT_TOKEN = TaggedToken(tokens.parenthesis_right, tokens.tag_parenthesis_right)
POW_FUNC_TOKEN = TaggedToken(tokens.pow_func, tokens.tag_pow_func)
SIN_FUNC_TOKEN = TaggedToken(tokens.sin_func, tokens.tag_sin_func)
TAN_FUNC_TOKEN = TaggedToken(tokens.tan_func, tokens.tag_tan_func)

#Javascript tokens
EMPTY_STRING_TOKEN = TaggedToken("''", tokens.tag_val_string)
FORMAT_FUNC_TOKEN = TaggedToken(tokens.format_func, tokens.tag_format_func)
FUNC_TYPE_TOKEN = TaggedToken(tokens.function_type, tokens.tag_function_type)
INPUT_FUNC_JS_TOKEN = TaggedToken(tokens.input_func_js, tokens.tag_input_func)
MATH_FUNC_TOKEN = TaggedToken(tokens.math_func, tokens.tag_math_func)
NUMBER_TYPE_TOKEN = TaggedToken(tokens.number_type, tokens.tag_number_type)
OUTPUT_FUNC_JS_TOKEN = TaggedToken(tokens.output_func_js, tokens.tag_output_func)
PROCESS_FUNC_TOKEN = TaggedToken(tokens.process_func, tokens.tag_process_func)
PTR_ACCESS_TOKEN = TaggedToken(tokens.ptr_access, tokens.tag_ptr_access)
READ_FUNC_TOKEN = TaggedToken(tokens.read_func, tokens.tag_read_func)
SIZEOF_FUNC_TOKEN = TaggedToken(tokens.sizeof_func, tokens.tag_sizeof_func)
SIZEOF_LIB_TOKEN = TaggedToken(tokens.sizeof_func, tokens.tag_sizeof_lib)
STDOUT_FUNC_TOKEN = TaggedToken(tokens.stdout_func, tokens.tag_stdout_func)
SQRT_FUNC_TOKEN = TaggedToken(tokens.sqrt_func, tokens.tag_sqrt_func)
TRUNC_FUNC_TOKEN = TaggedToken(tokens.trunc_func, tokens.tag_trunc_func)
UTIL_FUNC_TOKEN = TaggedToken(tokens.util_func, tokens.tag_util_func)
VAR_TYPE_TOKEN = TaggedToken(tokens.variable_type, tokens.tag_variable_type)

#------------------------------------
# PATTERNS
#------------------------------------
BLOCK_START_SP = Pattern(constants.BLOCK_START_TAG, [tokens.tag_curly_left])
BLOCK_END_SP = Pattern(constants.BLOCK_END_TAG, [tokens.tag_curly_right])
BREAK_SP = Pattern(constants.BREAK_TAG, [tokens.tag_break_kw])
CASE_SP = Pattern(constants.CASE_TAG, [tokens.tag_case_kw])
CONDITIONAL_SP = Pattern(constants.CONDITIONAL_TAG, [tokens.conditionals])
CONTINUE_SP = Pattern(constants.CONTINUE_TAG, [tokens.tag_continue_kw])
DECLARATION_SP = Pattern(constants.DECLARATION_TAG, [tokens.datatypes], [tokens.tag_semicolon])
DEFAULT_CASE_SP = Pattern(constants.CASE_TAG, [tokens.tag_default_kw])
DEFINE_SP = Pattern(constants.DEFINE_TAG, [tokens.tag_preprocessor, tokens.tag_define_kw], carryover=False)
FUNCTION_CALL_SP = Pattern(constants.FUNCTION_CALL_TAG, [tokens.tag_name_var, tokens.tag_parenthesis_left])
FUNCTION_DEFINITION_SP = Pattern(constants.FUNCTION_DEFINITION_TAG, [tokens.datatypes, tokens.tag_name_var, tokens.tag_parenthesis_left], 
                                [tokens.tag_semicolon], carryover=False, ignored=[tokens.tag_op_multiply])
FUNCTION_SP = Pattern(constants.FUNCTION_TAG, [tokens.datatypes, tokens.tag_name_var, tokens.tag_parenthesis_left], 
                     [tokens.tag_parenthesis_right], ignored=[tokens.tag_op_multiply])
INITIATION_COMPOUND_SP = Pattern(constants.INITIATION_TAG, [tokens.tag_name_var, tokens.compound_assignment_operator])
INITIATION_POINTER_SP = Pattern(constants.INITIATION_TAG, [tokens.tag_op_multiply])
INITIATION_SP = Pattern(constants.INITIATION_TAG, [tokens.tag_name_var])
INPUT_SP = Pattern(constants.INPUT_TAG, [tokens.tag_input_func])
LOOP_SP = Pattern(constants.LOOP_TAG, [tokens.loops])
MULTI_COMMENT_SP = Pattern(constants.MULTI_COMMENT_TAG, [tokens.tag_multi_comment])
OUTPUT_SP = Pattern(constants.OUTPUT_TAG, [tokens.tag_output_func])
POST_DECREMENT_SP = Pattern(constants.DECREMENT_INCREMENT_TAG, end=[tokens.tag_op_decrement, tokens.tag_semicolon])
POST_INCREMENT_SP = Pattern(constants.DECREMENT_INCREMENT_TAG, end=[tokens.tag_op_increment, tokens.tag_semicolon])
PRE_DECREMENT_SP = Pattern(constants.DECREMENT_INCREMENT_TAG, [tokens.tag_op_decrement], [tokens.tag_semicolon])
PRE_INCREMENT_SP = Pattern(constants.DECREMENT_INCREMENT_TAG, [tokens.tag_op_increment], [tokens.tag_semicolon])
PREPROCESSOR_SP = Pattern(constants.PREPROCESSOR_TAG, [tokens.tag_preprocessor, tokens.tag_include_kw], carryover=False)
RANDOM_SEED_SP = Pattern(constants.SEED_TAG, [tokens.tag_srand_func], carryover=False)
RETURN_SP = Pattern(constants.RETURN_TAG, [tokens.tag_return_kw])
SINGLE_COMMENT_SP = Pattern(constants.SINGLE_COMMENT_TAG, [tokens.tag_single_comment])
SWITCH_SP = Pattern(constants.SWITCH_TAG, [tokens.tag_switch_kw])

#------------------------------------
# TRANSLATIONS
#------------------------------------
TranslationItem = namedtuple("TranslationItem", ["key", "new_tokens"])

ARRAY_PREFILL_START_TL = TranslationItem(tokens.tag_curly_left, [BRACKET_LEFT_TOKEN])
ARRAY_PREFILL_END_TL = TranslationItem(tokens.tag_curly_right, [BRACKET_RIGHT_TOKEN])
DECLARATION_TL = TranslationItem(tokens.datatypes, [VAR_TYPE_TOKEN])
FUNCTION_TL = TranslationItem(tokens.datatypes, [FUNC_TYPE_TOKEN])
PRINTF_TL = TranslationItem(tokens.tag_output_func, 
    [PROCESS_FUNC_TOKEN, DOT_TOKEN, STDOUT_FUNC_TOKEN, DOT_TOKEN, OUTPUT_FUNC_JS_TOKEN, 
    PARENTHESIS_LEFT_TOKEN, UTIL_FUNC_TOKEN, DOT_TOKEN, FORMAT_FUNC_TOKEN])
SCANF_TL = TranslationItem(tokens.tag_input_func,[READ_FUNC_TOKEN, DOT_TOKEN, INPUT_FUNC_JS_TOKEN])
SIZEOF_TL = TranslationItem(tokens.tag_sizeof_func, [SIZEOF_LIB_TOKEN, DOT_TOKEN, SIZEOF_FUNC_TOKEN])

ABS_TL  = TranslationItem(tokens.tag_abs_func, [MATH_FUNC_TOKEN, DOT_TOKEN, ABS_FUNC_TOKEN])
FABS_TL = TranslationItem(tokens.tag_fabs_func, [MATH_FUNC_TOKEN, DOT_TOKEN, ABS_FUNC_TOKEN])

COS_TL = TranslationItem(tokens.tag_cos_func, [MATH_FUNC_TOKEN, DOT_TOKEN, COS_FUNC_TOKEN])
POW_TL = TranslationItem(tokens.tag_pow_func, [MATH_FUNC_TOKEN, DOT_TOKEN, POW_FUNC_TOKEN])
SIN_TL = TranslationItem(tokens.tag_sin_func, [MATH_FUNC_TOKEN, DOT_TOKEN, SIN_FUNC_TOKEN])
SQRT_TL = TranslationItem(tokens.tag_sqrt_func, [MATH_FUNC_TOKEN, DOT_TOKEN, SQRT_FUNC_TOKEN])
TAN_TL = TranslationItem(tokens.tag_tan_func, [MATH_FUNC_TOKEN, DOT_TOKEN, TAN_FUNC_TOKEN])

#CONSTANTS END
#---------------------------------------------------------------------------

class StructuralLexicalTransfer:

    def __init__(self):
        self._func_context = None
        self._headers = []
        self._preprocessors = {}
        self._variables = {}

    def _callback_dict(self, callbacks):
        """Converts a list of CallbackPairs to a dictionary, with its trigger as keys and its function as the values"""
        result = {}
        for callback in callbacks:
            trigger = callback.trigger
            if isinstance(trigger, str):
                result[trigger] = callback.function
            elif isinstance(trigger, (dict, list)):
                for trig in trigger:
                    result[trig] = callback.function
        return result

    def _capture_last_variable(self, input_tokens):
        return self._capture_variable_tokens(input_tokens)[0].token

    def _capture_variable_tokens(self, input_tokens):
        bracket_depth = 0
        results = []
        
        for token in reversed(input_tokens):
            results.append(token)
            if token.tag == tokens.tag_name_var and bracket_depth == 0:
                break
            elif token.tag == tokens.tag_bracket_right:
                bracket_depth += 1
            elif token.tag == tokens.tag_bracket_left:
                bracket_depth -= 1
        results.reverse()
        return results

    def _helper_assign(self, statement):
        """Wraps integer-based assignment in JS' truncate function."""
        trunc_start = [MATH_FUNC_TOKEN, DOT_TOKEN, TRUNC_FUNC_TOKEN, PARENTHESIS_LEFT_TOKEN]
        trunc_end = [PARENTHESIS_RIGHT_TOKEN]

        asg_found = False
        is_round = False

        cur_start = -1

        wrap_start = []
        wrap_end = []

        for idx, token in enumerate(statement):
            if token.tag == tokens.tag_assign:
                cur_start = idx
                asg_found = True
            
            if asg_found:
                #Reset counters & flags
                br_count = 0 #bracket counter
                pr_count = 0 #parenthesis counter

                has_processed = False
                is_arr_def = False
                is_ptr_def = False
                var_passed = False

                last_variable = self._capture_last_variable(statement[:idx])
                variable_type = self._variables[last_variable]

                is_round = (variable_type in tokens.round_datatypes)
                        
                #start tracing forward
                ftrace_idx = idx + 1
                while(ftrace_idx < len(statement)):
                    cur_token = statement[ftrace_idx]
                    if cur_token.tag == tokens.tag_bracket_left:
                        #If there's no variables before it, it's array definition
                        if not var_passed:
                            is_arr_def = True
                            break
                        br_count += 1
                    elif cur_token.tag == tokens.tag_bracket_right:
                        if br_count == 0:
                            break
                        br_count -= 1
                    elif cur_token.tag == tokens.tag_parenthesis_left:
                        pr_count += 1
                    elif cur_token.tag == tokens.tag_parenthesis_right:
                        if pr_count == 0:
                            break
                        pr_count -= 1
                    elif cur_token.tag == tokens.tag_semicolon:
                        break
                    elif cur_token.tag == tokens.tag_comma:
                        if pr_count == 0:
                            break
                    #special cases
                    elif cur_token.tag == tokens.tag_name_var:
                        var_passed = True
                    elif cur_token.tag == tokens.tag_curly_left:
                        is_ptr_def = True
                        break
                    elif cur_token.tag == tokens.tag_trunc_func:
                        has_processed = True
                        break

                    ftrace_idx += 1
                cur_end = ftrace_idx
                
                #do nothing if it's array/pointer
                if is_arr_def or is_ptr_def or has_processed:
                    pass
                elif is_round:
                    wrap_start.append(cur_start)
                    wrap_end.append(cur_end)

                asg_found = False

        results = []
        for idx, token in enumerate(statement):
            while idx in wrap_end:
                results.extend(trunc_end)
                wrap_end.remove(idx)

            results.append(token)

            while idx in wrap_start:
                results.extend(trunc_start)
                wrap_start.remove(idx)

        statement.tokens = results

    def _helper_comp(self, statement):
        """Expands compound-assignment function to normal assignment function"""
        expanded = False
        to_expand = []

        results = []
        for idx, token in enumerate(statement):
            if token.tag == tokens.tag_op_comp_add:
                to_expand = [ADD_TOKEN]
                expanded = True
            elif token.tag == tokens.tag_op_comp_minus:
                to_expand = [MINUS_TOKEN]
                expanded = True
            elif token.tag == tokens.tag_op_comp_divide:
                to_expand = [DIVIDE_TOKEN]
                expanded = True
            elif token.tag == tokens.tag_op_comp_multiply:
                to_expand = [MULTIPLY_TOKEN]
                expanded = True
            elif token.tag == tokens.tag_op_comp_modulo:
                to_expand = [MODULO_TOKEN]
                expanded = True
            elif token.tag == tokens.tag_op_comp_multiply:
                to_expand = [MULTIPLY_TOKEN]
                expanded = True
            
            if expanded:
                variable_tokens = self._capture_variable_tokens(statement[:idx])
                results.extend([ASSIGN_TOKEN] + variable_tokens + to_expand)
                expanded = False
            else:
                results.append(token)
        statement.tokens = results

        self._helper_assign(statement)

    def _helper_declaration(self, statement):
        is_lefthand = True
        is_prefilled_value = False
        prefilled_depth = 0

        skip = False
        skipped = False
        result = []

        for token in statement:
            tag = token.tag

            if tag == tokens.tag_assign:
                is_lefthand = False

            if is_lefthand and tag == tokens.tag_bracket_left:
                skip = True
                skipped = True
            #right-hand bracket means hard-coded array values
            elif not is_lefthand and tag == tokens.tag_bracket_left:
                is_prefilled_value = True
                prefilled_depth += 1

            if not skip:
                #if the comma is inside a hard-coded value, skip this step
                if ((tag == tokens.tag_comma or tag == tokens.tag_semicolon) and 
                    not is_prefilled_value):
                    #If there's no declaration and there's skipped brackets 
                    if is_lefthand and skipped:
                        result.extend(ARRAY_JS_DECL)
                    is_lefthand = True
                    skipped = False

                result.append(token)

            if is_lefthand and tag == tokens.tag_bracket_right:
                skip = False
            elif not is_lefthand and tag == tokens.tag_bracket_right:
                prefilled_depth -= 1
                if prefilled_depth == 0:
                    is_prefilled_value = False
            

        statement.tokens = result

    def _helper_output(self, statement):
        """Adds extra brackets for output statements. (JS's output has one extra bracket from its C counterpart)"""
        obrs, cbrs, fstmts = statement.find_all(tokens.tag_parenthesis_left, tokens.tag_parenthesis_right, tokens.tag_format_func)
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
            statement.tokens.insert(pos + add_offset, PARENTHESIS_RIGHT_TOKEN)

    def _helper_input(self, statement):
        """Fixes translated input statements' order of tokens."""
        input_tokens = statement.find_all(tokens.tag_read_func)

        if input_tokens:
            #At start, we haven't processed anything.
            processed_input_count = 0
            while True:
                #Rerun the positioning check for every loop, as the position may change after the previous loop.
                obrs, input_tokens = statement.find_all(tokens.tag_parenthesis_left, 
                                                        tokens.tag_read_func)
                #If we have processed the same number of input tokens as there is input tokens in the statement, end the loop.
                if processed_input_count == len(input_tokens):
                    break

                #Otherwise, get the first instance of unprocessed input token. (Notice how we sliced the list?)
                question_pos = min(input_tokens[processed_input_count:])
                #Then reset every flags and counters
                cur_open_brackets = list(filter(lambda pos: pos > question_pos, obrs))
                open_bracket_pos = min(cur_open_brackets)
                next_input_part = statement[open_bracket_pos:]
                member_access_tokens = []
                bracket_depth = 0                
                closed_bracket_pos = -1
                closed_bracket_count = 0
                open_bracket_count = 0
                number_expected = False
                variable_found = False
                variable_member_access = False
                variable_pointer = False
                variable_token = None

                #And finally start iterating!
                for idx, token in enumerate(next_input_part):

                    #Handles array inputs
                    if variable_member_access:
                        member_access_tokens.append(token)
                        
                        if token.tag == tokens.tag_bracket_left:
                            bracket_depth += 1
                        elif token.tag == tokens.tag_bracket_right:
                            bracket_depth -= 1
                        
                        if bracket_depth == 0:
                            variable_member_access = False

                    if token.tag == tokens.tag_parenthesis_left:
                        open_bracket_count += 1
                    elif token.tag == tokens.tag_parenthesis_right:
                        closed_bracket_count += 1
                    #If it's string, process to determine whether the input needs type-casting or not.
                    elif token.tag == tokens.tag_val_string:
                        identifier_string = token.token
                        is_identifier = False
                        for char in identifier_string:
                            if is_identifier:
                                if char in ['d','f','h','i','l']:
                                    number_expected = True
                            if char == '%':
                                is_identifier = True
                                continue
                    #If a variable is encountered, capture it, as it needs to be rewitten later. Only capture once, thus set the found flag.
                    elif token.tag == tokens.tag_name_var and not variable_found:
                        variable_token = token
                        variable_found = True
                        #If previous token is not "&", this variable is a pointer variable
                        if next_input_part[idx-1].tag != tokens.tag_op_binary_and:
                            variable_pointer = True
                    elif token.tag == tokens.tag_bracket_left and variable_found:
                        variable_member_access = True
                        bracket_depth += 1
                        member_access_tokens.append(token)

                    #If a bracket is encountered and the set(s) is complete, stop iteration.
                    if open_bracket_count == closed_bracket_count and open_bracket_count > 0:
                        closed_bracket_pos = open_bracket_pos + idx 
                        break
            
                #The operation below will modify scanf-style substatement to proper readlineSync substatement. Example:
                #From: readlineSync.question("%d", &x);
                #To  : x = readlineSync.question('');

                statement.tokens = (
                    #First get all tokens before the "readlineSync", and the variable captured above                
                    (statement.tokens[:question_pos] + [variable_token])
                    #Add array positional information if exists
                    + (member_access_tokens)
                    #Add pointer access if the variable is a pointer.
                    + ([DOT_TOKEN, PTR_ACCESS_TOKEN] if variable_pointer else [])
                    #Assignment operator
                    + ([ASSIGN_TOKEN]) 
                    #Add typecasting if needed
                    + ([NUMBER_TYPE_TOKEN, PARENTHESIS_LEFT_TOKEN] if number_expected else [])
                    #Next get all the remaining tokens, and insert an empty string token between the readlineSync.question calling parenthesis, 
                    #overwriting any tokens inside of it.
                    + (statement.tokens[question_pos:open_bracket_pos+1] + [EMPTY_STRING_TOKEN])
                    #Add closing parenthesis after the empty string token if you typecasted.
                    + ([PARENTHESIS_RIGHT_TOKEN] if number_expected else [])
                    #Finally, append all tokens after the original closed bracket.
                    + (statement.tokens[closed_bracket_pos:])
                )

                #We have processed yet another input substatement. Increment. Reiterate.
                processed_input_count += 1

    def _helper_parameter(self, statement):
        """Removes data type from parameter in function declarations"""
        result = []
        declaration_passed = False
        function_name_passed = False
        is_main = False
        is_main_parameter = False
        for token in statement:
            
            if is_main:
                if is_main_parameter:
                    if token.tag == tokens.tag_parenthesis_right:
                        is_main_parameter = False
                    else:
                        continue
                if token.tag == tokens.tag_parenthesis_left:
                    is_main_parameter = True
            else:
                if token.tag == tokens.tag_function_type:
                    if declaration_passed:
                        continue
                    else:
                        declaration_passed = True
                elif token.tag == tokens.tag_name_var and not function_name_passed:
                    if token.token == "main":
                        is_main = True
                    function_name_passed = True

            result.append(token)

        statement.tokens = result

    def _helper_reference(self, statement):
        """Adds object-wrapping for reference-like objects in JS"""
        reference_start = [CURLY_LEFT_TOKEN, PTR_ACCESS_TOKEN, COLON_TOKEN]
        reference_end = [CURLY_RIGHT_TOKEN]
        
        result = []
        is_referenced = False

        for idx, token in enumerate(statement):
            if token.tag == tokens.tag_op_binary_and:
                if idx == 0 or statement[idx-1].tag not in tokens.possible_lefthand_operations:    
                    is_referenced = True
                    continue
            if is_referenced:
                result.extend(reference_start)
                result.append(token)
                result.extend(reference_end)
                is_referenced = False
                continue
            result.append(token)

        statement.tokens = result

    def _helper_return(self, statement):
        trunc_start = [MATH_FUNC_TOKEN, DOT_TOKEN, TRUNC_FUNC_TOKEN, PARENTHESIS_LEFT_TOKEN]
        trunc_end = [PARENTHESIS_RIGHT_TOKEN]

        function_type = self._variables[self._func_context]
        is_round = (function_type in tokens.round_datatypes)
        if is_round:
            results = []
            after_return = False
            open_bracket = 0
            for token in statement:
                if (token.tag in [tokens.tag_comma, tokens.tag_semicolon] and after_return
                    and not open_bracket):
                    results.extend(trunc_end)
                    after_return = False
                elif token.tag == tokens.tag_parenthesis_left:
                    open_bracket += 1
                elif token.tag == tokens.tag_parenthesis_right:
                    open_bracket -= 1
                results.append(token)
                if token.tag == tokens.tag_return_kw:
                    results.extend(trunc_start)
                    after_return = True
            statement.tokens = results

    def _helper_pointer(self, statement):
        """Adds pointer member access for pointer-emulating variables in translation result"""
        js_pointer = [DOT_TOKEN, PTR_ACCESS_TOKEN]

        result = []
        is_lefthand = True
        is_multiply_exists = False
        is_pointer_variable = False
        
        for idx, token in enumerate(statement):    
            if token.tag == tokens.tag_op_multiply:
                if idx == 0 or statement[idx-1].tag not in tokens.possible_lefthand_operations:
                    is_pointer_variable = True
                    continue
                else:
                    is_multiply_exists = True
            elif token.tag == tokens.tag_assign:
                is_lefthand = False
            result.append(token)
            if is_pointer_variable:
                if not ((statement.tag == constants.DECLARATION_TAG and is_lefthand) 
                         or statement.tag == constants.FUNCTION_TAG):
                    result.extend(js_pointer)
                is_pointer_variable = False
        statement.tokens = result

    def _identify(self, statement):
        """Identifies statement type"""

        #NOTE: 
        #1. function declaration MUST be checked BEFORE variable declaration
        #2. function call MUST be checked BEFORE variable initiation 
        #Because declaration essentially checks a subset of function_declaration, if declaration are put before it everything will be identified as declaration.
        patterns = [BLOCK_START_SP, BLOCK_END_SP, PREPROCESSOR_SP, DEFINE_SP, SINGLE_COMMENT_SP, MULTI_COMMENT_SP, 
                    INPUT_SP, OUTPUT_SP, RETURN_SP, FUNCTION_SP, FUNCTION_CALL_SP, FUNCTION_DEFINITION_SP, DECLARATION_SP, CONDITIONAL_SP,
                    LOOP_SP, INITIATION_SP, BREAK_SP, CONTINUE_SP, INITIATION_COMPOUND_SP, INITIATION_POINTER_SP, CASE_SP, DEFAULT_CASE_SP, 
                    SWITCH_SP, POST_DECREMENT_SP, POST_INCREMENT_SP, PRE_DECREMENT_SP, PRE_INCREMENT_SP, RANDOM_SEED_SP]

        tags = [token.tag for token in statement]

        for pattern in patterns:
            if pattern.trace(tags):
                statement.tag = pattern.tag
                if not pattern.carryover:
                    statement.carryover = False
                break
        else:
            print("NOTICE - UNIDENTIFIED STATEMENT:")
            print(statement)
            statement.tag = "unknown"

        return statement

    def _preprocess(self, tokens):
        result = []
        for token in tokens:
            preprocess_value = self._preprocessors.get(token.token)
            if preprocess_value is not None:
                result.extend(preprocess_value)
            else:
                result.append(token)
        return result

    def _translation_dict(self, translations):
        """Converts a list of TranslationItems to a dictionary"""
        result = {}
        for item in translations:
            if isinstance(item.key, str):
                result[item.key] = item
            elif isinstance(item.key, (dict, list)):
                for key in item.key:
                    result[key] = item
        return result

    def reset(self):
        self._func_context = None
        self._headers = []
        self._preprocessors = {}
        self._variables = {}

    def translate(self, statement):
        """Translates C TaggedStatement to its JS equivalent."""

        #Define namedtuples needed by helper callbacks & translations
        CallbackPair = namedtuple("CallbackPair", ["trigger", "function"])

        #Define helper callbacks here
        ARRAY_DECL_CB = CallbackPair(tokens.tag_bracket_left, self._helper_declaration)
        ASSIGN_CB = CallbackPair(tokens.tag_assign, self._helper_assign)
        COMP_ADD_CB = CallbackPair(tokens.tag_op_comp_add, self._helper_comp)
        COMP_DIV_CB = CallbackPair(tokens.tag_op_comp_divide, self._helper_comp)
        COMP_MOD_CB = CallbackPair(tokens.tag_op_comp_modulo, self._helper_comp)
        COMP_MIN_CB = CallbackPair(tokens.tag_op_comp_minus, self._helper_comp)
        COMP_MUL_CB = CallbackPair(tokens.tag_op_comp_multiply, self._helper_comp)
        INPUT_CB = CallbackPair(tokens.tag_input_func, self._helper_input)
        OUTPUT_CB = CallbackPair(tokens.tag_output_func, self._helper_output)
        PARAM_CB = CallbackPair(tokens.tag_function_type, self._helper_parameter)
        POINTER_CB = CallbackPair(tokens.tag_op_multiply, self._helper_pointer)
        REFERENCE_CB = CallbackPair(tokens.tag_op_binary_and, self._helper_reference)
        RETURN_CB = CallbackPair(tokens.tag_return_kw, self._helper_return)


        #Join everything into lists
        #NOTE: assign_cb must be put AFTER pointer_cb! Assign_cb assumes that pointer_cb has done its job.
        default_helpers = [COMP_ADD_CB, COMP_DIV_CB, COMP_MIN_CB, COMP_MOD_CB, COMP_MUL_CB, INPUT_CB, OUTPUT_CB, 
                           PARAM_CB, POINTER_CB, ASSIGN_CB, REFERENCE_CB, RETURN_CB]
        default_translations = [DECLARATION_TL, PRINTF_TL, SCANF_TL, SIZEOF_TL]

        #Add specific-header bound translations
        if constants.STDLIB_HEADER in self._headers:
            default_translations.extend([ABS_TL, FABS_TL]) 
        if constants.MATH_HEADER in self._headers:
            default_translations.extend([COS_TL, POW_TL, SIN_TL, SQRT_TL, TAN_TL])

        specific_helpers = []
        specific_translations = []

        #Start translating!
        statement = self._identify(statement)

        #Remember headers used in the code
        if statement.tag == constants.PREPROCESSOR_TAG:
            for token in statement:
                if token.tag == tokens.tag_name_preproc:
                    self._headers.append(token.token)

        #Add preprocessor if it's define statement
        if statement.tag == constants.DEFINE_TAG:
            #Keyword is placed after preprocessor tag ('#') and define keyword
            keyword = statement[2].token
            to_replace = statement[3:]
            #Unroll define itself
            if self._preprocessors:
                to_replace = self._preprocess(to_replace)
            self._preprocessors[keyword] = to_replace

        #Process preprocessors
        if self._preprocessors:
            statement.tokens = self._preprocess(list(statement))
            #Try re-iden
            if statement.tag == constants.UNKNOWN_TAG:
                statement = self._identify(statement)

        #Immediately return if it's unneeded statements (e.g function declaration)
        if not statement.carryover:
            statement.tokens = []
            return statement
      
        if statement.tag == constants.FUNCTION_TAG:
            token_pos = 1
            self._func_context = statement[token_pos].token
            #If it's star, it's a pointer function, get the next token instead
            while self._func_context == "*":
                token_pos += 1
                self._func_context = statement[token_pos].token

        #Build variables dictionary while you're at it
        if statement.tag in [constants.FUNCTION_TAG, constants.FUNCTION_DEFINITION_TAG]:
            datatype = statement[0].tag
            token_pos = 1
            variable = statement[token_pos].token
            #If it's star, it's a pointer function, get the next token instead
            while variable == "*":
                token_pos += 1
                variable = statement[token_pos].token
            self._variables[variable] = datatype
            variable_expected = False
            for token in statement:
                if token.tag in tokens.datatypes:
                    datatype = token.tag
                    variable_expected = True
                if token.tag == tokens.tag_name_var and variable_expected:
                    self._variables[token.token] = datatype
                    variable_expected = False
        elif statement.tag == constants.DECLARATION_TAG:
            is_lefthand = True
            in_bracket = False
            bracket_count = 0
            datatype = statement[0].tag
            for token in statement:
                if token.tag == tokens.tag_assign:
                    is_lefthand = False
                elif token.tag == tokens.tag_comma:
                    is_lefthand = True
                elif token.tag == tokens.tag_bracket_left:
                    in_bracket = True
                    bracket_count += 1
                elif token.tag == tokens.tag_bracket_right:
                    bracket_count -= 1
                    if bracket_count == 0:
                        in_bracket = False
                elif token.tag == tokens.tag_name_var:
                    if is_lefthand and not in_bracket:
                        self._variables[token.token] = datatype

        #Add special cases of helpers/translations here
        if statement.tag == constants.FUNCTION_TAG:
            specific_helpers.append(ARRAY_DECL_CB)
            specific_translations.append(FUNCTION_TL)
        elif statement.tag == constants.DECLARATION_TAG:
            specific_helpers.append(ARRAY_DECL_CB)
            specific_translations.extend([ARRAY_PREFILL_START_TL, ARRAY_PREFILL_END_TL])

        #Prioritize special-case helpers and translations. Convert them to dicts first.
        helpers = ChainMap(self._callback_dict(specific_helpers), self._callback_dict(default_helpers))
        translations = ChainMap(self._translation_dict(specific_translations), self._translation_dict(default_translations))

        #Start translating
        result = []
        for token in statement:
            translation = translations.get(token.tag)
            if translation is not None:
                new_tokens = [token for token in translation.new_tokens]
                result.extend(new_tokens)
            else:
                result.append(token)

        #Overwrite statement tokens with translation results
        statement.tokens = result

        #List helper functions we need to call
        helper_functions = []
        for token in statement:
            #If there's a helper function defined for the function, add them to the list to call later.
            helper = helpers.get(token.tag)
            if helper is not None and helper not in helper_functions:
                helper_functions.append(helper)

        #NOTE: Prioritize pointer and reference helper - assignment and compound operator helpers assumes their job is done.
        #Then prioritize helper_output even higher, as it is programmed as if reference helper has not done its job yet.
        if self._helper_pointer in helper_functions:
            helper_functions.insert(0, 
                                    helper_functions.pop(
                                                         helper_functions.index(self._helper_pointer)))
        
        if self._helper_reference in helper_functions:
            helper_functions.insert(0, 
                                    helper_functions.pop(
                                                         helper_functions.index(self._helper_reference)))
                                                    
        if self._helper_input in helper_functions:
            helper_functions.insert(0, 
                                    helper_functions.pop(
                                                         helper_functions.index(self._helper_input)))
                                        

        for helper in helper_functions:
            helper(statement)

        return statement
