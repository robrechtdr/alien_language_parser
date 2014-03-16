"""
###################################################
#  Our own little alien language parsing utility  #
###################################################

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


def break_first_operable_group(stri, break_side="right"):
    """
    >>> break_first_operable_group('3 LEFT 4', 'right')
    ('3 LEFT ', '4')

    >>> break_first_operable_group('23 RIGHT 3 LEFT 12', 'right')
    ('23 RIGHT ', '3 LEFT 12')

    >>> break_first_operable_group('3 LEFT 4', 'left')
    ('3', ' LEFT 4')

    >>> break_first_operable_group('23 RIGHT 3 LEFT 12', 'left')
    ('23', ' RIGHT 3 LEFT 12')

    >>> break_first_operable_group('23 RIGHT 3 LEFT 12', 'bla')
    Traceback (most recent call last):
      File "/usr/lib/python2.7/doctest.py", line 1289, in __run
        compileflags, 1) in test.globs
      File "<doctest __main__.break_first_operable_group[4]>",
      line 1, in <module>
        break_first_operable_group('23 RIGHT 3 LEFT 12', 'bla')
      File "alien_language_parser.py", line 125, in break_first_operable_group
        raise Exception("'{0}' is not a valid argument".format(break_side))
    Exception: 'bla' is not a valid argument

    >>> break_first_operable_group('(23 RIGHT 3 LEFT 12', 'right')
    Traceback (most recent call last):
      File "/usr/lib/python2.7/doctest.py", line 1289, in __run
        compileflags, 1) in test.globs
      File "<doctest __main__.break_first_operable_group[2]>",
        line 1, in <module>
        break_first_operable_group("(23 RIGHT 3 LEFT 12", 'right')
      File "policy_brain.py", line 65, in break_first_operable_group
        raise Exception("Should start with a digit")
    Exception: Should start with a digit
    """
    if not stri[0].isdigit():
        raise Exception("Should start with a digit")
    split = stri.split()
    if break_side == "right":
        head = "{0} ".format(" ".join(split[:2]))
        remainder = " ".join(split[2:])
    elif break_side == "left":
        head = " ".join(split[:1])
        remainder = " {0}".format(" ".join(split[1:]))
    else:
        raise Exception("'{0}' is not a valid argument".format(break_side))
    return head, remainder


def break_parenthesis(stri, direction="l2r"):
    """
    >>> break_parenthesis("(2 RIGHT 3)", "l2r")
    ('(2 RIGHT 3', '')

    >>> break_parenthesis("(1 LEFT (2 RIGHT 3))", "l2r")
    ('(1 LEFT (2 RIGHT 3', ')')

    # Doc tests won't allow string line break via parenthesis alone
    >>> break_parenthesis(\
        "(2 UP ((1 LEFT (2 RIGHT 3)) UP 3)) DOWN 11", "l2r")
    ('(2 UP ((1 LEFT (2 RIGHT 3', ') UP 3)) DOWN 11')

    >>> break_parenthesis('(2 RIGHT 3', "r2l")
    ('', '2 RIGHT 3')

    >>> break_parenthesis("(1 LEFT (2 RIGHT 3", "r2l")
    ('(1 LEFT ', '2 RIGHT 3')

    >>> break_parenthesis("(2 UP ((1 LEFT (2 RIGHT 3", "r2l")
    ('(2 UP ((1 LEFT ', '2 RIGHT 3')

    >>> break_parenthesis('(2 RIGHT 3)', "bla")
    Traceback (most recent call last):
      File "/usr/lib/python2.7/doctest.py", line 1289, in __run
        compileflags, 1) in test.globs
      File "<doctest __main__.break_parenthesis[6]>", line 1, in <module>
        break_parenthesis('(2 RIGHT 3)', "bla")
      File "alien_language_parser.py", line 166, in break_parenthesis
        raise Exception("'{0}' is not a valid argument".format(direction))
    Exception: 'bla' is not a valid argument

    """
    if direction == "l2r":
        split = stri.split(")", 1)
    elif direction == "r2l":
        split = stri.rsplit("(", 1)
    else:
        raise Exception("'{0}' is not a valid argument".format(direction))

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
    # which was not tested with the given examples!
    >>> alien_eval("18 RIGHT (3 LEFT 4)")
    3

    """
    if alien_string[0].isdigit():
        # Case: "12"
        if len(alien_string.split()) == 1:
            return int(alien_string)
        # Case: "2 RIGHT 12"
        elif len(alien_string.split()) == 3:
            tmp_result = operate(alien_string)
            current_string = "{0}{1}{2}".format(parse_data.R2L_LAST,
                                                tmp_result,
                                                parse_data.L2R_LAST)
            parse_data.R2L_LAST = ""
            parse_data.L2R_LAST = ""
            return alien_eval(current_string)
        else:
            rhead, rremainder = break_first_operable_group(alien_string,
                                                           "right")
            # Case: "2 RIGHT 12 LEFT 3"
            if not rremainder.startswith('('):
                lhead, lremainder = break_first_operable_group(rremainder,
                                                               "left")
                operable_stri = "{0}{1}".format(rhead, lhead)
                tmp_result = operate(operable_stri)
                current_string = "{0}{1}".format(tmp_result, lremainder)
                return alien_eval(current_string)

            # Case: "2 RIGHT (3 RIGHT 4)"
            else:
                tmp_result = "{0}{1}".format(rhead, alien_eval(rremainder))
                return int(operate(tmp_result))

    # Case: "(2 RIGHT ((1 LEFT (5 RIGHT 4)) UP 3))"
    elif alien_string.startswith("("):
        l2r_first, parse_data.L2R_LAST = break_parenthesis(alien_string, "l2r")
        parse_data.R2L_LAST, r2l_first = break_parenthesis(l2r_first, "r2l")
        return alien_eval(r2l_first)

    else:
        raise Exception("Else Die")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
