import re
import operator

import distribution

class InputHandler:
    def __init__(self, match_string):
        self.match_str = match_string

    def match(self):
        return re.match("^"+self.regex+"$", self.match_str)

    def __repr__(self):
        return "H({})".format(self.match_str)

class BracketHandler(InputHandler):
    left_bracket = "("
    right_bracket = ")"
    regex = "[\{}\{}]".format(left_bracket, right_bracket)

    def is_left_bracket(self):
        return self.match_str == self.left_bracket

    def is_right_bracket(self):
        return self.match_str == self.right_bracket

class OperatorHandler(InputHandler):
    precedence = {  "<":-1,
                    ">":-1,
                    "=":-1,
                    "<=":-1,
                    ">=":-1,
                    "+":0,
                    "-":0,
                    "*":1
                 }
    symbol_to_operation = { "<": operator.lt,
                            ">": operator.gt,
                            "<=": operator.le,
                            ">=": operator.ge,
                            "=": operator.eq,
                            "+": operator.add,
                            "-": operator.sub,
                            "*": operator.mul,
                          }
    regex = "|".join("("+"".join("\\"+j for j in i)+")" for i in precedence.keys())

    def __lt__(self, other):
        return self.precedence[self.match_str] < self.precedence[other.match_str]

    def __gt__(self, other):
        return self.precedence[self.match_str] > self.precedence[other.match_str]

    def __ne__(self, other):
        if other is None:
            return True
        return self.precedence[self.match_str] != self.precedence[other.match_str]

    def __eq__(self, other):
        if other is None:
            return False
        return self.precedence[self.match_str] == self.precedence[other.match_str]

    def __call__(self):
        return self.symbol_to_operation[self.match_str]

class OperandHandler(InputHandler):

    def __call__(self, analytic):
        match = self.match()
        if match and analytic:
            return self.solve()
        elif match and not analytic:
            return self.sample()
        else:
            return None

class IntegerHandler(OperandHandler):
    regex = "([0-9]+)"

    def sample(self):
        return int(self.match_str)

    def solve(self):
        return distribution.DiscreteDistribution({int(self.match_str):1})

class DiceHandler(OperandHandler):
    regex = "([0-9]*)d([1-9][0-9]*)"

    def sample(self):
        distr = self._get_distribution()
        return sum(distr.sample() for i in range(self.repeats))

    def solve(self):
        distr = self._get_distribution()
        return sum(distr for i in range(self.repeats))

    def _get_distribution(self):
        match = self.match()
        if match.groups()[0]:
            self.repeats = int(match.groups()[0])
        else:
            self.repeats = 1
        dietype = int(match.groups()[1])
        return distribution.DiceDistribution(dietype)

class FateDiceHandler(DiceHandler):
    regex = "([0-9]*)F"

    def _get_distribution(self):
        match = self.match()
        if match.groups()[0]:
            self.repeats = int(match.groups()[0])
        else:
            self.repeats = 1
        return distribution.DiscreteDistribution({-1:2, 0:2, 1:2})

def calculate(input_string, analytic):
    postfix_list = _parse(input_string)
    return_value = _eval_postfix(postfix_list, analytic)
    return return_value

def _parse(input_string):
    operand_handlers = (DiceHandler, FateDiceHandler, IntegerHandler)

    def handle_operand(operand):
        for handler in operand_handlers:
            handler_instance = handler(operand)
            if handler_instance.match():
                return handler_instance
        else:
            raise ValueError("Unknown operand {}".format(operand))

    infix_list = []

    current_position = 0
    for operator_match in re.finditer(BracketHandler.regex+"|"+OperatorHandler.regex, input_string):
        operand = input_string[current_position:operator_match.span()[0]].strip()
        operator = operator_match[0].strip()
        current_position = operator_match.span()[1]

        if len(operand)>0:
            infix_list.append(handle_operand(operand))
        if OperatorHandler(operator).match():
            infix_list.append(OperatorHandler(operator))
        elif BracketHandler(operator).match():
            infix_list.append(BracketHandler(operator))
    if len(input_string[current_position:].strip()) > 0:
        infix_list.append(handle_operand(input_string[current_position:]))
    postfix_list = _infix_to_postfix(infix_list)

    return postfix_list

def _eval_postfix(postfix_list, analytic):

    value_stack = []

    for handler in postfix_list:
        if type(handler) == OperatorHandler:
            operand1 = value_stack.pop()
            operand2 = value_stack.pop()
            value_stack.append(handler()(operand1, operand2))
        else:
            value_stack.append(handler(analytic))
    return value_stack.pop()

def _infix_to_postfix(infix_input):
    #https://en.wikipedia.org/wiki/Shunting-yard_algorithm

    infix_input = list(infix_input)

    def get_top_token():
        if len(operator_stack)>0:
            top_token = operator_stack[-1]
        else:
            top_token = None
        return top_token

    operator_stack = []
    output = []

    while infix_input:
        token = infix_input.pop(0)

        if (issubclass(type(token),OperandHandler)):
            output.append(token)

        if (type(token) == OperatorHandler):
            top_token = get_top_token()
            while   ( top_token != None ) and \
                    ( type(top_token) == OperatorHandler) and \
                    ( top_token > token ):
                output.append(operator_stack.pop())
                top_token = get_top_token()
            operator_stack.append(token)

        elif (type(token) == BracketHandler) and \
            token.is_left_bracket():
            operator_stack.append(token)

        elif (type(token) == BracketHandler) and \
            token.is_right_bracket():
            top_token = get_top_token()
            if not top_token:
                raise ValueError("Mismatched parenthesis")
            while (type(top_token) != BracketHandler) or \
                    (not top_token.is_left_bracket()):
                output.append(operator_stack.pop())
                top_token = get_top_token()
            operator_stack.pop()

    while operator_stack:
        if (get_top_token() is "(") or (get_top_token() is ")"):
            raise ValueError("Mismatched parenthesis")
        output.append(operator_stack.pop())

    return output
