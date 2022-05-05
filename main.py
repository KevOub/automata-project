# from nfa_class import NFA

# from nfa import Compiler 
from nfa2 import Compiler 
from regex import Regex


# Q = {'q1', 'q2', 'q3', 'q4'}
# sigma = {'0', '1'}
# delta = {
#           'q1' : {
#                   '0' : {'q1'},
#                   '1' : {'q1', 'q2'}
#                   },
#           'q2' : {
#                   '0' : {'q3'},
#                   '' : {'q3'}
#                   },
#           'q3' : {
#                   '1' : {'q4'},
#                   },
#           'q4' : {
#                   '0' : {'q4'},
#                   '1' : {'q4'},
#                   },
#         }
# initialState = 'q1'
# F = {'q4'}

# automata2 = NFA(Q, sigma, delta, initialState, F)

# automata2.accept("0000011")   #True
# automata2.accept("000001")    #False

# a = Regex("a?b?b?a")
# b = Compiler(a.postfix)

# c = b.compile()
# print(a.postfix)
# print(b.match("ab"))
# print(b.automata.match("abba"))
# compile(b)

# re = input("in?\t")
# ma = input("match?\t")
# re = "a?b?c?d?e?f*?g"
re = "a?((b*?a))"
ma = "aba"

regex_to_test = Regex(re)
print(regex_to_test.postfix)

regex_match = Compiler(regex_to_test.postfix)

print(regex_match.automata.match(ma))

print("---\n---\n----")

# regex_match.transition_table()