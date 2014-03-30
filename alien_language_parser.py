###################################################
#  Our own little alien language parsing utility  #
###################################################


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
    for i in range(len(l)):
        if n % l[i] == 0:
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

        >>> calculate(1)
        Traceback (most recent call last):
            raise TypeError("'{0}' must be a string".format(operable_group))
        TypeError: '1' must be a string

        >>> calculate('1 LEFT 2 RIGHT 4')
        Traceback (most recent call last):
            raise ValueError(
                "'{0}' is not a valid operable group"\.format(operable_group))
        ValueError: '1 LEFT 2 RIGHT 4' is not a valid operable group

        >>> calculate('(1 LEFT 2')
        Traceback (most recent call last):
            raise not_a_number
        ValueError: invalid literal for int() with base 10: '(1'

        >>> calculate('1 BLA 2')
        Traceback (most recent call last):
            raise ValueError("'{0}' is not a valid operator".format(operator))
        ValueError: 'BLA' is not a valid operator

    """
    # Getting a TypeError is more clear than getting an AtttributeError
    # which would occur on the first split method call if operable_group
    # wasn't a string.
    if not isinstance(operable_group, str):
        raise TypeError("'{0}' must be a string".format(operable_group))

    operation_blocks = operable_group.split()
    left_operand = operation_blocks[0]
    right_operand = operation_blocks[2]
    operator = operation_blocks[1]

    if len(operation_blocks) != 3:
        raise ValueError(
            "'{0}' is not a valid operable group".format(operable_group))

    try:
        left_operand_int = int(left_operand)
        right_operand_int = int(right_operand)
    except ValueError as not_a_number:
        raise not_a_number

    if operator == "LEFT":
        return left_operand
    elif operator == "RIGHT":
        return right_operand
    elif operator == "UP":
        if right_operand_int % left_operand_int == 0:
            return "1"
        else:
            return "0"

    elif operator == "DOWN":
        sum_blocks = left_operand_int + right_operand_int
        if is_prime(sum_blocks):
            return "1"
        else:
            return "0"

    else:
        raise ValueError("'{0}' is not a valid operator".format(operator))


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
            raise ValueError(
                "'{0}' is not a valid break side".format(break_side))
        ValueError: 'bla' is not a valid break side

        >>> break_in_first_operable_group('(23 RIGHT 3 LEFT 12', 'right')
        Traceback (most recent call last):
            raise ValueError("'(23 RIGHT 3 LEFT 12' should start with a digit")
        ValueError: '(23 RIGHT 3 LEFT 12' should start with a digit

        >>> break_in_first_operable_group(4546546)
        Traceback (most recent call last):
            raise TypeError("'{0}' must be a string".format(text))
        TypeError: '4546546' must be a string

    """
    if not isinstance(text, str):
        raise TypeError("'{0}' must be a string".format(text))
    if not text[0].isdigit():
        raise ValueError("'{0}' should start with a digit".format(text))

    split = text.split()
    if break_side == "right":
        head = "{0} ".format(" ".join(split[:2]))
        remainder = " ".join(split[2:])
    elif break_side == "left":
        head = " ".join(split[:1])
        remainder = " {0}".format(" ".join(split[1:]))
    else:
        raise ValueError("'{0}' is not a valid break side".format(break_side))

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
            raise ValueError(
                "'{0}' is not a valid direction".format(direction))
        ValueError: 'bla' is not a valid direction

        >>> break_on_parenthesis("(3 RIGHT 2", "l2r")
        Traceback (most recent call last):
            raise ValueError("{0} does not contain a `)`".format(text))
        ValueError: (3 RIGHT 2 does not contain a `)`

        >>> break_on_parenthesis(489)
        Traceback (most recent call last):
            raise TypeError("'{0}' must be a string".format(text))
        TypeError: '489' must be a string

    """
    if not isinstance(text, str):
        raise TypeError("'{0}' must be a string".format(text))

    if direction == "l2r":
        split = text.split(")", 1)
        try:
            right_split = split[1]
        except IndexError:
            raise ValueError("{0} does not contain a `)`".format(text))

    elif direction == "r2l":
        split = text.rsplit("(", 1)
        try:
            right_split = split[1]
        except IndexError:
            raise ValueError("{0} does not contain a `(`".format(text))

    else:
        raise ValueError("'{0}' is not a valid direction".format(direction))

    left_split = split[0]
    return left_split, right_split


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

        >>> alien_eval("((8 UP 3))")
        0

        # This case follows another parsing path
        # which was not tested with the given examples!
        >>> alien_eval("18 RIGHT (3 LEFT 4)")
        3

        >>> alien_eval(3)
        Traceback (most recent call last):
            raise TypeError("'{0}' must be a string".format(text))
        TypeError: '3' must be a string

        >>> alien_eval(")2 LEFT 4")
        Traceback (most recent call last):
            raise ValueError(
                "'{0}' does not have a valid Alien Language syntax")
        ValueError: ')2 LEFT 4' does not have a valid Alien Language syntax

    """
    # Getting a TypeError is more clear than getting an AtttributeError
    # which would occur on the first split method call if operable_group
    # wasn't a string.
    if not isinstance(text, str):
        raise TypeError("'{0}' must be a string".format(text))
    text_split = text.split()

    if text[0].isdigit():
        # Case: "12"
        if len(text_split) == 1:
            return int(text)
        # Case: "2 RIGHT 12"
        elif len(text_split) == 3:
            result = calculate(text)
            return alien_eval(result)
        else:
            rhead, rremainder = break_in_first_operable_group(text, "right")
            # Case: "2 RIGHT 12 LEFT 3"
            if not rremainder.startswith('('):
                lhead, lremainder = break_in_first_operable_group(rremainder,
                                                                  "left")
                operable_group = "{0}{1}".format(rhead, lhead)
                tmp_result = calculate(operable_group)
                current_string = "{0}{1}".format(tmp_result, lremainder)
                return alien_eval(current_string)
            # Case: "2 RIGHT (3 RIGHT 4)"
            else:
                operable_group = "{0}{1}".format(rhead, alien_eval(rremainder))
                return alien_eval(operable_group)

    elif text.startswith("("):
        # Case: "((3))"
        if len(text_split) == 1:
            left_parenth_removed = text.replace("(", "")
            parentheses_removed_text = left_parenth_removed.replace(")", "")
            return alien_eval(parentheses_removed_text)
        # Case: "(2 RIGHT ((1 LEFT (5 RIGHT 4)) UP 3))"
        else:
            l2r_first, l2r_last = break_on_parenthesis(text, "l2r")
            r2l_last, r2l_first = break_on_parenthesis(l2r_first, "r2l")
            tmp_result = calculate(r2l_first)
            current_string = "{0}{1}{2}".format(r2l_last, tmp_result, l2r_last)
            return alien_eval(current_string)

    else:
        raise ValueError("'{0}' does not have a valid Alien Language syntax".format(text))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
