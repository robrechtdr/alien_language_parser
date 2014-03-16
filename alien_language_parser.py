"""
###################################################
#  Our own little alien language parsing utility  #
###################################################

Applicant: Robrecht De Rouck
"""


def is_prime(n):
    """
    >>> is_prime(0)
    False

    >>> is_prime(1)
    False

    >>> is_prime(2)
    True

    >>> is_prime(30)
    False

    >>> is_prime(89)
    True
    """
    l = range(2, n)
    for m in range(len(l)):
        if n % l[m] == 0:
            return False
    if n < 2:
        return False
    else:
        return True


def operate(operable_string):
    """
    >>> operate('1 LEFT 2')
    '1'

    >>> operate('1 RIGHT 2')
    '2'

    >>> operate('32 RIGHT 4')
    '4'

    >>> operate('1 DOWN 2')
    '1'

    >>> operate('1 DOWN 3')
    '0'

    >>> operate('1 UP 2')
    '1'

    >>> operate('8 UP 3')
    '0'


    """
    operation_blocks = operable_string.split()
    left_operand = operation_blocks[0]
    right_operand = operation_blocks[2]
    if "LEFT" in operable_string:
        return left_operand
    elif "RIGHT" in operable_string:
        return right_operand
    elif "UP" in operable_string:
        if int(right_operand) % int(left_operand) == 0:
            return "1"
        else:
            return "0"

    elif "DOWN" in operable_string:
        sum_blocks = int(left_operand) + int(right_operand)
        if is_prime(sum_blocks):
            return "1"
        else:
            return "0"

    else:
        raise Exception(
            "Operator in '{0}' is invalid".format(operable_string))


def break_first_operable_group_right_sided(stri):
    """
    >>> break_first_operable_group_right_sided('3 LEFT 4')
    ('3 LEFT ', '4')

    >>> break_first_operable_group_right_sided('23 RIGHT 3 LEFT 12')
    ('23 RIGHT ', '3 LEFT 12')

    >>> break_first_operable_group_right_sided('(23 RIGHT 3 LEFT 12')
    Traceback (most recent call last):
      File "/usr/lib/python2.7/doctest.py", line 1289, in __run
        compileflags, 1) in test.globs
      File "<doctest __main__.break_first_operable_group_right_sided[2]>",
        line 1, in <module>
        break_first_operable_group_right_sided("(23 RIGHT 3 LEFT 12")
      File "policy_brain.py", line 65, in break_first_operable_group_right_sided
        raise Exception("Should start with a digit")
    Exception: Should start with a digit

    """
    if not stri[0].isdigit():
        raise Exception("Should start with a digit")
    head = "{0} ".format(" ".join(stri.split()[:2]))
    remainder = " ".join(stri.split()[2:])
    return head, remainder


def break_first_operable_group_left_sided(stri):
    """
    >>> break_first_operable_group_left_sided('3 LEFT 4')
    ('3', ' LEFT 4')

    >>> break_first_operable_group_left_sided('23 RIGHT 3 LEFT 12')
    ('23', ' RIGHT 3 LEFT 12')

    >>> break_first_operable_group_left_sided('(23 RIGHT 3 LEFT 12')
    Traceback (most recent call last):
      File "/usr/lib/python2.7/doctest.py", line 1289, in __run
        compileflags, 1) in test.globs
      File "<doctest __main__.break_first_operable_group_right_sided[2]>",
        line 1, in <module>
        break_first_operable_group_left_sided("(23 RIGHT 3 LEFT 12")
      File "policy_brain.py", line 65, in break_first_operable_group_right_sided
        raise Exception("Should start with a digit")
    Exception: Should start with a digit

    """
    if not stri[0].isdigit():
        raise Exception("Should start with a digit")
    head = " ".join(stri.split()[:1])
    remainder = " {0}".format(" ".join(stri.split()[1:]))
    return head, remainder


def left_to_right_parenth_break(stri):
    """
    >>> left_to_right_parenth_break("(2 RIGHT 3)")
    ('(2 RIGHT 3', '')

    >>> left_to_right_parenth_break("(1 LEFT (2 RIGHT 3))")
    ('(1 LEFT (2 RIGHT 3', ')')

    # Doc tests won't allow string line break via parenthesis alone
    >>> left_to_right_parenth_break(\
        "(2 UP ((1 LEFT (2 RIGHT 3)) UP 3)) DOWN 11")
    ('(2 UP ((1 LEFT (2 RIGHT 3', ') UP 3)) DOWN 11')

    """
    split = stri.split(")", 1)
    left_split = split[0]
    right_split = split[1]
    return left_split, right_split


def right_to_left_parenth_break(stri):
    """
    >>> right_to_left_parenth_break('(2 RIGHT 3')
    ('', '2 RIGHT 3')

    >>> right_to_left_parenth_break("(1 LEFT (2 RIGHT 3")
    ('(1 LEFT ', '2 RIGHT 3')

    >>> right_to_left_parenth_break("(2 UP ((1 LEFT (2 RIGHT 3")
    ('(2 UP ((1 LEFT ', '2 RIGHT 3')

    """
    split = stri.rsplit("(", 1)
    left_split = split[0]
    right_split = split[1]
    return left_split, right_split


# Slightly less namespace-polluting than using global
class ParseData(object):
    def __init__(self):
        self.R2L_LAST = ""
        self.L2R_LAST = ""

parse_data = ParseData()


def alien_eval(alien_string):
    """
    >>> alien_eval("(2 DOWN ((1 LEFT (2 RIGHT 3)) UP 3)) DOWN 11")
    0

    >>> alien_eval("(1 LEFT 2) RIGHT 1")
    1

    # Bonus : }
    >>> alien_eval("8 LEFT 3 LEFT 4")
    8

    >>> alien_eval("((8 UP 3 ))")
    0

    # This case follows another parsing path
    # not tested with the given examples!
    >>> alien_eval("18 RIGHT (3 LEFT 4)")
    3

    """
    if alien_string[0].isdigit():
        if len(alien_string.split()) == 1:
            return int(alien_string)
        elif len(alien_string.split()) == 3:
            tmp_result = operate(alien_string)
            current_string = "{0}{1}{2}".format(parse_data.R2L_LAST,
                                                tmp_result,
                                                parse_data.L2R_LAST)
            parse_data.R2L_LAST = ""
            parse_data.L2R_LAST = ""
            return alien_eval(current_string)
        else:
            rhead, rremainder = break_first_operable_group_right_sided(alien_string)
            if not rremainder.startswith('('):
                lhead, lremainder = break_first_operable_group_left_sided(rremainder)
                operable_stri = "{0}{1}".format(rhead, lhead)
                tmp_result = operate(operable_stri)
                current_string = "{0}{1}".format(tmp_result, lremainder)
                return alien_eval(current_string)

            else:
                tmp_result = "{0}{1}".format(rhead, alien_eval(rremainder))
                return int(operate(tmp_result))

    elif alien_string.startswith("("):
        l2r_first, parse_data.L2R_LAST = left_to_right_parenth_break(alien_string)
        parse_data.R2L_LAST, r2l_first = right_to_left_parenth_break(l2r_first)
        return alien_eval(r2l_first)

    else:
        raise Exception("Else Die")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
