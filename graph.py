from cProfile import label
from time import time
import numpy as np
import timeit
from nfa import Compiler
from regex import Regex
from matplotlib import pyplot as plt
import re


# re_mine = "((a*).d+.(b*).c)"
# re_act = "((a*)d+(b*)c)"
# re_mine = "(a?).(a*).(a?).a.a"
# re_act = "a?a*a?aaa"
re_mine = "((a*).(b*).c)"
# re_act = "a*b*" 
# re_act = "(a*b?)|(c*d?)"
re_act = "((a*)(b*)c)"

regex_to_test = Regex(re_mine)
regex_match = Compiler(regex_to_test.postfix)

n_as = "a"
n_bs = "b"
# ma = f"{n_as}d{n_bs}c"
ma = "c"

# re_engine_bi = re.compile(re_act)
pattern = re.compile(re_act)
MAX_COUNT = 5000
r = range(1, 50000)
dt_bi = []

start_time = timeit.default_timer()
for i in r: 
    # np.math.factorial(i)
    # re.match(re_act,ma)
    pattern.findall(ma)
    # ma = f"{n_as}d{n_bs}c"
    ma = "a" if i < (5000 / 2) else "b" + ma
    ma = "a" + ma
    # ma[-1] = "c"
    
    # n_as += "a"
    # n_bs += "b"
    dt_bi.append(timeit.default_timer()-start_time)

n_as = "a"
n_bs = "b"
# ma = f"{n_as}d{n_bs}c"
ma = "c"

# dt_my = []
# start_time = timeit.default_timer()
# for i in r:
#     regex_match.automata.match(ma)
#     # ma = f"{n_as}d{n_bs}c"
#     # n_as += "a"
#     # n_bs += "b"
#     # ma += "a"
#     ma = "a" + ma
#     # ma = "a" if i < (2500 / 2) else "b" + ma
#     dt_my.append(timeit.default_timer()-start_time)


# plt.plot(range(1,len(test)+1),test,label="TEST")
# data = {"a": dt_bi, "b": dt_my}
plt.plot(r,dt_bi,label="BUILT-IN")
# plt.plot(r,dt_my,label="MINE")

plt.legend()
plt.show()