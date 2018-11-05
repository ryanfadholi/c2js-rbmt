#Javascript keywords & functions
variable_type = "var";  tag_variable_type = "variable-type"
function_type = "function"; tag_function_type = "function-type"
number_type = "Number"; tag_number_type = "number-type"
process_func = "process"; tag_process_func = "process-module"
stdout_func = "stdout"; tag_stdout_func = "stdout-module"
util_func = "util"; tag_util_func = "utility-module"
format_func = "format"; tag_format_func = "format-function"
read_func = "readlineSync"; tag_read_func = "readline-module"
ptr_access = "ptr"; tag_ptr_access = "pointer-access"
math_func = "Math"; tag_math_func = "math-module"
trunc_func = "trunc"; tag_trunc_func = "truncate-function"

if_conditional = "if"; tag_if_conditional = "if-cond"
else_conditional = "else"; tag_else_conditional = "else-cond"

char_type = "char"; tag_char_type = "char-type"
double_type = "double"; tag_double_type = "double-type"
float_type = "float" ; tag_float_type = "float-type" 
int_type = "int"; tag_int_type = "int-type"
long_type = "long"; tag_long_type = "long-type" 
short_type = "short"; tag_short_type = "short-type" 
void_type = "void"; tag_void_type = "void-type"

dowhile_loop = "do"; tag_dowhile_loop = "dowhile-loop"
for_loop = "for"; tag_for_loop = "for-loop"
while_loop = "while"; tag_while_loop = "while-loop"

output_func = "printf"; output_func_js = "write"; tag_output_func = "output-function"
input_func = "scanf"; input_func_js = "question"; tag_input_func = "input-function"
rand_func = "rand"; tag_rand_func = "random-function"
pow_func = "pow"; tag_pow_func = "power-function"
sizeof_func = "sizeof"; tag_sizeof_lib = "sizeof-module"; tag_sizeof_func = "sizeof-function"
sqrt_func = "sqrt"; tag_sqrt_func = "sqrt-function"

abs_func = "abs"; tag_abs_func = "absolute-function"
cos_func = "cos"; tag_cos_func = "cos-function"
fabs_func = "fabs"; tag_fabs_func = "float-absolute-function"
sin_func = "sin"; tag_sin_func = "sin-function"
srand_func = "srand"; tag_srand_func = "random-seed-function"
tan_func = "tan"; tag_tan_func = "tan-function"


break_kw = "break"; tag_break_kw = "break-keyword"
case_kw = "case"; tag_case_kw = "switch-case"
continue_kw = "continue"; tag_continue_kw = "continue-keyword"
default_kw = "default"; tag_default_kw = "default-keyword"
define_kw = "define"; tag_define_kw = "define-keyword"
include_kw = "include"; tag_include_kw = "include-keyword"
return_kw = "return"; tag_return_kw = "return-keyword"
switch_kw = "switch"; tag_switch_kw = "switch-keyword"

single_comment = "//"; tag_single_comment = "single-comment" 
multi_comment = "/*"; tag_multi_comment = "multi-comment"
multi_comment_end = "*/"; tag_multi_comment_end = "multi-comment-end" 

assign = "="; tag_assign = "assign"
colon = ":"; tag_colon = "colon"
comma = ","; tag_comma = "comma"
dot = "."; tag_dot = "dot"
preprocessor = "#"; tag_preprocessor = "preprocessor"
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

#Every dynamically-determined tokens key goes here
tag_name_preproc = "preprocessor-name"
tag_name_var = "variable-name"
tag_val_char = "char-value"
tag_val_float = "float-value"
tag_val_int = "int-value"
tag_val_string = "string-value"

#lists every tokens with more than one character
multichar_symbol = [
    op_comp_lshift, op_comp_rshift, single_comment, multi_comment, multi_comment_end, op_eq,
    op_not_eq, op_gt_eq, op_lt_eq, op_and, op_or, op_increment, op_decrement,
    op_comp_add, op_comp_minus, op_comp_multiply, op_comp_divide,
    op_comp_modulo, op_comp_and, op_comp_or, op_comp_xor, op_lshift, op_rshift
]

parsing_exceptions = [
    single_comment, multi_comment, single_quote, double_quote
]

string_identifiers = [
    single_quote, double_quote
]

possible_lefthand_operations = [tag_name_var, tag_val_char, tag_val_float, tag_val_int, tag_val_string, tag_parenthesis_right, tag_bracket_right]

round_datatypes = [tag_int_type, tag_long_type, tag_short_type]

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
    tag_dot : dot,
    tag_preprocessor : preprocessor,
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
    tag_else_conditional : else_conditional,
}

datatypes = {
    tag_char_type :char_type, 
    tag_double_type : double_type,
    tag_float_type : float_type,
    tag_int_type: int_type,
    tag_long_type: long_type,
    tag_short_type: short_type,
    tag_void_type: void_type
}
  
loops = {
    tag_dowhile_loop : dowhile_loop, 
    tag_for_loop : for_loop, 
    tag_while_loop : while_loop
}

special_functions = {
    tag_output_func : output_func,
    tag_input_func : input_func,
    tag_pow_func : pow_func,
    tag_rand_func : rand_func,
    tag_srand_func : srand_func,
    tag_sizeof_func : sizeof_func,
    tag_sqrt_func : sqrt_func,
    
    tag_abs_func : abs_func,
    tag_cos_func : cos_func,
    tag_fabs_func : fabs_func,
    tag_tan_func : tan_func,
    tag_sin_func : sin_func
}

keywords = {
    tag_break_kw : break_kw,
    tag_case_kw : case_kw,
    tag_continue_kw : continue_kw,
    tag_default_kw : default_kw,
    tag_define_kw : define_kw,
    tag_include_kw : include_kw,
    tag_return_kw : return_kw,
    tag_switch_kw : switch_kw 
}


