/***************************************************
 *  Our own little alien language parsing utility  *
 ***************************************************/


// Check if n is a prime.
//
// Args:
//   n (number): The number to check.
//
// Returns:
//   boolean.
//
// Doctests:
//
//   > isPrime(0)
//   false
//   
//   > isPrime(1)
//   false
//  
//   > isPrime(2)
//   true
//  
//   > isPrime(30)
//   false
//  
//   > isPrime(89)
//   true
//
function isPrime(n) {
  for (var i = 2; i < n; i++) {
    if (n % i === 0) {
      return false;
    }
  }

  if (n < 2) {
    return false;
  }
  else {
     return true;
  }
}


// Calculate the result of an operable group.
//
// Args:
//   operableGroup (string): The group to calculate a result of.
// 
// Returns:
//   string.
//
// Doctests:
//   > calculate('1 LEFT 2')
//   '1'
//
//   > calculate('1 RIGHT 2')
//   '2'
//
//   > calculate('32 RIGHT 4')
//   '4'
//
//   > calculate('1 DOWN 2')
//   '1'
//
//   > calculate('1 DOWN 3')
//   '0'
//
//   > calculate('1 UP 2')
//   '1'
//
//   > calculate('8 UP 3')
//   '0'
//
//   > calculate(1)
//   TypeError //'1' is not a valid operable group
//
//   > calculate('1 LEFT 2 RIGHT 4')
//   Error //'1 LEFT 2 RIGHT 4' is not a valid operable group
//
//   > calculate('(1 LEFT 2')
//   Error //Operands must be integers
//
//   > calculate('1 BLA 2')
//   Error //'Bla' is not a valid operator
//
function calculate(operableGroup) {
  // TypeError would be raised either way if operableGroup wasn't a string
  // when the `split` method would be called. However, this error message is 
  // slightly clearer.   
  if (typeof operableGroup !== "string") {
    throw new TypeError("'" + operableGroup + "' must be a string");
  } 

  var operationBlocks = operableGroup.split(" ");
  var leftOperand = operationBlocks[0];
  var rightOperand = operationBlocks[2];
  var operator = operationBlocks[1];

  if (operationBlocks.length !== 3) {
    throw new Error("'" + operableGroup + "' is not a valid operable group");
  }

  var leftOperandNumber = Number(leftOperand);
  var rightOperandNumber = Number(rightOperand);
 
  if (isNaN(leftOperandNumber) || isNaN(rightOperandNumber)) {
    throw new Error("Operands must be integers")
  }

  if (operator === "LEFT") {
    return leftOperand;
  }
  else if (operator === "RIGHT") {
    return rightOperand;
  }
  else if (operator === "UP") {
    if (rightOperandNumber % leftOperandNumber === 0) {
      return "1";
    }
    else {
      return "0";
    }
  }
  else if (operator === "DOWN") {
    sumBlocks = leftOperandNumber + rightOperandNumber;
    if (isPrime(sumBlocks)) {
        return "1";
    }
    else {
        return "0";
    }
  }
  else {
    throw new Error("'" + operator + "' is not a valid operator");
  }
}


