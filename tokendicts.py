#TODO: Convert everything to dictionary
#TODO: Register every tokens and keywords needed.

if_conditional = "if"
else_conditional = "else"

char_type = "char"
double_type = "double"
float_type = "float" 
int_type = "int"
long_type = "long"
short_type = "short"

dowhile_loop = "do"
for_loop = "for"
while_loop = "while"

output_func = "printf"
input_func = "scanf"

single_comment = "//"
multi_comment = "/*"
multi_comment_end = "*/"

assign = "="
comma = ","
include = "#"
pointer = "*"
semicolon = ";"
single_quote = "'"
double_quote = "\""
bracket_left = "["
bracket_right = "]"
curly_left = "{"
curly_right = "}"
parenthesis_left = "("
parenthesis_right = ")"

op_add = "+"
op_minus = "-"
op_multiply = "*"
op_divide = "/"
op_modulo = "%"
op_increment = "++"
op_decrement = "--"

op_eq = "=="
op_not_eq = "!="
op_gt_eq = ">="
op_lt_eq = "<="
op_gt = ">"
op_lt = "<"

op_comp_add = "+="
op_comp_minus = "-="
op_comp_multiply = "*="
op_comp_divide = "/="
op_comp_modulo = "%="
op_comp_and = "&="
op_comp_or = "|="
op_comp_xor = "^="
op_comp_lshift = "<<="
op_comp_rshift = ">>="

op_not = "!"
op_and = "&&"
op_or = "||"

op_binary_and = "&"
op_binary_or = "|"
op_binary_xor = "^"
op_binary_flip = "~"
op_lshift = "<<"
op_rshift = ">>"

bitwise_operator = {
    "op-binary-and" : op_binary_and,
    "op-binary-or" : op_binary_or,
    "op-binary-xor" : op_binary_xor,
    "op-binary-flip" : op_binary_flip,
    "op-left-shift" : op_lshift,
    "op-right-shift" : op_rshift
}

#lists every tokens with more than one character
multichar_symbol = [
    op_comp_lshift, op_comp_rshift, single_comment, multi_comment, multi_comment_end, op_eq, 
    op_not_eq, op_gt_eq, op_lt_eq, op_and, op_or, op_increment, op_decrement, 
    op_comp_add, op_comp_minus, op_comp_multiply, op_comp_divide, 
    op_comp_modulo, op_comp_and, op_comp_or, op_comp_xor, op_lshift, op_rshift
]

arithmetic_operator = {
    "op-add" : op_add,
    "op-minus" : op_minus,
    "op-multiply" : op_multiply,
    "op-divide" : op_divide
}

misc_operator = {
    "assign" : assign,    
    "comma" : comma,
    "pointer" : pointer,
    "semicolon" : semicolon,
    "single-quote" : single_quote,
    "double-quote" : double_quote,
    "bracket-left" : bracket_left,
    "bracket-right" : bracket_right,
    "curly-left" : curly_left,
    "curly-right" : curly_right,
    "parenthesis-left" : parenthesis_left,
    "parenthesis-right" : parenthesis_right,
}

relational_operator = {
    "op-equal" : op_eq,
    "op-not-equal" : op_not_eq,
    "op-greater-equal" : op_gt_eq,
    "op-less-equal" : op_lt_eq,
    "op-greater" : op_gt,
    "op-less" : op_lt
}

comments = {
    "single-comment" : single_comment,
    "multi-comment" : multi_comment,
    "multi-comment-end" : multi_comment_end
}

#Max operator length: 3
compound_assignment_operator = {
    "op-compound-add" : op_comp_add,
    "op-compound-minus" : op_comp_minus,
    "op-compound-multiply" : op_comp_multiply,
    "op-compound-divide" : op_comp_divide,
    "op-compound-modulo" : op_comp_modulo,
    "op-compound-and" : op_comp_and,
    "op-compound-or" : op_comp_or,
    "op-compound-lshift" : op_comp_lshift,
    "op-compound-rshift" : op_comp_rshift
}

logical_operator = {
    "op-not" : op_not,
    "op-and" : op_and,
    "op-or" : op_or
}

conditionals = {
    "if-cond" : if_conditional,
    "else-cond" : else_conditional
}

datatypes = {
    "char-type" :char_type, 
    "double-type" : double_type,
    "float-type" : float_type,
    "int-type": int_type,
    "long-type": long_type,
    "short-type": short_type
}
  
loops = {
    "dowhile-loop" : dowhile_loop, 
    "for-loop" : for_loop, 
    "while-loop" : while_loop
    }

special_functions = {
    "output-function" : output_func,
    "input-function" : input_func
}
