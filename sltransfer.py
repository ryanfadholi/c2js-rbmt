import constants
import tokens

from taggedtoken import TaggedToken

from collections import ChainMap, namedtuple
from pattern import Pattern

class StructuralLexicalTransfer:

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

    def _helper_declaration(self, statement):
        is_lefthand = True
        skip = False
        result = []

        for token in statement:
            tag = token.tag

            if tag == tokens.tag_assign:
                is_lefthand = False

            if is_lefthand and tag == tokens.tag_bracket_left:
                skip = True

            if not skip:
                result.append(token)

            if is_lefthand and tag == tokens.tag_bracket_right:
                skip = False

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
            statement.tokens.insert(pos + add_offset, TaggedToken(tokens.parenthesis_right, tokens.tag_parenthesis_right))

    def _helper_input(self, statement):
        """Fixes translated input statements' order of tokens."""
        input_tokens = statement.find_all(tokens.tag_read_func)
        empty_string_token = TaggedToken("''", tokens.tag_val_string)
        assign_token = TaggedToken(tokens.assign, tokens.tag_assign)
        close_parenthesis_token = TaggedToken(tokens.parenthesis_right, tokens.tag_parenthesis_right)
        dot_token = TaggedToken(tokens.dot, tokens.tag_dot)
        number_type_token = TaggedToken(tokens.number_type, tokens.tag_number_type)
        open_parenthesis_token = TaggedToken(tokens.parenthesis_left, tokens.tag_parenthesis_left)
        ptr_access_token = TaggedToken(tokens.ptr_access, tokens.tag_ptr_access)

        if input_tokens:
            #At start, we haven't processed anything.
            processed_input_count = 0
            while True:

                #Rerun the positioning check for every loop, as the position may change after the previous loop.
                obrs, input_tokens = statement.find_all(tokens.tag_parenthesis_left, tokens.tag_read_func)
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
                number_expected = False
                variable_found = False
                variable_pointer = False
                variable_token = None

                #And finally start iterating!
                for idx, token in enumerate(next_input_part):
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
                    #Add pointer access if the variable is a pointer.
                    + ([dot_token, ptr_access_token] if variable_pointer else [])
                    #Assignment operator
                    + ([assign_token]) 
                    #Add typecasting if needed
                    + ([number_type_token, open_parenthesis_token] if number_expected else [])
                    #Next get all the remaining tokens, and insert an empty string token between the readlineSync.question calling parenthesis, 
                    #overwriting any tokens inside of it.
                    + (statement.tokens[question_pos:open_bracket_pos+1] + [empty_string_token])
                    #Add closing parenthesis after the empty string token if you typecasted.
                    + ([close_parenthesis_token] if number_expected else [])
                    #Finally, append all tokens after the original closed bracket.
                    + (statement.tokens[closed_bracket_pos:])
                )

                #We have processed yet another input substatement. Increment. Reiterate.
                processed_input_count += 1

    def _helper_parameter(self, statement):
        """Removes data type from parameter in function declarations"""
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

    def _helper_reference(self, statement):
        """Adds object-wrapping for reference-like objects in JS"""
        reference_start = [TaggedToken(tokens.curly_left, tokens.tag_curly_left), TaggedToken(tokens.ptr_access, tokens.tag_ptr_access), TaggedToken(tokens.colon, tokens.tag_colon)]
        reference_end = [TaggedToken(tokens.curly_right, tokens.tag_curly_right)]
        
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

    def _helper_pointer(self, statement):
        """Adds pointer member access for pointer-emulating variables in translation result"""
        js_pointer = [TaggedToken(tokens.dot, tokens.tag_dot), TaggedToken(tokens.ptr_access, tokens.tag_ptr_access)]

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
                if not ((statement.tag == constants.DECLARATION_TAG and is_lefthand) 
                         or statement.tag == constants.FUNCTION_TAG):
                    result.extend(js_pointer)
                is_pointer_variable = False
        statement.tokens = result

    def _identify(self, statement):
        """Identifies statement type"""
        block_start_sp = Pattern(constants.BLOCK_START_TAG, 
                                 [tokens.tag_curly_left])
        block_end_sp = Pattern(constants.BLOCK_END_TAG, 
                               [tokens.tag_curly_right])
        conditional_sp = Pattern(constants.CONDITIONAL_TAG, 
                                 [tokens.conditionals])
        declaration_sp = Pattern(constants.DECLARATION_TAG, 
                                 [tokens.datatypes], 
                                 [tokens.tag_semicolon])
        function_definition_sp = Pattern(constants.FUNCTION_DEFINITION_TAG, 
                                         [tokens.datatypes, tokens.tag_name_var, tokens.tag_parenthesis_left], 
                                         [tokens.tag_semicolon], 
                                         carryover=False)
        function_sp = Pattern(constants.FUNCTION_TAG, 
                              [tokens.datatypes, tokens.tag_name_var, tokens.tag_parenthesis_left], 
                              [tokens.tag_parenthesis_right])
        initiation_pointer_sp = Pattern(constants.INITIATION_TAG, 
                                        [tokens.tag_op_multiply])
        initiation_sp = Pattern(constants.INITIATION_TAG, 
                                [tokens.tag_name_var, tokens.tag_assign])
        input_sp = Pattern(constants.INPUT_TAG, 
                           [tokens.tag_input_func])
        loop_sp = Pattern(constants.LOOP_TAG, 
                          [tokens.loops])                    
        multi_comment_sp = Pattern(constants.MULTI_COMMENT_TAG, 
                                   [tokens.tag_multi_comment])
        output_sp = Pattern(constants.OUTPUT_TAG, 
                            [tokens.tag_output_func])
        preprocessor_sp = Pattern(constants.PREPROCESSOR_TAG, 
                                  [tokens.tag_preprocessor], 
                                  carryover=False)
        return_sp = Pattern(constants.RETURN_TAG, 
                            [tokens.tag_return_kw])
        single_comment_sp = Pattern(constants.SINGLE_COMMENT_TAG,
                                    [tokens.tag_single_comment])


        #NOTE: function_declaration MUST be checked BEFORE declaration! 
        #Because declaration essentially checks a subset of function_declaration, if declaration are put before it everything will be identified as declaration.
        patterns = [block_start_sp, block_end_sp, preprocessor_sp, single_comment_sp, multi_comment_sp, 
                    input_sp, output_sp, return_sp, function_sp, function_definition_sp, declaration_sp, conditional_sp,
                    loop_sp, initiation_sp, initiation_pointer_sp]

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

    def translate(self, statement):
        """Translates C TaggedStatement to its JS equivalent."""

        #Define namedtuples needed by helper callbacks & translations
        CallbackPair = namedtuple("CallbackPair", ["trigger", "function"])
        TranslationItem = namedtuple("TranslationItem", ["key", "new_keys", "new_values"])

        #Define helper callbacks here
        array_decl_cb = CallbackPair(tokens.tag_bracket_left, self._helper_declaration)
        input_cb = CallbackPair(tokens.tag_input_func, self._helper_input)
        output_cb = CallbackPair(tokens.tag_output_func, self._helper_output)
        param_cb = CallbackPair(tokens.tag_function_type, self._helper_parameter)
        pointer_cb = CallbackPair(tokens.tag_op_multiply, self._helper_pointer)
        reference_cb = CallbackPair(tokens.tag_op_binary_and, self._helper_reference)

        #Define translations here
        array_prefill_start_tl = TranslationItem(tokens.tag_curly_left, [tokens.tag_bracket_left], [tokens.bracket_left])
        array_prefill_end_tl = TranslationItem(tokens.tag_curly_right, [tokens.tag_bracket_right], [tokens.bracket_right])
        declaration_tl = TranslationItem(tokens.datatypes, [tokens.tag_variable_type], [tokens.variable_type])
        function_tl = TranslationItem(tokens.datatypes, [tokens.tag_function_type], [tokens.function_type])
        printf_tl = TranslationItem(tokens.tag_output_func, 
            [tokens.tag_console_func, tokens.tag_dot, tokens.tag_output_func, tokens.tag_parenthesis_left, tokens.tag_util_func, tokens.tag_dot, tokens.tag_format_func], 
            [tokens.console_func, tokens.dot, tokens.output_func_js, tokens.parenthesis_left, tokens.util_func, tokens.dot, tokens.format_func])
        scanf_tl = TranslationItem(tokens.tag_input_func,
            [tokens.tag_read_func, tokens.tag_dot, tokens.tag_input_func],
            [tokens.read_func, tokens.dot, tokens.input_func_js])

        #Join everything into lists
        default_helpers = [input_cb, output_cb, param_cb, pointer_cb, reference_cb]
        default_translations = [declaration_tl, printf_tl, scanf_tl]
        specific_helpers = []
        specific_translations = []

        #Start translating!
        statement = self._identify(statement)

        #Immediately return if it's unneeded statements (e.g function declaration)
        if not statement.carryover:
            statement.tokens = []
            return statement

        #Add special cases of helpers/translations here
        if statement.tag == constants.FUNCTION_TAG:
            specific_helpers.append(array_decl_cb)
            specific_translations.append(function_tl)
        elif statement.tag == constants.DECLARATION_TAG:
            specific_helpers.append(array_decl_cb)
            specific_translations.extend([array_prefill_start_tl, array_prefill_end_tl])

        #Prioritize special-case helpers and translations. Convert them to dicts first.
        helpers = ChainMap(self._callback_dict(specific_helpers), self._callback_dict(default_helpers))
        translations = ChainMap(self._translation_dict(specific_translations), self._translation_dict(default_translations))

        #Start translating
        result = []
        for token in statement:
            translation = translations.get(token.tag)
            if translation is not None:
                new_tokens = [TaggedToken(new_value, new_key) 
                              for new_key, new_value in zip(translation.new_keys, translation.new_values)]
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

        for helper in helper_functions:
            helper(statement)

        return statement