// Break alien text into two pieces in the first operable group.
//
// Args:
//    text (string): The alien text to break into pieces.
//
// Kwargs:
//   breakSide (string): The side in the first operable group where the
//     the text should be broken. This is either "right" or "left".
//
// Returns:
//   string.
//
// Doctests:
//   > breakInFirstOperableGroup('3 LEFT 4', 'right')
//   {"head": "3 LEFT ", "remainder": "4"}
//
//   > breakInFirstOperableGroup('23 RIGHT 3 LEFT 12', 'right')
//   {"head": "23 RIGHT ", "remainder": "3 LEFT 12"}
//
//   > breakInFirstOperableGroup('3 LEFT 4', 'left')
//   {"head": "3", "remainder": " LEFT 4"}
//
//   > breakInFirstOperableGroup('23 RIGHT 3 LEFT 12', 'left')
//   {"head": "23", "remainder": " RIGHT 3 LEFT 12"}
//
//   > breakInFirstOperableGroup('23 RIGHT 3 LEFT 12', 'bla')
//   Error //'bla' is not a valid break side
//
//   > breakInFirstOperableGroup('(23 RIGHT 3 LEFT 12', 'right')
//   Error //'(23 RIGHT 3 LEFT 12' should start with a digit
//
//   > breakInFirstOperableGroup(4546546, 'right')
//   TypeError //'4546546' must be a string
//
function breakInFirstOperableGroup(text, breakSide) {
  if (typeof text !== "string") {
    throw new TypeError("'" + text + "' must be a string"); 
  }

  var textStartsWithNumber = !isNaN(Number(text[0]));
  if (!textStartsWithNumber) {
    throw new Error("'" + text + "' should start with a digit");
  }

  var split = text.split(" ");
  if (breakSide === "right") {
    var head = split.slice(0, 2).join().replace(/,/g, " ") + " "
    var remainder = split.slice(2).join().replace(/,/g, " ")
  }
  else if (breakSide == "left") {
    var head = split.slice(0, 1).join().replace(/,/g, " ")
    var remainder = " " + split.slice(1).join().replace(/,/g, " ")
  }
  else {
    throw new Error("'" + breakSide + "' is not a valid break side");
  }

  return {"head": head, "remainder": remainder}
}


// Break text on first encountered parenthesis.
//
// Args:
//     text (string): The alien text to break into pieces.
//
// Kwargs:
//     direction (string): The direction in which the text is processed to break
//         it into pieces.
//         If the direction is "l2r" then the text will be broken on the
//         first encountered right parenthesis; `)`.
//         If the direction is "r2l" then the text will be broken on the
//         first encountered left parenthesis; `(`.
//
// Returns:
//     string.
//
// Doctests:
//   > breakOnParenthesis("(2 RIGHT 3)", "l2r")
//   {"leftSplit": "(2 RIGHT 3", "rightSplit": ""}
//
//   > breakOnParenthesis("(1 LEFT (2 RIGHT 3))", "l2r")
//   {"leftSplit": "(1 LEFT (2 RIGHT 3", "rightSplit": ")"}
//
//   > breakOnParenthesis("(2 UP ((1 LEFT (2 RIGHT 3)) UP 3)) DOWN 11", "l2r")
//   {"leftSplit": "(2 UP ((1 LEFT (2 RIGHT 3", "rightSplit": ") UP 3)) DOWN 11"}
//
//   > breakOnParenthesis('(2 RIGHT 3', "r2l")
//   {"leftSplit": "", "rightSplit": "2 RIGHT 3"}
//
//   > breakOnParenthesis("(1 LEFT (2 RIGHT 3", "r2l")
//   {"leftSplit": "(1 LEFT ", "rightSplit": "2 RIGHT 3"}
//
//   > breakOnParenthesis("(2 UP ((1 LEFT (2 RIGHT 3", "r2l")
//   {"leftSplit": "(2 UP ((1 LEFT ", "rightSplit": "2 RIGHT 3"}
//
//   > breakOnParenthesis('(2 RIGHT 3)', "bla")
//   Error //'bla' is not a valid direction
//
//   > breakOnParenthesis("(3 RIGHT 2", "l2r")
//   Error //(3 RIGHT 2 does not contain a `)`
//
//   > breakOnParenthesis(489)
//   TypeError //'489' must be a string
//
function breakOnParenthesis(text, direction) {
  if(typeof text !== "string") {
    throw new TypeError("'" + text + "' must be a string"); 
  }

  if (direction === "l2r") {
    var splitStri = ")";
    var tmpSplit = text.split(splitStri);

    if (tmpSplit.join().replace(/,/g, "") === text) {
      throw new Error("'" + text + "' does not contain a `)`");
    }

    var leftSplit = tmpSplit.shift();
    var rightSplit = tmpSplit.join(splitStri);
  }
  else if (direction === "r2l") {
    var splitStri = "(";
    var tmpSplit = text.split(splitStri)

    if (tmpSplit.join().replace(/,/g, "") === text) {
      throw new Error("'" + text + "' does not contain a `(`")
    }

    var rightSplit = tmpSplit.pop();
    var leftSplit = tmpSplit.join(splitStri);
  }
  else {
    throw new Error("'" + direction + "' is not a valid direction");
  }

  return {"leftSplit": leftSplit, "rightSplit": rightSplit};
}


