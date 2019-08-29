import math as mt
import numpy as np
import argparse
import re
from inspect import signature


def get_module_func(module):

"""
    get module functions
"""

   object_arr = [i for i in dir(module) if not(i.startswith("__"))]
    return {i: getattr(mt, i) for i in object_arr if type(getattr(mt, i)) != float}


def get_module_const(module):

"""
    get module constants
"""
   object_arr = [i for i in dir(module) if not(i.startswith("__"))]
    return {i: getattr(mt, i) for i in object_arr if type(getattr(mt, i)) == float}


basic_operators = {"+": lambda x, y: x+y,
                   "-": lambda x, y: x-y,
                   "*": lambda x, y: x*y,
                   "/": lambda x, y: x/y,
                   "%": lambda x, y: x % y,
                   "^": lambda x, y: x**y,
                   "+": lambda x, y: x+y,
                   "<": lambda x, y: int(x < y),
                   ">": lambda x, y: int(x > y),
                   "<": lambda x, y: int(x < y)
                   }

compound_operators = {
    "//": lambda x, y: x//y,
    "<=": lambda x, y: int(x <= y),
    ">=": lambda x, y: int(x >= y),
    "!=": lambda x, y: int(x != y),
    "==": lambda x, y: int(x == y)}

priority_dict = {'+': 2,
                 '-': 2,
                 '*': 3,
                 '/': 3,
                 '//': 3,
                 '%': 3,
                 '^': 4,
                 '<': 1,
                 '>': 1,
                 '<=': 1,
                 '>=': 1,
                 '!=': 1,
                 '==': 1}

good_chars = "abcdefghijklmnopqrstuvwxyz"+"0123456789"+"()"+" ,."


def get_operator_chars(operators):

"""
    get operator symbols
"""
   operator_chars = "".join(set("".join(list(operators))))
    return operator_chars


def get_num_of_params(func, func_dict):

"""
    get the number arguments
"""
   if (func == "pow") or (func == "log"):
        return 2
    sig = signature(func_dict[func])
    return len(sig.parameters)


def calculator(st, mt, basic_operators, compound_operators, priority_dict, good_chars):

"""
    The funciton, where all conditions are being checked and the expression is being calculated.
    Takes a string, returns the calculation result.
"""
   operators = {**basic_operators, **compound_operators}
    operator_chars = get_operator_chars(operators)

    good_chars = good_chars+operator_chars

    built_in_func_dict = {"abs": abs, "round": round}
    math_func_dict = get_module_func(mt)
    func_dict = {**math_func_dict, **built_in_func_dict}
    const_dict = get_module_const(mt)

    funcs = list(func_dict.keys())
    consts = list(const_dict.keys())

    if not(check_not_empty(st)):
        return "ERROR: Empty string."

    if not(check_spaces(st, operator_chars)):
        return "ERROR: Spaces between numbers or operators."

    st = make_lower(st)
    st = remove_spaces(st)

    if not(check_chars(st, good_chars)):
        return "ERROR: Bad symbols in expression."

    if not(check_dots(st)):
        return "ERROR: dot outside the number."

    if not(check_bracket_balance(st)):
        return "ERROR: brackets are not balanced."

    if not(check_not_empty_brackets(st)):
        return "ERROR: empty brackets."

    st = replace_const(st, const_dict)

    if not(check_functions(st, funcs)):
        return "ERROR: unknown function or missed operator found."

    if not(check_operators(st, basic_operators, compound_operators)):
        return "ERROR: operator written incorrectly."

    if not(check_operator_arg(st, operator_chars)):
        return "ERROR: wrong operator arguments"

    st = split_by_brackets(st, basic_operators, compound_operators)
    st = replace_unary(st)

    rez = calc_rec(st, func_dict, priority_dict, operators)
    if rez == "error":
        return "ERROR: wrong number of arguments passed to the function."
    else:
        return rez


def check_not_empty(st):

"""
    checking if string is empty
"""
   if (len(st)) == 0:
        return False
    else:
        return True


def check_spaces(st, operator_chars):

