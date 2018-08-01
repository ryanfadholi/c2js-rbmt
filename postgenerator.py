import tokendicts as td
import transrules as tr
import sltransfer as slt

from taggedtoken import TaggedToken

js_reserveds = ["catch", "class", "console", "debugger", "delete", "export", "extends", "false", "finally", 
                "function", "import", "in", "instanceof", "let", "new", "null", "super", "this", 
                "throw", "true", "try", "typeof", "util", "var", "with", "yield"]

class PostGenerator:
    def __init__(self, filepath):
        self.filepath = filepath
        self.rules = tr.TranslationHelper()

    def join(self, tokens):
        result = ""

        fspacing = False
        for token in tokens:
            if fspacing and token.bspacing:
                result += " "
            result += token.token
            fspacing = token.fspacing
        
        return result

    def write(self, statements):
        #Decides how many spaces the program should give before writing a line, 1 block depth equals 4 spaces.
        block_depth = 0
        with open(self.filepath, "w") as file_output:
            for statement in statements:
                #Reduce spaces when code block closes.
                if statement.tag == slt.BLOCK_END_TAG:
                    block_depth -= 1

                line = self.join(self.fix(statement).tokens)
                if line: #Only writes if the line is not empty
                    file_output.write("    " * block_depth)
                    file_output.write(line)
                    file_output.write("\n")

                #Add spaces AFTER code block opens, so increment after writing current line.
                if statement.tag == slt.BLOCK_START_TAG:
                    block_depth += 1

    def fix(self, statement):
        #TODO: Only fix first strings inside output functions
        #TODO: Fix strings BEFORE comma, not only the first!
        after_output = False
        before_comma = True

        is_prev_string = False
        new_tokens = []
        for token in statement:
            #Get flag-changing tokens out first.
            if token.tag == td.tag_output_func:
                after_output = True
                before_comma = True
            elif token.tag == td.tag_comma:
                before_comma = False
            elif token.tag == td.tag_val_string:
                #Change C-style formatting characters in the first string (assuming it's a printf format)
                if after_output and before_comma:
                    token.token = self.fix_format(token.token)
                #Add + sign between consecutive strings
                if is_prev_string:
                    new_tokens.append(TaggedToken("+", td.tag_op_add))
            #Fix "reserved" token strings
            elif token.tag == td.tag_name_var:
                if token.token in js_reserveds:
                    token.token = 'a' + token.token
            
            is_prev_string = True if token.tag == td.tag_val_string else False
            new_tokens.append(token)

        statement.tokens = new_tokens
        return statement
        
    def fix_format(self, string):
        kdigits_three = (["%lli"], 4, "%d")
        kdigits_two = (["%hi", "%li"], 3, "%d")
        kdigits_one = (["%f", "%i"], 2, "%d")
        kchar = (["%c"], 2, "%s")

        formatting_guides = [kdigits_three, kdigits_two, kdigits_one, kchar]

        for keys, tlen, new_format in formatting_guides:
            while True:
                tpos = self.rules.findfirst(string, keys)
                if tpos == -1:
                    break
                lstr, rstr = string[:tpos], string[tpos+tlen:]
                string = lstr + new_format + rstr

        return string
