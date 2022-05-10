from string import  ascii_lowercase, ascii_uppercase
# https://github.com/kevinniland/Thompsons-Construction-on-NFAs/blob/master/thompsons.py


class Regex():

    def __init__(self, expr, lang=[c for c in ascii_lowercase], postfix=""):
        self.expr = expr
        self.lang = lang
        self.infix = expr
        self.postfix = postfix
        self.infixToPostfix()

    def peek(self, stack):
        return stack[-1] if stack else None

    def calc_prec(self, a, b):
        precedence = {"*": 2, "?": 0, "+": 1}
        if a in precedence and b in precedence:
            return precedence[a] >= precedence[b]

    def infixToPostfix(self):
        """
        [] If the incoming symbols is an operand, print it..

        [] If the incoming symbol is a left parenthesis, push it on the stack.

        [] If the incoming symbol is a right parenthesis: discard the right parenthesis, pop and print the stack symbols until you see a left parenthesis. Pop the left parenthesis and discard it.

        [] If the incoming symbol is an operator and the stack is empty or contains a left parenthesis on top, push the incoming operator onto the stack.

        If the incoming symbol is an operator and has either higher precedence than the operator on the top of the stack, or has the same precedence as the operator on the top of the stack and is right associative -- push it on the stack.

        If the incoming symbol is an operator and has either lower precedence than the operator on the top of the stack, or has the same precedence as the operator on the top of the stack and is left associative -- continue to pop the stack until this is not true. Then, push the incoming operator.

        At the end of the expression, pop and print all operators on the stack. (No parentheses should remain.)

        """

        output = ""  # "print" to
        operand_stack = []  # stack
        operators = ["*", "+", "|", "?"]
        ploop = False
        count = 0
        for c in self.expr:
            if c in self.lang:
                output += c
                # if count > 0:
                    # count = 0 
                    # output += chr(0x08)
                # else:
                    # count += 1

            elif c == "(":
                operand_stack.append(c)
            elif c == ")":
                top = self.peek(operand_stack)
                while top is not None and top != "(":
                    output += operand_stack.pop()
                    top = self.peek(operand_stack)
                operand_stack.pop()  # ignore "("

            else:
                top = self.peek(operand_stack)
                while top is not None and top not in "()" and self.calc_prec(top, c):
                    output += operand_stack.pop()
                    top = self.peek(operand_stack)
                operand_stack.append(c)

        while self.peek(operand_stack) is not None:
            output += operand_stack.pop()

        # val = operand_stack.pop()
        # output += val if operand_stack != "(" else ""
        # return output
        print(operand_stack)
        self.postfix = output