// Evaluate a piece of text in our alien language to a number.
//
// Args:
//     text (string): A piece of text with alien language syntax.
//
// Returns:
//     number.
//
// Doctests:
//   > alienEval("(2 DOWN ((1 LEFT (2 RIGHT 3)) UP 3)) DOWN 11")
//   0
//
//   > alienEval("(1 LEFT 2) RIGHT 1")
//   1
//
//   // Bonus : }
//   > alienEval("8 LEFT 3 LEFT 4")
//   8
//
//   > alienEval("((8 UP 3))")
//   0
//
//   // This case follows another parsing path
//   // which was not tested with the given examples!
//   > alienEval("18 RIGHT (3 LEFT 4)")
//   3
//
//   > alienEval(3)
//   TypeError //'3' must be a string
//
//   > alienEval(")2 LEFT 4")
//   Error // ')2 LEFT 4' does not have a valid Alien Language syntax
//
function alienEval(text) {
  // TypeError would be raised either way if text wasn't a string
  // when the `split` method would be called. However, this error message is 
  // slightly clearer.   
  if (typeof text !== "string") {
    throw TypeError("'" + text + "' must be a string")
  }

  var textSplit = text.split(" ")

  var textStartsWithNumber = !isNaN(Number(text[0]));
  if (textStartsWithNumber) {
    // Case: "12"
    if (textSplit.length == 1) {
      return Number(text) 
    }
    // Case: "2 RIGHT 12"
    else if (textSplit.length == 3) {
      var result = calculate(text);
      return alienEval(result)
    }
    else {
      var rOperableGroupDeconstruction = breakInFirstOperableGroup(text, "right");
      var rHead = rOperableGroupDeconstruction.head;
      var rRemainder = rOperableGroupDeconstruction.remainder;

      // Case: "2 RIGHT 12 LEFT 3"
      if (rRemainder[0] !== "(") {
        var lDeconstruction = breakInFirstOperableGroup(rRemainder, "left")
        var lHead = lDeconstruction.head
        var lRemainder = lDeconstruction.remainder

        var operableGroup = rHead + lHead
        var tmpResult = calculate(operableGroup)
        var currentString = tmpResult + lRemainder
        return alienEval(currentString)
      }
      // Case: "2 RIGHT (3 RIGHT 4)"
      else {
          var operableGroup = rHead + alienEval(rRemainder)  
          return alienEval(operableGroup)
      }
    }
  }
  else if (text[0] === "(") {
    // Case: "((3))"
    if (textSplit.length === 1) {
      var leftParenthRemoved = text.split("(").join("")
      var parenthesesRemovedText = leftParenthRemoved.split(")").join("")
      return alienEval(parenthesesRemovedText)
    }
    // Case: "(2 RIGHT ((1 LEFT (5 RIGHT 4)) UP 3))"
    else {
      var l2rParenthesisDeconstruction = breakOnParenthesis(text, "l2r")
      var l2rFirst = l2rParenthesisDeconstruction.leftSplit
      var l2rLast = l2rParenthesisDeconstruction.rightSplit

      var r2lParenthesisDeconstruction = breakOnParenthesis(l2rFirst, "r2l")
      var r2lFirst = r2lParenthesisDeconstruction.rightSplit 
      var r2lLast = r2lParenthesisDeconstruction.leftSplit 

      var tmpResult = calculate(r2lFirst)
      var currentString = r2lLast + tmpResult + l2rLast
      return alienEval(currentString)
    }
  }
  else {
    throw new Error("'" + text + "' does not have a valid Alien Language syntax")
  }
}
