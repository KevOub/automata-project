from nfa import NFA


Q = {'q1', 'q2', 'q3', 'q4'}
sigma = {'0', '1'}
delta = {
          'q1' : {
                  '0' : {'q1'},
                  '1' : {'q1', 'q2'}
                  },
          'q2' : {
                  '0' : {'q3'},
                  '' : {'q3'}
                  },
          'q3' : {
                  '1' : {'q4'},
                  },
          'q4' : {
                  '0' : {'q4'},
                  '1' : {'q4'},
                  },
        }
initialState = 'q1'
F = {'q4'}

automata2 = NFA(Q, sigma, delta, initialState, F)

automata2.accept("0000011")   #True
automata2.accept("000001")    #False