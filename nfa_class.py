

from collections import deque


# class State():

#     def __init__(self) -> None:
#         label = ""
#         edges = []
#         transitions = {}
        


class NFA():

    # THE SPECS OF OPERATION ARE FROM HERE https://github.com/rohaquinlop/automathon
    """
     A Class used to represent a Non-Deterministic Finite Automaton

    ...

    Attributes
    - - - - - - - - - - - - - - - - - -
    Q : set
      Set of strings where each string represent the states.
      Ex:
        Q = {'q0', 'q1', 'q2'}

    sigma : set
      Set of strings that represents the alphabet.
      Ex:
        sigma = {'0', '1'}

    delta : dict
      Dictionary that represents the transition function.
      Ex:
        delta = {
                  'q0' : {
                          '0' : {'q0', 'q2'},
                          '1' : {'q1', 'q2', 'q3'}
                         },
                  'q1' : {
                          '0' : {'q2'},
                          '1' : {'q0', 'q1'}
                         },
                  'q2' : {
                          '0' : {'q1', 'q2'},
                          '' : {'q2'}
                         },
                }

    initialState : str
      String that represents the initial state from where any input is processed (initialState ∈ Q / initialState in Q).
      Ex:
        initialState = 'q0'

    F : set
      Set of strings that represent the final state/states of Q (F ⊆ Q).
      Ex:
        F = {'q0', 'q1'}


    Methods
    - - - - - - - - - - - - - - - - - -
    fromRegex(r : str) -> None : Updates NFA to reflect that of a regular expression
    accept(S : str) -> bool : Returns True if the given string S is accepted by the NFA
    isValid() -> bool : Returns True if the NFA is a valid automata


    """

    def __init__(self, Q: set, sigma: set, delta: dict, initialState: str, F: set):
        """
        Parameters
        - - - - - - - - - - - - - - - - - -

        Q : set
          Set of strings where each string represent the states.

        sigma : set
          Set of strings that represents the alphabet.

        delta : dict
          Dictionary that represents the transition function.

        initialState : str
          String that represents the initial state from where any input is processed (initialState ∈ Q / initialState in Q).

        F : set
          Set of strings that represent the final state/states of Q (F ⊆ Q).
        """
        self.Q = Q
        self.sigma = sigma
        self.delta = delta
        self.initialState = initialState
        self.F = F

    def accept(self, S: str) -> bool:
        """ Returns True if the given string S is accepted by the NFA

        The string S will be accepted if ∀a · a ∈ S ⇒ a ∈ sigma, which means that all the characters in S must be in sigma (must be in the alphabet).

        Parameters
        - - - - - - - - - - - - - - - - - -
        S : str
          A string that the NFA will try to process.
        """

        q = deque()  # queue -> states from i to last character in S | (index, state)
        q.append([0, self.initialState])  # Starts from 0
        ans = False  # Flag

        print(f"TESTING ACCEPTANCE OF {S}")
        print("---")
        while q and not ans:
            frontQ = q.popleft()  # get start state
            idx = frontQ[0]
            state = frontQ[1]
            print(f"\tfrontQ = {frontQ}\tidx={idx}\t\tstate={state}")
            print(f"q={list(q)}")

            if idx == len(S):
                if state in self.F:
                    ans = True
            elif S[idx] not in self.sigma:
                print(f"[!] S[idx] = {S[idx]} is not in {self.sigma}!")
                return False
            elif state in self.delta:
                print(f"\t\t\t\tS[idx]={S[idx]}")
                # search through states to find the gaurds
                for transition in self.delta[state].items():
                    d = transition[0]  # the guard
                    states = transition[1]
                    print(f"\t\t\t\td={d}\tstates={states}\n")

                    if d == "":
                        # is epsilon
                        for state in states:
                            # do not consume character
                            q.append([idx, state])
                    elif S[idx] == d:
                        for state in states:
                            # Consume character
                            q.append([idx + 1, state])
        if S == "":
            ans = True

        print(f"\n---\nRESULT={ans}\n---")
        return ans

    def isValid(self) -> bool:
        """ Returns True if the NFA is an valid automata """

        # Validate if the initial state is in the set Q
        if self.initialState not in self.Q:
            # raise SigmaError(self.initialState, 'Is not declared in Q')
            return False

        # Validate if the delta transitions are in the set Q
        for d in self.delta:
            if d != "" and d not in self.Q:
                # raise SigmaError(d, 'Is not declared in Q')
                return False

            # Validate if the d transitions are valid
            for s in self.delta[d]:
                if s != "" and s not in self.sigma:
                    #    raise SigmaError(s, 'Is not declared in sigma')
                    return False
                for q in self.delta[d][s]:
                    if q not in self.Q:
                        #raise SigmaError(self.delta[d][s], 'Is not declared Q')
                        return False

        # Validate if the final state are in Q
        for f in self.F:
            if f not in self.Q:
                # raise SigmaError(f, 'Is not declared in Q')
                return False

        # None of the above cases failed then this NFA is valid
        return True
