import tokendicts as td
import transrules as tr
js_reserveds = ["catch", "class", "debugger", "delete", "export", "extends", "false", "finally", 
                "function", "import", "in", "instanceof", "let", "new", "null", "super", "this", 
                "throw", "true", "try", "typeof", "var", "with", "yield"]

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
        #TODO: Add four spaces each time the function enters a new block.
        with open(self.filepath, "w") as file_output:
            for statement in statements:
                line = self.join(self.fix(statement).tokens)
                if line: #Only writes if the line is not empty
                    file_output.write(line)
                    file_output.write("\n")

    def fix(self, statement):
        #TODO: Fix multiple direct occurrences of string!
        #TODO: Fix "reserved" variable name in Javascript
        for token in statement:
            if token.tag == td.tag_val_string:
                token.token = self.fix_format(token.token)
            elif token.tag == td.tag_name_var:
                if token.token in js_reserveds:
                    token.token = 'a' + token.token
        return statement
        
    def fix_format(self, string):
        digits_three = (["%lli"], 4, "%d")
        digits_two = (["%hi", "%li"], 3, "%d")
        digits_one = (["%f", "%i"], 2, "%d")
        char = (["%c"], 2, "%s")

        format_keys = [digits_three, digits_two, digits_one, char]

        for keys, tlen, new_format in format_keys:
            while True:
                tpos = self.rules.findfirst(string, keys)
                if tpos == -1:
                    break
                lstr, rstr = string[:tpos], string[tpos+tlen:]
                string = lstr + new_format + rstr

        return string