"""
    checking, if there are any spaces between numbers or operators
"""
   if len(re.findall("[0-9] [0-9]", st)) > 0:
        return False
    operator_chars = ["//" + i for i in operator_chars if i not in "+-"]
    operator_chars = "".join(operator_chars)
    re_oper = "["+operator_chars+"] ["+operator_chars+"]"
    if len(re.findall(re_oper, st)) > 0:
        return False
    return True


def make_lower(st):

"""
    lowering string
"""
   return st.lower()


def check_chars(string, good_chars):

"""
    checking, if there are any bad symbols.
"""
   if len([i for i in string if i not in good_chars]) > 0:
        return False
    else:
        return True


def check_dots(st):

"""
    checking whereas dots are used properly.
"""
   if (len(st) == 1):
        if (st[0] == "."):
            return False
        else:
            return True
    else:
        if ((st[0] == ".") and not(st[1].isdigit())) or ((st[-1] == ".") and not(st[-2].isdigit())):
            return False
    for ind in range(1, len(st)-1):
        if (st[ind] == ".") and not(st[ind-1].isdigit()) and not(st[ind+1].isdigit()):
            return False
    return True


def remove_spaces(st):

"""
    removing spaces.
"""
   return st.replace(" ", "")


def check_bracket_balance(st):

"""
    checking brackets balance.
"""
   if "(" or ")" in st:
        l_it = 0
        r_it = 0
        for i in st:
            if i == "(":

                if l_it < r_it:
                    return False
                l_it += 1

            elif i == ")":
                r_it += 1

        if l_it != r_it:
            return False
    return True


def check_not_empty_brackets(st):

"""
    checking string on empty brackets
"""
   if st.find("()") != -1:
        return False
    else:
        return True


def replace_const(st, const_dict):

