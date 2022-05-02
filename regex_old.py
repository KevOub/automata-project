from collections import deque

from numpy import outer

class Node():

    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


class Regex():


    def __init__(self, expression, postfix=""):
        self.expression = expression
        self.postfix = postfix
        # self.tree = self.construct(expression)

    def isOperand(self,c: str) -> bool:
        return c in ["*","+"]
    
    def precedence(self,c : str) -> int:
        if c == "*" or c == "+":
            return 0 
            

    # turn input to postfix (I.E., a+b -> ab+)
    def inTopost(self, expression : str) -> str:
        """
        If the current token is an opening parenthesis, push it into the stack.
        If the current token is a closing parenthesis, pop tokens from the stack until a corresponding opening parenthesis are popped. Append each operator to the end of the postfix expression.
        Append the current token to the end of the postfix expression if it is an operand
        If the current token is an operator, append it to the postfix expression with higher precedence than the operator on top of the stack. 
            If it has lower precedence, first pop operators from the stack until we have a higher precedence operator on top, or the stack becomes empty.
        Finally, if you have any remaining operators in the stack, add them to the end of the postfix expression until the stack is empty and return the postfixed expression.
        """
        s = list()
        output = "" # output is the result of the code
        ploop = False # way to see if stuck in between paranthesis
        for c in expression:
            # look for open paranthesis
            if c == ")":
                ploop = True
            else:
                ploop = False

            if self.isOperand(c):
                s.append(c)
            elif c == "(":
                output += c
                s.append(c)
            else:
                output += c

            
            while ploop:
                val = s.pop()
                if val == "(":
                    ploop = False
                else:
                    output += val
         
        while len(s) != 0:
            output += s.pop()

        return output
                




    def construct(self, expression: str):
        s = deque()        
        for c in expression:
            # if operand
            if self.isOperand(c):
                # grab two nodes and put it in x and y
                x = s.pop()
                y = s.pop()

                # create a new operator from it
                node = Node(c, x, y)

                # push current node onto stack
                s.append(node)

            # otherwise create new tree
            else:
                s.append(Node(c))

        # return head of tree
        return s[-1]


    # Print the postfix expression for an expression tree
    def postorder(self,root):
        if root is None:
            return
        self.postorder(root.left)
        self.postorder(root.right)
        print(root.data, end='')


    # Print the infix expression for an expression tree
    def inorder(self,root):
        if root is None:
            return

        # if the current token is an operator, print open parenthesis
        if self.isOperator(root.data):
            print('(', end='')

        self.inorder(root.left)
        print(root.data, end='')
        self.inorder(root.right)

        # if the current token is an operator, print close parenthesis
        if self.isOperator(root.data):
            print(')', end='')

    def __str__(self) -> str:
        self.postorder(self.tree)
        return ""

test = Regex("(ab+)+c")
# print(test)
print(test.inTopost("(a+b)a"))
