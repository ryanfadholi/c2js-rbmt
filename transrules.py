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

op_add = "+"
op_minus = "-"
op_multiply = "*"
op_divide = "/"

compound_add = "+="
compound_minus = "-="
compound_multiply = "*="
compound_divide = "/="

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

compound_assignment = {
    "compound-add" : compound_add,
    "compound-minus" : compound_minus,
    "compound-multiply" : compound_multiply,
    "compound-divide" : compound_divide
}

loops = {
    "dowhile-loop" : dowhile_loop, 
    "for-loop" : for_loop, 
    "while-loop" : while_loop
    }

logical_operator = {}
decrement = "--"
increment = "++"

