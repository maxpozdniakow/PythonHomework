import math as mt
import numpy as np
import argparse
import re
from inspect import signature


def get_module_func(module):
    object_arr = [i for i in dir(module) if not(i.startswith("__"))]
    return {i: getattr(mt, i) for i in object_arr if type(getattr(mt, i)) != float}


def get_module_const(module):
    object_arr = [i for i in dir(module) if not(i.startswith("__"))]
    return {i: getattr(mt, i) for i in object_arr if type(getattr(mt, i)) == float}

# ЛОГАРИФМЫ! done

# запятые

# функции с цифрами на конце

# App plan:

# проверка и предобработка:
# make_lower
# remove_spaces
# check_not_empty
# check_chars
# check_dots
# 	есть только возможные символы
# check_quote_balance
# 	есть только возможные символы, соблюдён баланс скобок
# check_not_empty_quotes
# 	есть только возможные символы, соблюдён баланс скобок, в скобках что-то написано
# replace_const
# check_functions
# check_function_quotes
# 	есть только возможные символы, соблюдён баланс скобок, в скобках что-то написано, все буквенные выражения- функции, все функции написаны правильно
# check_operators
# check_operator_arg
# 	есть только возможные символы, соблюдён баланс скобок, в скобках что-то написано, все буквенные выражения- функции, все функции написаны правильно, все операторы написаны правильно

# вычесления:
# split_by_quotes


def get_operator_chars(operators):
    operator_chars = "".join(set("".join(list(operators))))
    return operator_chars

# ABS!!!!


def get_num_of_params(func, func_dict):
    if (func == "pow") or (func == "log"):
        return 2
    sig = signature(func_dict[func])
    return len(sig.parameters)


def calculator(st, mt=mt, basic_operators=False, compound_operators=False, priority_dict=False, good_chars=False):

#     ***************declarations***************

    compound_operators = {
           "//": lambda x, y: x//y,
           "<=": lambda x, y: int(x <= y),
           ">=": lambda x, y: int(x >= y),
           "!=": lambda x, y: int(x != y),
           "==": lambda x, y: int(x == y)}

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

#     ***************/declarations***************

    operators = {**basic_operators, **compound_operators}
    operator_chars = get_operator_chars(operators)

