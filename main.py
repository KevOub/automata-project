# from nfa_class import NFA

# from nfa import Compiler 
from nfa import Compiler 
from regex import Regex

# re = input("in?\t")
# ma = input("match?\t")
# re = "a?b?c?d?e?f*?g"
# re = "a?((b*?a))"
# ma = "aba"
re = "a+b"
ma = "abbbbbbbbbbbbbbbbbbbbbbbbbbbb"

regex_to_test = Regex(re)
print(regex_to_test.postfix)

regex_match = Compiler(regex_to_test.postfix)

print(regex_match.automata.match(ma))

print("---\n---\n----")

print(regex_match.transition_table())

# regex_match.automata.match_and_draw(ma,"test")

regex_match.draw_transition_table("tmp/test.png")
regex_match.flatten()
print(regex_match.transition_table())
regex_match.draw_transition_table("tmp/test.png")
