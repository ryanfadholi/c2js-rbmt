import constants
import tokens
import os

from taggedtoken import TaggedToken

JS_RESERVED = ["catch", "class", "console", "debugger", "delete", "export", "extends", "false", "finally", 
               "function", "import", "in", "instanceof", "let", "new", "null", "super", "this", 
               "throw", "true", "try", "typeof", "util", "var", "with", "yield"]

ADD_TOKEN = TaggedToken(tokens.op_add, tokens.tag_op_add)

class PostGenerator:
    
    def _fix(self, statement):
        """Corrects JS-side translation errors."""
        after_output = False
        before_comma = True

        is_prev_string = False
        new_tokens = []
        for token in statement:
            #Get flag-changing tokens out first.
            if token.tag == tokens.tag_output_func:
                after_output = True
                before_comma = True
            elif token.tag == tokens.tag_comma:
                before_comma = False
            elif token.tag == tokens.tag_val_string:
                #Change C-style formatting characters in the first string (assuming it's a printf format)
                if after_output and before_comma:
                    token.token = self._reformat(token.token)
                #Add + sign between consecutive strings
                if is_prev_string:
                    new_tokens.append(ADD_TOKEN)
            #Fix "reserved" token strings
            elif token.tag == tokens.tag_name_var:
                if token.token in JS_RESERVED:
                    token.token = 'a' + token.token
            
            is_prev_string = True if token.tag == tokens.tag_val_string else False
            new_tokens.append(token)

        statement.tokens = new_tokens
        return statement

    def _join(self, token_list):
        """Joins a list of tokens into string."""
        result = ""

        fspacing = False
        for token in token_list:
            if fspacing and token.bspacing:
                result += " "
            result += token.token
            fspacing = token.fspacing
        
        return result

    def _nearest(self, statement_tokens, text):
        """
        Find the first instance of any token from the statement_tokens list on the text string.
        Returns -1 when there is no instance of any token in the string.
        """

        nearest_each = [text.find(token) for token in statement_tokens]
        found = list(filter(lambda pos: pos > -1, nearest_each))

        return min(found) if found else -1
    
    def _reformat(self, string):
        """
        Converts C formatting characters unknown by JS (for example "%f" for float) to its nearest equivalence in JS.
        """

        #Define the mappings
        kdigits_three = (["%lli"], 4, "%d")
        kdigits_two = (["%hi", "%li", "%lf"], 3, "%d")
        kdigits_one = (["%i"], 2, "%d")
        kchar = (["%c"], 2, "%s")

        formatting_guides = [kdigits_three, kdigits_two, kdigits_one, kchar]

        for keys, tlen, new_format in formatting_guides:
            while True:
                #Check for any occurrence of the formatting characters
                tpos = self._nearest(keys, string)
                if tpos == -1:
                    break
                #Cut and paste the correct one
                lstr, rstr = string[:tpos], string[tpos+tlen:]
                string = lstr + new_format + rstr

        return string

    def _requirements(self, statements):
        """Returns a list of libraries required for statements to run correctly."""
        input_lib = False
        output_lib = False
        rand_lib = False
        sizeof_lib = False

        for statement in statements:
            if statement.tag == constants.INPUT_TAG:
                input_lib = True
            elif statement.tag == constants.OUTPUT_TAG:
                output_lib = True

            if False in [rand_lib, sizeof_lib]:
                for token in statement:
                    if token.tag == tokens.tag_rand_func:
                        rand_lib = True
                    elif token.tag == tokens.tag_sizeof_func:
                        sizeof_lib = True
                        
        line_count = 0
        to_write = []
        if input_lib:
            to_write.append("var readlineSync = require('readline-sync')")
            line_count += 1
        if output_lib:
            to_write.append("var util = require('util')")
            line_count += 1
        if sizeof_lib:
            to_write.append("var sizeof = require('sizeof')")
            line_count += 1
        if rand_lib:
            to_write.append("function rand() {")
            to_write.append("   return Math.floor(Math.random() * Math.floor(32767));")
            to_write.append("}")
            line_count += 4

        return (line_count, to_write)

    def write(self, statements):
        """Writes a list of TaggedStatement into the designated temporary file."""
        #Decides how many spaces the program should give before writing a line, 1 block depth equals 4 spaces.
        block_depth = 0
        total_lines = 0
        with open(constants.OUTPUT_TEMPFILE_PATH, "w") as output:

            lib_lines, libs = self._requirements(statements)
            for lib in libs:
                output.write(lib)
                output.write("\n")
            if libs:
                output.write("\n")
            total_lines += lib_lines

            for statement in statements:
                #Reduce spaces when code block closes.
                if statement.tag == constants.BLOCK_END_TAG:
                    block_depth -= 1

                line = self._join(self._fix(statement).tokens)
                if line: #Only writes if the line is not empty
                    output.write("    " * block_depth)
                    output.write(line)
                    output.write("\n")
                    total_lines += 1
                    #Add an empty line for each block ends
                    if statement.tag == constants.BLOCK_END_TAG:
                        output.write("\n")        

                #Add spaces AFTER code block opens, so increment after writing current line.
                if statement.tag == constants.BLOCK_START_TAG:
                    block_depth += 1

            #Run main function at the end of the script!
            output.write("main();")
            total_lines += 1

            return total_lines
