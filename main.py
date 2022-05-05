# from nfa_class import NFA

# from nfa import Compiler 
from nfa2 import Compiler 
from regex import Regex

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