"""
    replacing constant names with its numbers
"""
   p = re.compile("[a-z]+")
    edges = [(m.start(), m.end(), m.group())
             for m in p.finditer(st) if m.group() in const_dict]
    edges = sorted(edges)
    consts = [i[2] for i in edges]
    edges = [j for i in edges for j in i[0:2]]
    edges = [0]+edges+[len(st)]
    edges = list(zip(edges[0:-1], edges[1:]))
    edges = [st[i[0]:i[1]] if ind % 2 == 0
             else str(const_dict[consts[(ind-1)//2]]) for ind, i in enumerate(edges)]
    return "".join(edges)


def check_functions(st, functions):

"""
    checking functions.
"""

   # checking if all words in string are functions
   tmp_re_1 = r"([a-z]+[\w]*)"
    all_func = re.findall(tmp_re_1, st)
    if len(set(all_func)-set(functions)) != 0:
        return False

    # check if there are any nums near brackets
    found_arr = re.findall(r"([a-z0-9]+)\(", st)

    if len(set(found_arr)-set(functions)) != 0:
        return False

        # checking if there are any symbols near the brackets.
    found_arr = re.findall(r"[a-z0-9]\(", st)

    if len(found_arr) != len(all_func):
        return False

    return True


def check_operators(st, basic_operators, compound_operators):


"""
Checking, whereas operators are written correctly.
"""

   operator_chars = get_operator_chars(
        {**basic_operators, **compound_operators})
    operator_chars_re = "".join(np.asarray(
        (list(zip("\\"*len(operator_chars), operator_chars)))).reshape((-1,)))
    operators = list(basic_operators)+list(compound_operators)

    tmp_re = "["+operator_chars_re+"]"+"+"
    found_arr = re.findall(tmp_re, st)
    found_arr = [i for i in found_arr if (len(set(i)-{"+", "-"}) > 0)]
    found_arr = [i for i in found_arr if (
        i[:-1] not in operators) and i[-1] in ["+", "-"]]

    if len(set(found_arr)-(set(basic_operators
                               ).union(set(compound_operators)))) > 0:
        return set(found_arr)-(set(basic_operators
                                   ).union(set(compound_operators)))
    else:
        return True


def check_operator_arg(st, operator_chars):


"""
Checking, whereas operators have proper arguments.
"""

   if st[-1] in ["+", "-"]:
        return False

    bad_unary = [i for ind, i in enumerate(st)
                 if (i in ["+", "-"]) and
                 st[ind+1] not in "(0123456789abcdefghijklmnopqrstuvwxyz.+-"]
    if len(bad_unary) > 0:
        return False

    operator_chars = [i for i in operator_chars if i not in ["+", "-"]]

    if (st[0] in operator_chars) or (st[-1] in operator_chars):
        return False

    bad_binary = [i for ind, i in enumerate(st)
                  if (i in operator_chars) and
                  (st[ind+1] == ")") or (st[ind-1] == "(")
                  ]

    if len(bad_unary) > 0:
        return False

    return True


def split_simple_exp(st, basic_operators, compound_operators):

"""
Splitting simple expression without any brackets and commas.
"""

   basic_oper_re = list(zip(["\\"]*len(basic_operators.keys()),
                             basic_operators.keys(),
                             ["|"]*len(basic_operators.keys())))
    basic_oper_re = "".join(np.asarray(basic_oper_re).reshape((-1,)))[:-1]
    basic_oper_re = "("+basic_oper_re+")"

    comp_oper_re = [["\\"+j for j in i]+["|"]
                    for i in compound_operators.keys()]
    comp_oper_re = np.asarray(comp_oper_re).reshape((-1,))
    comp_oper_re = "".join(comp_oper_re)[:-1]
    comp_oper_re = "("+comp_oper_re+")"

    st = re.split(comp_oper_re, st)
    arr = []
    for i in st:

        if i not in compound_operators.keys():
            i = re.split(basic_oper_re, i)
            i = [j for j in i if len(j) > 0]

            arr.extend(i)
        else:
            arr.append(i)
    return arr


def split_by_comma(st):

"""
splitting string with comma as separator only on the top level of expression( without touching anything inside brackets.)
"""

   it = 0
    comma_arr = []

    for ind, i in enumerate(st):

        if i == ",":
            if it == 0:
                comma_arr.append(ind)
        elif i == ")":
            it = it-1
        elif i == "(":
            it = it+1

    if len(comma_arr) == 0:
        return [st]

    return [st[i:j] for i, j in zip(
        ([0]+[i+1 for i in comma_arr]),
        comma_arr+[None])]


def split_by_brackets(st, basic_operators, compound_operators, is_func=False):


"""
function, which splits the expression and returns a nested list.
"""
   operators = {**basic_operators, **compound_operators}
    operator_chars = set("".join(operators.keys()))
    operator_chars = "".join(operator_chars)

    # split simple expression
    if ("(" not in st) and ("," not in st):
        return split_simple_exp(st, basic_operators, compound_operators)

    # else:

    # get bracket index and level
    it = 0
    left_q = []
    right_q = []

    for ind, i in enumerate(st):
        if i == ")":
            right_q.append((it, ind))
            it = it-1
        if i == "(":
            it = it+1
            left_q.append((it, ind))

    left_q = [i[1] for i in left_q if i[0] == 1]
    right_q = [i[1] for i in right_q if i[0] == 1]

    edges = sorted(left_q+right_q)

    split_arr = []
    if st[0:edges[0]] != "":
        split_arr = split_arr + \
            split_simple_exp(
                st[0:edges[0]], basic_operators, compound_operators)

    func_flag = False
    for ind, i in enumerate(edges[:-1]):
        tmp_st = st[i+1:edges[ind+1]]
        if st[i] == "(":
            if (st[i-1].isalpha()) or (st[i-1].isdigit()):
                tmp_st = [split_by_brackets(i, basic_operators, compound_operators)
                          for i in split_by_comma(tmp_st)]
            else:
                tmp_st = split_by_brackets(
                    tmp_st, basic_operators, compound_operators)
            split_arr.append(tmp_st)
        else:
            tmp_st = split_simple_exp(
                tmp_st, basic_operators, compound_operators)
            split_arr = split_arr+tmp_st

    if st[edges[-1]+1:len(st)] != "":
        split_arr = split_arr + \
            split_simple_exp(st[edges[-1]+1:len(st)],
                             basic_operators, compound_operators)

    return split_arr


def replace_atom_unary(arr):


"""
replaces two unary operators with one.
"""
   if arr[0] == arr[1]:
        return "+"
    else:
        return "-"


def replace_unary(exp):


"""
Replaces all sequential unary operators in the nested list.
"""

   if type(exp) == list:
        rez_arr = []

        for ind in range(len(exp))[:-1]:

            if type(exp[ind]) == list:
                rez_arr.append(replace_unary(exp[ind]))
            elif exp[ind] in ["+", "-"] and exp[ind+1] in ["+", "-"]:
                exp[ind+1] = replace_atom_unary((exp[ind], exp[ind+1]))
            else:
                rez_arr.append(exp[ind])
        rez_arr.append(replace_unary(exp[-1]))
    else:

        return exp
    return rez_arr


def key_by_pripority(x, priority_dict):

"""
returns key for sorting non associative operators, power particularly.
"""
   if x[0] == priority_dict["^"]:
        return (x[0], x[1])
    else:
        return (x[0], -x[1])


def calc_rec(exp_arr, func_dict, priority_dict, operators):

"""
recursive calculating expression,taking a nested list.
"""
   if type(exp_arr) == list:

        # numbers to float
        exp_arr = [float(i) if((type(i) == str) and i.replace(
            '.', '', 1).isdigit()) else i for i in exp_arr]

        # calculate brackets
        exp_arr = [calc_rec(i, func_dict, priority_dict, operators) if type(
            i) == list else i for i in exp_arr]

        # exit recursion with error
        if "error" in exp_arr:
            return "error"

        func_ind = [ind for ind, i in enumerate(exp_arr) if (
            type(i) == str) and (i in func_dict.keys())]

        # calculate functions
        while (len(func_ind) > 0):
            i = func_ind[0]

            if(type(exp_arr[i+1]) == list):
                if len(exp_arr[i+1]) > get_num_of_params(exp_arr[i], func_dict):
                    return "error"
                exp_arr[i] = func_dict[exp_arr[i]](*exp_arr[i+1])
            else:
                exp_arr[i] = func_dict[exp_arr[i]](exp_arr[i+1])
            del exp_arr[i+1]
            func_ind = [ind for ind, i in enumerate(exp_arr) if (
                type(i) == str) and (i in func_dict.keys())]

        # calculate unary operators
        op_ind = [(priority_dict[i], ind) for ind, i in enumerate(
            exp_arr) if (type(i) == str) and i in operators.keys()]
        drop_arr = []
        for i in op_ind:
            ind = i[1]
            if exp_arr[ind] in ["+", "-"] and ((ind == 0) or not type(exp_arr[ind-1]) == float):

                drop_arr.append(ind)
                exp_arr[ind+1] = {"-": -1, "+": 1}[exp_arr[ind]]*exp_arr[ind+1]
        exp_arr = [i for ind, i in enumerate(exp_arr) if ind not in drop_arr]

        # calculate operators
        op_ind = [(priority_dict[i], ind) for ind, i in enumerate(
            exp_arr) if (type(i) == str) and i in operators.keys()]
        op_ind = sorted(op_ind, key=lambda x: key_by_pripority(
            x, priority_dict), reverse=True)
        while (len(op_ind) > 0):
            i = op_ind[0][1]
            arg_1 = exp_arr[i-1]
            arg_2 = exp_arr[i+1]
            exp_arr[i] = operators[exp_arr[i]](arg_1, arg_2)
            del exp_arr[i-1]
            del exp_arr[i]

            op_ind = [(priority_dict[i], ind) for ind, i in enumerate(
                exp_arr) if (type(i) == str) and i in operators.keys()]
            op_ind = sorted(op_ind, key=lambda x: key_by_pripority(
                x, priority_dict), reverse=True)

        if len(exp_arr) == 1:

            return exp_arr[0]

    return exp_arr


def main():

"""
the main function.
"""
   parser = argparse.ArgumentParser(
        description='Pure-python command-line calculator.')
    parser.add_argument('EXPRESSION', type=str,
                        help='expression string to evaluate')
    args = parser.parse_args()
    print(calculator(args.EXPRESSION, mt, basic_operators,
                     compound_operators, priority_dict, good_chars))
