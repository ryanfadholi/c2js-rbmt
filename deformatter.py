import transrules as rules

#TODO: delete all unnecessary commented print-debugs! 

class Deformat:

    _tempfile_path = "temp/source.txt"

    def __init__(self, filepath):
        self.rules = rules.TranslationHelper()        

        #Prepare the temporary file
        self._filepath = filepath
        self._readfile()

    # def _determine_genera_end()

    def _determine_decl_end(self, text):
        """
        Determines whether a declaration sentence ends with "{" or ";", 
        or in other words, whether it's a variable or function declaration
        """        
        curlybrace_pos = text.find("{")
        semicolon_pos = text.find(";")

        if curlybrace_pos > 0 and curlybrace_pos < semicolon_pos:
            return "{"
        else:
            return ";"

    def _determine_bracket_end(self, text):
        # print(f"determine_bracket_end called, the text: {text}")
        first_open_bracket = text.find("(")
    
        if first_open_bracket == -1:
            return -1
        else:
            char_idx = first_open_bracket+1

            bracket_end_idx = -1
            open_bracket_count = 1

            while(char_idx < len(text)):
                cur_char = text[char_idx]
                if cur_char == "(":
                    open_bracket_count += 1
                elif cur_char == ")":
                    open_bracket_count -= 1
                
                if open_bracket_count == 0:
                    
                    bracket_end_idx = char_idx
                    break

                char_idx += 1
        bracket_closed = open_bracket_count == 0
        # print(f"is bracket closed? {bracket_closed}")

        if bracket_closed:
            # print(f"bracket closed at {bracket_end_idx + 1} from {len(text)} chars")
            return bracket_end_idx + 1
        else:
            return -1

    def _determine_block_end(self, text):
        #TODO: Correctly handle conditionals/loops separated by comments!
        print(f"determine_block_end called, the text: {text}")
        first_open_bracket = text.find("(")
    
        if first_open_bracket == -1:
            return -1
        else:
            char_idx = first_open_bracket+1

            bracket_end_idx = -1
            open_bracket_count = 1

            while(char_idx < len(text)):
                cur_char = text[char_idx]
                if cur_char == "(":
                    open_bracket_count += 1
                elif cur_char == ")":
                    open_bracket_count -= 1
                
                if open_bracket_count == 0:
                    
                    bracket_end_idx = char_idx
                    break

                char_idx += 1
        bracket_closed = open_bracket_count == 0
        one_liner = False

        if(bracket_closed):
            char_idx = bracket_end_idx+1
            unfinished_comment = False
            comment_check = self.rules.findcomment(text[char_idx:])
            if comment_check > -1:
                cut_comment = self.stmt_cutter(text[comment_check:])
                if cut_comment > -1:
                    char_idx = char_idx + comment_check + cut_comment
                    print(f"comment found! jump to {char_idx} from {len(text)} characters")
                else:
                    unfinished_comment = True

            while(char_idx < len(text) and not unfinished_comment):
                cur_char = text[char_idx]
                if(not (cur_char == " " or cur_char == "{")):
                    one_liner = True
                    break 

                char_idx += 1
    
        if one_liner:
            return bracket_end_idx + 1 
        else:
            separator = "{"
            sep_pos = text.find(separator)        
            offset = len(separator) #Determine the offset
            cut_pos = sep_pos + offset if sep_pos > -1 else -1
            return cut_pos 


    def _extract_substmt(self, text):
        """
        Extracts comments inserted inside a statement.
        Returns the statement (and any comments found) as a list.
        """
        original_text = text

        substmts = []

        #if it's comments or include statements, no need to reanalyze statement.
        if self.rules.is_singlecomment(text) or self.rules.is_multicomment(text) or self.rules.is_include(text):
            pass 
        else:
            while self.rules.findcomment(text) > -1:
                # print(f"original text is: {original_text} ~")
                # print(f"text is: {text} ~")
                start_cut = self.rules.findcomment(text)
                cut_len = self.stmt_cutter(text[start_cut:])
                end_cut = start_cut + cut_len
                #text on the left side are right-stripped and the text on the right are left-stripped,
                #to cut any extra whitespace/next lines between them.
                comment, text = text[start_cut:end_cut], text[:start_cut].rstrip() + " " + text[end_cut:].lstrip()
                substmts.append(comment)

        substmts.append(text)
        return map(lambda text: text.strip(), substmts)


    def stmt_cutter(self, text):
        """Determine where a statement ends and its separator.
        Returns the correct ending character for the line string, according
        to the first characters of the string.
        """

        #TODO: Refactor as in the paper, add whitespace_offset variable.
        line = str(text).lstrip()

        #Get special case out of the way first (if it's a conditional/loop statement)
        if self.rules.is_conditional(line) or self.rules.is_loop(line):
            if self._determine_bracket_end(line) > -1:
                return self._determine_bracket_end(line) + (len(str(text)) - len(str(text).lstrip()))
            else:
                return -1

        separator = ""
        if self.rules.is_singlecomment(line) or self.rules.is_include(line):
            separator = '\n'
        elif self.rules.is_multicomment(line):
            separator = '*/'
        elif self.rules.is_block_end(line):
            separator = '}'
        elif self.rules.is_declaration(line):
            separator = self._determine_decl_end(line)
        # elif self.rules.is_conditional(line) or self.rules.is_loop(line):
        #     separator = "{"
        else: 
            separator = ';'

        sep_pos = text.find(separator)        
        offset = len(separator) #Determine the offset
        cut_pos = sep_pos + offset if sep_pos > -1 else -1
        return cut_pos

    def findfirst(self, text, tokens):
        """
        Find the first instance of any token from the tokens list on the text string. 
        Returns -1 when there is no instance of any token in the string.
        """

        if isinstance(tokens, dict):
            findall = [text.find(token) for key, token in tokens.items()]
        elif isinstance(tokens, list):
            findall = [text.find(token) for token in tokens]
        
        found = list(filter(lambda pos: pos > -1, findall))

        return min(found) if len(found) > 0 else -1

    def _readfile(self):
        """
        Reads file located in self._filepath, and rewrites it
        into the designated path (self._tempfile_path).
        """

        with open(self._filepath, "r") as file_input:
            
            raw_input = file_input.read()
            with open(self._tempfile_path, "w") as temp_file:
                temp_file.write(raw_input)

    def _lines_generator(self):
        """Reads temporary file per-line."""
        with open(self._tempfile_path) as file:
            for line in file:
                yield line

    def _statements_generator(self):
        """Returns temporary file's content as an iterable of separated C statements."""

        prev_line = ""

        for line in self._lines_generator():
            cur_line = prev_line + line
            while len(cur_line) > 0:
                cut_pos = self.stmt_cutter(cur_line)  

                if cut_pos == -1:
                    break
                else:
                    # print(f"{cur_line[:cut_pos]}, {cur_line[cut_pos:]}")
                    next_stmt, cur_line = cur_line[:cut_pos], cur_line[cut_pos:]
                    for stmt in self._extract_substmt(next_stmt.strip()):
                        #Scrap empty strings.
                        if len(stmt) > 0:
                            yield stmt
            
            prev_line = cur_line

        if len(prev_line) > 0:
            yield prev_line.strip()

        raise StopIteration 

    @property
    def lines(self):
        return [line for line in self._lines_generator()]

if __name__ == "__main__":
    #When run, run c2js instead
    import c2js