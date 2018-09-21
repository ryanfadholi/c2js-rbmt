import tokens
import sltransfer as slt

from taggedtoken import TaggedToken

JS_RESERVED = ["catch", "class", "console", "debugger", "delete", "export", "extends", "false", "finally", 
               "function", "import", "in", "instanceof", "let", "new", "null", "super", "this", 
               "throw", "true", "try", "typeof", "util", "var", "with", "yield"]

TEMPFILE_PATH = "temp/result.txt"

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
                    new_tokens.append(TaggedToken("+", tokens.tag_op_add))
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

    def _nearest(self, tokens, text):
        """
        Find the first instance of any token from the tokens list on the text string.
        Returns -1 when there is no instance of any token in the string.
        """

        nearest_each = [text.find(token) for token in tokens]
        found = list(filter(lambda pos: pos > -1, nearest_each))

        return min(found) if found else -1
        
    def _reformat(self, string):
        """
        Converts C formatting characters unknown by JS (for example "%f" for float) to its nearest equivalence in JS.
        """

        #Define the mappings
        kdigits_three = (["%lli"], 4, "%d")
        kdigits_two = (["%hi", "%li"], 3, "%d")
        kdigits_one = (["%f", "%i"], 2, "%d")
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

        for statement in statements:
            if statement.tag == slt.INPUT_TAG:
                input_lib = True
            elif statement.tag == slt.OUTPUT_TAG:
                output_lib = True

        to_write = []
        if input_lib:
            to_write.append("var readlineSync = require('readline-sync')")
        if output_lib:
            to_write.append("var util = require('util')")

        return to_write

    def write(self, statements):
        """Writes a list of TaggedStatement into the designated temporary file."""
        #Decides how many spaces the program should give before writing a line, 1 block depth equals 4 spaces.
        block_depth = 0
        with open(TEMPFILE_PATH, "w") as output:

            libs = self._requirements(statements)
            for lib in libs:
                output.write(lib)
                output.write("\n")

            for statement in statements:
                #Reduce spaces when code block closes.
                if statement.tag == slt.BLOCK_END_TAG:
                    block_depth -= 1

                line = self._join(self._fix(statement).tokens)
                if line: #Only writes if the line is not empty
                    output.write("    " * block_depth)
                    output.write(line)
                    output.write("\n")
                    #Add an empty line for each block ends
                    if statement.tag == slt.BLOCK_END_TAG:
                        output.write("\n")

                #Add spaces AFTER code block opens, so increment after writing current line.
                if statement.tag == slt.BLOCK_START_TAG:
                    block_depth += 1

            #Run main function at the end of the script!
            output.write("main();")
