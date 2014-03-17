"""
###################################################
#  Our own little alien language parsing utility  #
###################################################

"""


def is_prime(n):
    """Check if n is a prime.

    Args:
        n (int): The number to check.

    Returns:
        bool.

    Doctests:
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


def calculate(operable_group):
    """Calculate the result of an operable group.

    Args:
        operable_group (str): The group to calculate a result of.

    Returns:
        str.

    Doctests:
        >>> calculate('1 LEFT 2')
        '1'

        >>> calculate('1 RIGHT 2')
        '2'

        >>> calculate('32 RIGHT 4')
        '4'

        >>> calculate('1 DOWN 2')
        '1'

        >>> calculate('1 DOWN 3')
        '0'

        >>> calculate('1 UP 2')
        '1'

        >>> calculate('8 UP 3')
        '0'

    """
    operation_blocks = operable_group.split()
    left_operand = operation_blocks[0]
    right_operand = operation_blocks[2]
    if "LEFT" in operable_group:
        return left_operand
    elif "RIGHT" in operable_group:
        return right_operand
    elif "UP" in operable_group:
        if int(right_operand) % int(left_operand) == 0:
            return "1"
        else:
            return "0"

    elif "DOWN" in operable_group:
        sum_blocks = int(left_operand) + int(right_operand)
        if is_prime(sum_blocks):
            return "1"
        else:
            return "0"

    else:
        raise Exception(
            "Operator in '{0}' is invalid".format(operable_group))


def break_in_first_operable_group(text, break_side="right"):
    """Break alien text into two pieces in the first operable group.

    Args:
        text (str): The alien text to break into pieces.

    Kwargs:
        break_side (str): The side in the first operable group where the
            the text should be broken. This is either "right" or "left".

    Returns:
        str.

    Doctests:
        >>> break_in_first_operable_group('3 LEFT 4', 'right')
        ('3 LEFT ', '4')

        >>> break_in_first_operable_group('23 RIGHT 3 LEFT 12', 'right')
        ('23 RIGHT ', '3 LEFT 12')

        >>> break_in_first_operable_group('3 LEFT 4', 'left')
        ('3', ' LEFT 4')

        >>> break_in_first_operable_group('23 RIGHT 3 LEFT 12', 'left')
        ('23', ' RIGHT 3 LEFT 12')

        >>> break_in_first_operable_group('23 RIGHT 3 LEFT 12', 'bla')
        Traceback (most recent call last):
          File "/usr/lib/python2.7/doctest.py", line 1289, in __run
            compileflags, 1) in test.globs
          File "<doctest __main__.break_in_first_operable_group[4]>",
            line 1, in <module>
            break_in_first_operable_group('23 RIGHT 3 LEFT 12', 'bla')
          File "alien_language_parser.py", line 125,
            in break_in_first_operable_group
            raise Exception("'{0}' is not a valid argument".format(break_side))
        Exception: 'bla' is not a valid argument

        >>> break_in_first_operable_group('(23 RIGHT 3 LEFT 12', 'right')
        Traceback (most recent call last):
          File "/usr/lib/python2.7/doctest.py", line 1289, in __run
            compileflags, 1) in test.globs
          File "<doctest __main__.break_in_first_operable_group[5]>",
            line 1, in <module>
            break_in_first_operable_group('(23 RIGHT 3 LEFT 12', 'right')
          File "alien_language_parser.py", line 144,
            in break_in_first_operable_group
            raise Exception("Should start with a digit")
        Exception: Should start with a digit

    """
    if not text[0].isdigit():
        raise Exception("Should start with a digit")
    split = text.split()
    if break_side == "right":
        head = "{0} ".format(" ".join(split[:2]))
        remainder = " ".join(split[2:])
    elif break_side == "left":
        head = " ".join(split[:1])
        remainder = " {0}".format(" ".join(split[1:]))
    else:
        raise Exception("'{0}' is not a valid argument".format(break_side))
    return head, remainder


def break_on_parenthesis(text, direction="l2r"):
    """Break text on first encountered parenthesis.

    Args:
        text (str): The alien text to break into pieces.

    Kwargs:
        direction (str): The direction in which the text is processed to break
            it into pieces.
            If the direction is "l2r" then the text will be broken on the
            first encountered right parenthesis; `)`.
            If the direction is "r2l" then the text will be broken on the
            first encountered left parenthesis; `(`.

    Returns:
        str.

    Doctests:
        >>> break_on_parenthesis("(2 RIGHT 3)", "l2r")
        ('(2 RIGHT 3', '')

        >>> break_on_parenthesis("(1 LEFT (2 RIGHT 3))", "l2r")
        ('(1 LEFT (2 RIGHT 3', ')')

        # Doc tests won't allow string line break via parenthesis alone
        >>> break_on_parenthesis(\
            "(2 UP ((1 LEFT (2 RIGHT 3)) UP 3)) DOWN 11", "l2r")
        ('(2 UP ((1 LEFT (2 RIGHT 3', ') UP 3)) DOWN 11')

        >>> break_on_parenthesis('(2 RIGHT 3', "r2l")
        ('', '2 RIGHT 3')

        >>> break_on_parenthesis("(1 LEFT (2 RIGHT 3", "r2l")
        ('(1 LEFT ', '2 RIGHT 3')

        >>> break_on_parenthesis("(2 UP ((1 LEFT (2 RIGHT 3", "r2l")
        ('(2 UP ((1 LEFT ', '2 RIGHT 3')

        >>> break_on_parenthesis('(2 RIGHT 3)', "bla")
        Traceback (most recent call last):
          File "/usr/lib/python2.7/doctest.py", line 1289, in __run
            compileflags, 1) in test.globs
          File "<doctest __main__.break_on_parenthesis[6]>", line 1,
            in <module>
            break_on_parenthesis('(2 RIGHT 3)', "bla")
          File "alien_language_parser.py", line 166, in break_on_parenthesis
            raise Exception("'{0}' is not a valid argument".format(direction))
        Exception: 'bla' is not a valid argument

    """
    if direction == "l2r":
        split = text.split(")", 1)
    elif direction == "r2l":
        split = text.rsplit("(", 1)
    else:
        raise Exception("'{0}' is not a valid argument".format(direction))

    left_split = split[0]
    right_split = split[1]
    return left_split, right_split


# Slightly less namespace-polluting than using global
class ParseData(object):
    """Holds text between recursive calls of alien_eval."""
    def __init__(self):
        #: Is prepended to text of a recursive call of alien_eval stemming
        #: from a text beginning with a left parenthesis.
        #:
        #: Example :
        #:   alien_eval("(1 LEFT (2 RIGHT 1) RIGHT 4)")
        #:     then
        #:   self.R2L_LAST is "(1 LEFT "
        self.R2L_LAST = ""

        #: Similar to the above but it is appended instead of prepended.
        #:
        #: For example above:
        #:   self.L2R_LAST is " RIGHT 4"
        self.L2R_LAST = ""


parse_data = ParseData()


def alien_eval(text):
    """Evaluate a piece of text in our alien language to a number.

    Args:
        text (str): A piece of text with alien language syntax.

    Returns:
        int.

    Doctests:
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
    if text[0].isdigit():
        # Case: "12"
        if len(text.split()) == 1:
            return int(text)
        # Case: "2 RIGHT 12"
        elif len(text.split()) == 3:
            tmp_result = calculate(text)
            current_string = "{0}{1}{2}".format(parse_data.R2L_LAST,
                                                tmp_result,
                                                parse_data.L2R_LAST)
            parse_data.R2L_LAST = ""
            parse_data.L2R_LAST = ""
            return alien_eval(current_string)
        else:
            rhead, rremainder = break_in_first_operable_group(text, "right")

            # Case: "2 RIGHT 12 LEFT 3"
            if not rremainder.startswith('('):
                lhead, lremainder = break_in_first_operable_group(rremainder,
                                                                  "left")
                operable_stri = "{0}{1}".format(rhead, lhead)
                tmp_result = calculate(operable_stri)
                current_string = "{0}{1}".format(tmp_result, lremainder)
                return alien_eval(current_string)

            # Case: "2 RIGHT (3 RIGHT 4)"
            else:
                tmp_result = "{0}{1}".format(rhead, alien_eval(rremainder))
                return int(calculate(tmp_result))

    # Case: "(2 RIGHT ((1 LEFT (5 RIGHT 4)) UP 3))"
    elif text.startswith("("):
        l2r_first, parse_data.L2R_LAST = break_on_parenthesis(text, "l2r")
        parse_data.R2L_LAST, r2l_first = break_on_parenthesis(l2r_first, "r2l")
        return alien_eval(r2l_first)

    else:
        raise Exception("Else Die")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
