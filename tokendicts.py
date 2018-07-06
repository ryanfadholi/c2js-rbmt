if_conditional = "if"; tag_if_conditional = "if-cond"
else_conditional = "else"; tag_else_conditional = "else-cond"

char_type = "char"; tag_char_type = "char-type"
double_type = "double"; tag_double_type = "double-type"
float_type = "float" ; tag_float_type = "float-type" 
int_type = "int"; tag_int_type = "int-type"
long_type = "long"; tag_long_type = "long-type" 
short_type = "short"; tag_short_type = "short-type" 

dowhile_loop = "do"; tag_dowhile_loop = "dowhile-loop"
for_loop = "for"; tag_for_loop = "for-loop"
while_loop = "while"; tag_while_loop = "while-loop"

output_func = "printf"; tag_output_func = "output-function"
input_func = "scanf"; tag_input_func = "input-function"

include_kw = "include"; tag_include_kw = "include-keyword"
return_kw = "return"; tag_return_kw = "return-keyword"

single_comment = "//"; tag_single_comment = "single-comment" 
multi_comment = "/*"; tag_multi_comment = "multi-comment"
multi_comment_end = "*/"; tag_multi_comment_end = "multi-comment-end" 

assign = "="; tag_assign = "assign"
comma = ","; tag_comma = "comma"
preprocessor = "#"; tag_preprocessor = "preprocessor"
pointer = "*"; tag_pointer = "pointer"
semicolon = ";"; tag_semicolon = "semicolon"
single_quote = "'"; tag_single_quote = "single-quote"
double_quote = "\""; tag_double_quote = "double-quote"
bracket_left = "["; tag_bracket_left = "bracket-left" 
bracket_right = "]"; tag_bracket_right = "bracket-right"
curly_left = "{"; tag_curly_left = "curly-left"
curly_right = "}"; tag_curly_right = "curly-right"
parenthesis_left = "("; tag_parenthesis_left = "parenthesis-left"
parenthesis_right = ")"; tag_parenthesis_right = "parenthesis-right"

op_add = "+"; tag_op_add = "op-add" 
op_minus = "-"; tag_op_minus = "op-minus"
op_multiply = "*"; tag_op_multiply = "op-multiply"
op_divide = "/"; tag_op_divide = "op-divide" 
op_modulo = "%"; tag_op_modulo = "op-modulo"
op_increment = "++"; tag_op_increment = "op-increment"
op_decrement = "--"; tag_op_decrement = "op-decrement"

op_eq = "=="; tag_op_eq = "op-equal"
op_not_eq = "!="; tag_op_not_eq = "op-not-equal"
op_gt_eq = ">="; tag_op_gt_eq = "op-greater-equal"
op_lt_eq = "<="; tag_op_lt_eq = "op-less-equal"
op_gt = ">"; tag_op_gt = "op-greater"
op_lt = "<"; tag_op_lt = "op-less"

op_comp_add = "+="; tag_op_comp_add = "op-compound-add"
op_comp_minus = "-="; tag_op_comp_minus = "op-compound-minus"
op_comp_multiply = "*="; tag_op_comp_multiply = "op-compound-multiply"
op_comp_divide = "/="; tag_op_comp_divide = "op-compound-divide"
op_comp_modulo = "%="; tag_op_comp_modulo = "op-compound-modulo"
op_comp_and = "&="; tag_op_comp_and = "op-compound-and" 
op_comp_or = "|="; tag_op_comp_or = "op-compound-or"
op_comp_xor = "^="; tag_op_comp_xor = "op-compound-xor"
op_comp_lshift = "<<="; tag_op_comp_lshift = "op-compound-lshift"
op_comp_rshift = ">>="; tag_op_comp_rshift = "op-compound-rshift"

op_not = "!"; tag_op_not = "op-not"
op_and = "&&"; tag_op_and = "op-and"
op_or = "||"; tag_op_or = "op-or"

