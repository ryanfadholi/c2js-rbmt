#TODO: Convert everything to dictionary

conditionals = ["if", "else"]
datatypes = ["char", "double" ,"float", "int", "long", "short"]

block_start = "{"
block_end = "}"

include = "#"

dowhile_loop = "do"
for_loop = "for"
while_loop = "while"

single_comment = "//"
multi_comment = "/*"

op_decrement = "--"
op_increment = "++"

op_assign = "="

op_add = "+"
op_minus = "-"
op_multiply = "*"
op_divide = "/"

op_eq = "=="
op_not_eq = "!="
op_gt_eq = ">="
op_lt_eq = "<="

op_not = "!"
op_and = "&&"
op_or = "||"

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

op_lshift = "<<"
op_rshift = ">>"

#lists every tokens with more than one character
multichar_symbol = [
    op_comp_lshift, op_comp_rshift, single_comment, multi_comment, op_eq, 
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

comments = {
    "single-comment" : single_comment,
    "multi-comment" : multi_comment
}

#Max operator length: 3
op_comp_assignment = {
    "op-compound-lshift" : op_comp_lshift,
    "op-compound-rshift" : op_comp_rshift,
    "op-compound-add" : op_comp_add,
    "op-compound-minus" : op_comp_minus,
    "op-compound-multiply" : op_comp_multiply,
    "op-compound-divide" : op_comp_divide,
    "op-compound-modulo" : op_comp_modulo,
    "op-compound-and" : op_comp_and,
    "op-compound-or" : op_comp_or
}

loops = {
    "dowhile-loop" : dowhile_loop, 
    "for-loop" : for_loop, 
    "while-loop" : while_loop
    }

logical_operator = {
    "not-op" : op_not,
    "and-op" : op_and,
    "or-op" : op_or
}

