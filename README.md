REFERENCE:
https://github.com/rohaquinlop/automathon
https://www.usna.edu/Users/cs/wcbrown/courses/F18SI340/lec/l18/lec.html
https://medium.com/swlh/visualizing-thompsons-construction-algorithm-for-nfas-step-by-step-f92ef378581b

## ALGORITHM FOR VALIDATION

1) turn regex from infix to postfix 
2) turn postfix into NFA using thompsons algorithm
3) match against NFA to determine if string matches

#### regex.py

The whole point of `regex.py` is to turn the regular expression from infix to postfix.
Computers are dumb and it does not recognize infix so we need to convert it
If there is a parsing issue, it probably is here

```python
class Regex():

    def __init__(self, expr, lang=[c for c in ascii_lowercase], postfix=""):
        self.expr = expr
        self.lang = lang
        self.infix = expr
        self.postfix = postfix
        self.infixToPostfix()
```

###### How To Use

```python
from regex import Regex

re = "a+b" # regex to input
regex_to_test = Regex(re) # now has the infix and postfix reference

print(regex_to_test.postfix)
print(regex_to_test.infix)
```



#### nfa2.py

Implements `State()`, `NFA()`, and `Compiler()` classes

The `State()` class is as follows
```python
class State():

    def __init__(self, name) -> None:
        self.name = name
        self.transitions = {}
        self.epsilon = []
        self.final_state = False
```
which encapsulates each individual state for an NFA

The `NFA()` class is as follows
```python
class NFA():

    def __init__(self, begin, end):
        self.begin = begin
        self.end = end
        end.final_state = True

```
Which holds the start and and of two states. This is used for the algorithm of Thompson's Algorithm

The `Compiler()` class is as follows
```python
class Compiler():

    def __init__(self, regex):
        self.regex = regex
        self.states = 1
        self.automata = self.compile()
```
Where it takes `postfix` version of the regular expression, sends it to the `compile()` function, and generates a `NFA`


###### How To Use

```python
from nfa2 import Compiler 
from regex import Regex

re = "a?((b*?a))" # the expression
ma = "aba" # what we are matching against

regex_to_test = Regex(re) # create postfix
print(regex_to_test.postfix) 

regex_match = Compiler(regex_to_test.postfix) # make an NFA

print(regex_match.automata.match(ma)) # call not the compiler but the compiler's internal NFA
```


#### testing.py

run it to see if it passes the tests layed out in `testing/test_suite.dat`

#### bot.py

run it to have a discord bot test your regexes

Key is stored in `bot/secret.key`

#### ref/*
files I used for reference