op_binary_and = "&"; tag_op_binary_and = "op-binary-and"
op_binary_or = "|"; tag_op_binary_or = "op-binary-or"
op_binary_xor = "^"; tag_op_binary_xor = "op-binary-xor"
op_binary_flip = "~"; tag_op_binary_flip = "op-binary-flip"
op_lshift = "<<"; tag_op_left_shift = "op-left-shift" 
op_rshift = ">>"; tag_op_right_shift = "op-right-shift"

#lists every tokens with more than one character
multichar_symbol = [
    op_comp_lshift, op_comp_rshift, single_comment, multi_comment, multi_comment_end, op_eq, 
    op_not_eq, op_gt_eq, op_lt_eq, op_and, op_or, op_increment, op_decrement, 
    op_comp_add, op_comp_minus, op_comp_multiply, op_comp_divide, 
    op_comp_modulo, op_comp_and, op_comp_or, op_comp_xor, op_lshift, op_rshift
]

#Every dynamically-determined tokens key goes here
tag_name_preproc = "preprocessor-name"
tag_name_var = "variable-name"
tag_val_char = "char-value"
tag_val_float = "float-value"
tag_val_int = "int-value"
tag_val_string = "string-value"

arithmetic_operator = {
    tag_op_add : op_add,
    tag_op_minus : op_minus,
    tag_op_multiply : op_multiply,
    tag_op_divide : op_divide,
    tag_op_modulo : op_modulo,
    tag_op_increment : op_increment,
    tag_op_decrement : op_decrement
}

bitwise_operator = {
    tag_op_binary_or : op_binary_or,
    tag_op_binary_and : op_binary_and,
    tag_op_binary_xor : op_binary_xor,
    tag_op_binary_flip : op_binary_flip,
    tag_op_left_shift : op_lshift,
    tag_op_right_shift : op_rshift
}

relational_operator = {
    tag_op_eq : op_eq,
    tag_op_not_eq : op_not_eq,
    tag_op_gt_eq : op_gt_eq,
    tag_op_lt_eq : op_lt_eq,
    tag_op_gt : op_gt,
    tag_op_lt : op_lt
}

#Max operator length: 3
compound_assignment_operator = {
    tag_op_comp_add : op_comp_add,
    tag_op_comp_minus : op_comp_minus,
    tag_op_comp_multiply : op_comp_multiply,
    tag_op_comp_divide : op_comp_divide,
    tag_op_comp_modulo : op_comp_modulo,
    tag_op_comp_and : op_comp_and,
    tag_op_comp_or : op_comp_or,
    tag_op_comp_xor : op_comp_xor,
    tag_op_comp_lshift : op_comp_lshift,
    tag_op_comp_rshift : op_comp_rshift
}

logical_operator = {
    tag_op_not : op_not,
    tag_op_and : op_and,
    tag_op_or : op_or
}

misc_operator = {
    tag_assign : assign,
    tag_comma : comma,
    tag_preprocessor : preprocessor,
    tag_pointer : pointer,
    tag_semicolon : semicolon,
    tag_single_quote : single_quote,
    tag_double_quote : double_quote,
    tag_bracket_left : bracket_left,
    tag_bracket_right : bracket_right,
    tag_curly_left : curly_left,
    tag_curly_right : curly_right,
    tag_parenthesis_left : parenthesis_left,
    tag_parenthesis_right : parenthesis_right,
}

comments = {
    tag_single_comment : single_comment,
    tag_multi_comment : multi_comment,
    tag_multi_comment_end : multi_comment_end
}
 
conditionals = {
    tag_if_conditional : if_conditional,
    tag_else_conditional : else_conditional
}

datatypes = {
    tag_char_type :char_type, 
    tag_double_type : double_type,
    tag_float_type : float_type,
    tag_int_type: int_type,
    tag_long_type: long_type,
    tag_short_type: short_type
}
  
loops = {
    tag_dowhile_loop : dowhile_loop, 
    tag_for_loop : for_loop, 
    tag_while_loop : while_loop
}

special_functions = {
    tag_output_func : output_func,
    tag_input_func : input_func
}

keywords = {
    tag_include_kw : include_kw,
    tag_return_kw : return_kw
}
