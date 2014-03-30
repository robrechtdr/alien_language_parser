## Problem

> I received this problem during an application for a position as a Python Software Engineer. 

There is an alien language which is made only of numbers, parenthesis and four basic operators (LEFT, RIGHT, UP, DOWN).
LEFT/RIGHT/UP/DOWN are operators which always have an element to their right and left.

* UP is an operator that returns 1 if the element to its right can be divided by the element to its left, 0 otherwise.
* DOWN is an operator that returns 1 if the sum of the elements to its right and left is a prime number, 0 otherwise.
* LEFT is an operator that always returns the element to its left and ignores the one to its right.
* RIGHT is an operator that always returns the element to its right and ignores the one to its left.
* Parenthesis and numbers work just like regular parenthesis and numbers in our world.
* Bonus points if you can parse strings with no parenthesis (or with redundant parenthesis) always following the "right to left" precedence rule. 

Examples:

print alien_eval("1 LEFT 2") 			#returns 1   
print alien_eval("1 RIGHT 2") 			#returns 2    
print alien_eval("(1 LEFT 2) RIGHT 1")	#returns 1     
print alien_eval("1 DOWN 2") 			#returns 1      
print alien_eval("1 DOWN 3") 			#returns 0      
print alien_eval("1 UP 2")			#returns 1      
print alien_eval("8 UP 3")			#returns 0       
print alien_eval("LEFT 3 LEFT 4")	#bonus. returns 8      
print alien_eval("((8 UP 3))")			#bonus. returns 0       
print alien_eval("(2 DOWN ((1 LEFT (2 RIGHT 3)) UP 3)) DOWN 11")		#returns ?

Your task is to write a short Python program that can parse this language without using any non standard python 2.7 library (and/or the eval function). Furthermore you should NOT use the REGEX module.


## Solution

### Python

    python alien_language_parser.py

> Check the git branches for alternative algorithms (which use e.g. a while loop instead of recursion).

### Javascript

> Install [doctest](https://github.com/davidchambers/doctest) with `npm install -g doctest`

    doctest alien_language_parser.js

If you want to run the program without doctests then run the following:

    node alien_language_parser.js