#     quotes_chars="()"
#     alphabet="abcdefghijklmnopqrstuvwxyz"
#     digits="0123456789"
#     good_chars=digits+alphabet+operator_chars+quotes_chars+" ,"

    good_chars = good_chars+operator_chars

    built_in_func_dict = {"abs": abs, "round": round}
    math_func_dict = get_module_func(mt)
    func_dict = {**math_func_dict, **built_in_func_dict}

    const_dict = get_module_const(mt)

    funcs = list(func_dict.keys())
    consts = list(const_dict.keys())

    # preprocessing
    st = make_lower(st)
    st = remove_spaces(st)

    if not(check_not_empty(st)):
        return "ERROR: BLA BLA BLA"

    if not(
check_chars(st, good_chars)):
        return "ERROR: BLA BLA BLA"

    if not(
check_dots(st)):
        return "ERROR: BLA BLA BLA"

    if not(check_spaces(st, operator_chars):
           return "ERROR: BLA BLA BLA"

    if not(
        check_quote_balance(st) and
        check_not_empty_quotes(st)
    ):
        return "ERROR: BLA BLA BLA"




    st=replace_const(st, const_dict)
    if not(st):
        return "ERROR: BLA BLA BLA"





    if not(
        check_functions(st, funcs)
#         and check_function_quotes(st)
    ):
        return "ERROR: BLA BLA BLA"



#     if not(
#     check_operators(st,basic_operators,compound_operators) and
#     check_operator_arg(st,operator_chars)):
#         return "ERROR: BLA BLA BLA"

    st=split_by_quotes(st, basic_operators, compound_operators)
    st=replace_unary(st)

    rez=calc_rec(st, func_dict, priority_dict, operators)
    if rez == "error":
        return "ERROR: BLA BLA BLA"
    else:
        return rez

def check_not_empty(st):
    if (len(st)) == 0:
        return False
    else:
        return True

def check_spaces(st, operator_chars):
    if len(re.findall("[0-9] [0-9]", st)) > 0:
        return False
    operator_chars=["//" + i for i in operator_chars if i not in "+-"]
    operator_chars="".join(operator_chars)
    re_oper="["+operator_chars+"] ["+operator_chars+"]"

    if len(re.findall(re_oper, st)) > 0:
        return False
    return True

def make_lower(st):
    return st.lower()

def check_chars(string, good_chars):
    if len([i for i in string if i not in good_chars]) > 0:
        return False
    else:
        return True

# def check_dots(st):
#         t=re.findall("[^0-9]\.[^0-9]|^\.[^0-9]|[^0-9]\.$",st)
#         if len(t)>0:
#             return t
#         else:
#             return False

def check_dots(st):
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
    return st.replace(" ", "")

def check_quote_balance(st):
    if "(" or ")" in st:
        l_it=0
        r_it=0

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

def check_not_empty_quotes(st):
    if st.find("()") != -1:
        return False
    else:
        return True

def replace_const(st, const_dict):
    p=re.compile("[a-z]+")
    edges=[(m.start(), m.end(), m.group())
            for m in p.finditer(st) if m.group() in const_dict]
    edges=sorted(edges)
    consts=[i[2] for i in edges]
    edges=[j for i in edges for j in i[0:2]]
    edges=[0]+edges+[len(st)]
    edges=list(zip(edges[0:-1], edges[1:]))
    edges=[st[i[0]:i[1]] if ind % 2 == 0
           else str(const_dict[consts[(ind-1)//2]]) for ind, i in enumerate(edges)]
    return "".join(edges)

# def replace_const(st,const_dict):
#     re_exp = r'[a-zA-Z]+'
#     word_arr=set(re.findall(re_exp,st))

#     word_arr=list(word_arr.intersection(set(const_dict)))
#     word_arr=sorted(word_arr,key=lambda x: len(x),reverse=True)

#     if ("inf" in word_arr) or ("nan" in word_arr):
#         return False
#     word_arr=sorted(word_arr,reverse=True)
#     for i in word_arr:
#         tmp_val=str(const_dict[i])
#         st=st.replace(i,tmp_val)
#     return st

# def replace_const(st,const_dict):
#     re_exp = r'[a-zA-Z]+'
#     word_arr=set(re.findall(re_exp,st))

#     word_arr=list(word_arr.intersection(set(const_dict)))
#     word_arr=sorted(word_arr,key=lambda x: len(x),reverse=True)

#     if ("inf" in word_arr) or ("nan" in word_arr):
#         return False

#     for i in word_arr:
#         tmp_val=const_dict[i]
#         pat_re="([\W]|^)"+i+"([\W]|$)"
#         repl_re=r"\g<1>"+str(tmp_val)+r"\g<2>"
#         st=re.sub(pat_re,repl_re,st)
#     return st

# def replace_const(st, const_dict):

#     #checking constants, which cannot be proccessed with calculator
#     for i in ["inf","nan"]:
#         pat_re="([\W]|^)"+i+"([\W]|$)"
#         if len(re.findall(pat_re,st))>0:
#             return False

#     #replacing constants:
#     for i in const_dict.items():
#         pat_re="([\W]|^)"+i[0]+"([\W]|$)"
#         precision=3
#         tmp_val=round(i[1],precision)
#         repl_re=r"\g<1>"+str(tmp_val)+r"\g<2>"
#         st=re.sub(pat_re,repl_re,st)

#     return st

def check_functions(st, functions):
    # checking if all words in string are functions
    tmp_re_1=r"([a-z]+[\w]*)"
    all_func=re.findall(tmp_re_1, st)
    if len(set(all_func)-set(functions)) != 0:
        return False



#     #check if there are any nums near brackets

#     if len(set(re.findall("([\w]+\()",st))-set([i+"(" for i in functions]))!=0:
#         return False




#     if len(re.findall("([a-z]+[^\(]+)",st))!=0:
#         return False



    return True

def check_function_quotes(st):
    for ind, i in enumerate(st[:-1]):
        if i.isalpha():
            if (not st[ind+1].isalpha()
               ) and st[ind+1] != "(":
                return False

    if st[-1].isalpha():
        return False

    return True

def check_operators(st, basic_operators, compound_operators):

    operator_chars=get_operator_chars(
        {**basic_operators, **compound_operators})
    operator_chars_re="".join(np.asarray(
        (list(zip("\\"*len(operator_chars), operator_chars)))).reshape((-1,)))

    tmp_re="["+operator_chars_re+"]"+"+"
    found_arr=re.findall(tmp_re, st)
    if len(set(found_arr)-(set(basic_operators
                           ).union(set(compound_operators)))) > 0:
        return False
    else:
        return True

def check_operator_arg(st, operator_chars):
    if st[0] in operator_chars or st[-1] in operator_chars:
        return False

    if len(st) <= 2:
        return True

    for i in range(1, len(st)-1):
        if (st[i] in operator_chars) and ((st[i+1] == ")") or (st[i-1] == "(")):


            return False
    return True

# def split_by_quotes(st,operator_chars):
#     re_operators="".join(["\\"+i+"|" for i in operator_chars])
#     re_tmp_1="([\d]+[\.]?[\d]*|[a-zA-Z]+|"+re_operators[:-1]+")"

#     if "(" not in st:
# #         re_tmp_1="([\d]+[\.]?[\d]*|\*|\+|-|[a-zA-Z]+)"

#         tmp_st=re.findall(re_tmp_1,st)
#         return tmp_st
#     else:
#         it=0
#         left_q=[]
#         right_q=[]

#         for ind,i in enumerate(st):
#             if i==")":
#                 right_q.append((it,ind))
#                 it=it-1
#             if i=="(":
#                 it=it+1
#                 left_q.append((it,ind))

#         left_q=[i[1] for i in left_q if i[0]==1]
#         right_q=[i[1] for i in right_q if i[0]==1]

#         edges=sorted(left_q+right_q)


# #         re_tmp_1="([\d]+[\.]?[\d]*|[a-zA-Z]+|"+re_operators+")"

#         split_arr=[]
#         if st[0:edges[0]]!="":
#             split_arr=split_arr+re.findall(re_tmp_1,st[0:edges[0]])

#         for ind,i in enumerate(edges[:-1]):
#             tmp_st=st[i+1:edges[ind+1]]
#             if st[i]=="(":
#                 tmp_st=split_by_quotes(tmp_st,operator_chars)
#                 split_arr.append(tmp_st)
#             else:
#                 tmp_st=re.findall(re_tmp_1,tmp_st)
#                 split_arr=split_arr+tmp_st

#         if st[edges[-1]+1:len(st)]!="":
#             split_arr=split_arr+re.findall(re_tmp_1,st[edges[-1]+1:len(st)])

#         return split_arr


def split_simple_exp(st, basic_operators, compound_operators):

    basic_oper_re=list(zip(["\\"]*len(basic_operators.keys()),
                          basic_operators.keys(),
                         ["|"]*len(basic_operators.keys())))
    basic_oper_re="".join(np.asarray(basic_oper_re).reshape((-1,)))[:-1]
    basic_oper_re="("+basic_oper_re+")"

    comp_oper_re=[["\\"+j for j in i]+["|"] for i in compound_operators.keys()]
    comp_oper_re=np.asarray(comp_oper_re).reshape((-1,))
    comp_oper_re="".join(comp_oper_re)[:-1]
    comp_oper_re="("+comp_oper_re+")"

    st=re.split(comp_oper_re, st)
    arr=[]
    for i in st:

        if i not in compound_operators.keys():
            i=re.split(basic_oper_re, i)
#             i=re.split("([^\w\.])",i)
            i=[j for j in i if len(j) > 0]

            arr.extend(i)
        else:
            arr.append(i)
    return arr

def split_by_comma(st):

    it=0
    comma_arr=[]

    for ind, i in enumerate(st):

        if i == ",":
            if it == 0:
                comma_arr.append(ind)
        elif i == ")":
            it=it-1
        elif i == "(":
            it=it+1

    if len(comma_arr) == 0:
        return [st]

    return [st[i:j] for i, j in zip(
        ([0]+[i+1 for i in comma_arr]),
        comma_arr+[None])]

def split_by_quotes(st, basic_operators, compound_operators, is_func=False):


    operators={**basic_operators, **compound_operators}
    operator_chars=set("".join(operators.keys()))
    operator_chars="".join(operator_chars)

    # split simple expression
    if ("(" not in st) and ("," not in st):
        return split_simple_exp(st, basic_operators, compound_operators)

    # else:

    # get bracket index and level
    it=0
    left_q=[]
    right_q=[]

    for ind, i in enumerate(st):
        if i == ")":
            right_q.append((it, ind))
            it=it-1
        if i == "(":
            it=it+1
            left_q.append((it, ind))


    left_q=[i[1] for i in left_q if i[0] == 1]
    right_q=[i[1] for i in right_q if i[0] == 1]

    edges=sorted(left_q+right_q)

    split_arr=[]
    if st[0:edges[0]] != "":
        split_arr=split_arr + \
            split_simple_exp(
                st[0:edges[0]], basic_operators, compound_operators)

    func_flag=False
    for ind, i in enumerate(edges[:-1]):
        tmp_st=st[i+1:edges[ind+1]]
        if st[i] == "(":
            if (st[i-1].isalpha()) or (st[i-1].isdigit()):
                tmp_st=[split_by_quotes(i, basic_operators, compound_operators)
                        for i in split_by_comma(tmp_st)]
            else:
                tmp_st=split_by_quotes(
                    tmp_st, basic_operators, compound_operators)
            split_arr.append(tmp_st)
        else:
            tmp_st=split_simple_exp(
                tmp_st, basic_operators, compound_operators)
            split_arr=split_arr+tmp_st

    if st[edges[-1]+1:len(st)] != "":
        split_arr=split_arr + \
            split_simple_exp(st[edges[-1]+1:len(st)],
                             basic_operators, compound_operators)

    return split_arr

def replace_atom_unary(arr):
    if arr[0] == arr[1]:
        return "+"
    else:
        return "-"

def replace_unary(exp):
    if type(exp) == list:
        rez_arr=[]
        for ind in range(len(exp))[:-1]:
            if type(exp[ind]) == list:
                rez_arr.append(replace_unary(exp))
            else:
                if exp[ind] in ["+", "-"] and exp[ind+1] in ["+", "-"]:

                    exp[ind+1]=replace_atom_unary((exp[ind], exp[ind+1]))
#                     rez_arr.append(exp[ind+1])
                else:
                    rez_arr.append(exp[ind])
        rez_arr.append(exp[-1])
    else:
        return False
    return rez_arr

def replace_unary(exp):
    if type(exp) == list:
        rez_arr=[]

        for ind in range(len(exp))[:-1]:

            if type(exp[ind]) == list:
                rez_arr.append(replace_unary(exp[ind]))
            elif exp[ind] in ["+", "-"] and exp[ind+1] in ["+", "-"]:
                exp[ind+1]=replace_atom_unary((exp[ind], exp[ind+1]))
#                     rez_arr.append(exp[ind+1])
            else:
                rez_arr.append(exp[ind])
        rez_arr.append(replace_unary(exp[-1]))
    else:

        return exp
    return rez_arr

def replace_atom_unary(arr):
    if arr[0] == arr[1]:
        return "+"
    else:
        return "-"

def key_by_pripority(x, priority_dict):
    if x[0] == priority_dict["^"]:
        return (x[0], x[1])
    else:
        return (x[0], -x[1])

def calc_rec(exp_arr, func_dict, priority_dict, operators):


    if type(exp_arr) == list:

        # numbers to float
        exp_arr=[float(i) if((type(i) == str) and i.replace(
            '.', '', 1).isdigit()) else i for i in exp_arr]

        # calculate brackets
        exp_arr=[calc_rec(i, func_dict, priority_dict, operators)
                          if type(i) == list else i for i in exp_arr]

        # exit recursion with error
        if "error" in exp_arr:
            return "error"

        func_ind=[ind for ind, i in enumerate(exp_arr) if (
            type(i) == str) and (i in func_dict.keys())]

        # calculate functions
        while (len(func_ind) > 0):
            i=func_ind[0]

            if(type(exp_arr[i+1]) == list):
                if len(exp_arr[i+1]) > get_num_of_params(exp_arr[i], func_dict):
                    return "error"
                exp_arr[i]=func_dict[exp_arr[i]](*exp_arr[i+1])
            else:
                exp_arr[i]=func_dict[exp_arr[i]](exp_arr[i+1])
            del exp_arr[i+1]
            func_ind=[ind for ind, i in enumerate(exp_arr) if (
                type(i) == str) and (i in func_dict.keys())]

        # calculate unary operators
        op_ind=[(priority_dict[i], ind) for ind, i in enumerate(
            exp_arr) if (type(i) == str) and i in operators.keys()]
        drop_arr=[]
        for i in op_ind:
            ind=i[1]
            if exp_arr[ind] in ["+", "-"] and ((ind == 0) or not type(exp_arr[ind-1]) == float):

                drop_arr.append(ind)
                exp_arr[ind+1]={"-": -1, "+": 1}[exp_arr[ind]]*exp_arr[ind+1]
        exp_arr=[i for ind, i in enumerate(exp_arr) if ind not in drop_arr]


        # calculate operators
        op_ind=[(priority_dict[i], ind) for ind, i in enumerate(
            exp_arr) if (type(i) == str) and i in operators.keys()]
        op_ind=sorted(op_ind, key=lambda x: key_by_pripority(
            x, priority_dict), reverse=True)
        while (len(op_ind) > 0):
            i=op_ind[0][1]
            arg_1=exp_arr[i-1]
            arg_2=exp_arr[i+1]
            exp_arr[i]=operators[exp_arr[i]](arg_1, arg_2)
            del exp_arr[i-1]
            del exp_arr[i]

            op_ind=[(priority_dict[i], ind) for ind, i in enumerate(
                exp_arr) if (type(i) == str) and i in operators.keys()]
            op_ind=sorted(op_ind, key=lambda x: key_by_pripority(
                x, priority_dict), reverse=True)

        if len(exp_arr) == 1:

            return exp_arr[0]

    return exp_arr

def main():
    parser = argparse.ArgumentParser(
        description='Pure-python command-line calculator.')
    parser.add_argument('EXPRESSION', type=str,
                        help='expression string to evaluate')
    args = parser.parse_args()
    print(calculator(args.EXPRESSION, mt))
