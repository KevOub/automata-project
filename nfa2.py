

from os import stat

from flask import current_app
from itsdangerous import exc


class State():

    def __init__(self, name) -> None:
        self.name = name
        self.transitions = {}
        self.epsilon = []
        self.final_state = False

    def add_transition(self, c, state):
        if c in self.transitions:
            self.transitions[c].append(state)
        else:
            self.transitions.setdefault(c, []).append(state)
            # self.transitions.update({c: []})
            # self.transitions[c].append(state)

    def __str__(self) -> str:
        output = f"[{self.name}]"
        for k, v in self.transitions.items():
            for state in v:
                output += f"-{k}->{state}"

        return output
        # return f"{self.name} -{}-> {self.transitions}"


class NFA():

    def __init__(self, begin, end):
        self.begin = begin
        self.end = end
        end.is_end = True

    def addstate(self, state, state_set):  # add state + recursively add epsilon transitions
        if state in state_set:
            return
        state_set.add(state)
        for eps in state.epsilon:
            self.addstate(eps, state_set)

    def next_state(self, c, current_state):
        # if c in current_state.transitions.keys():
        # return
        for key in current_state.transitions.keys():
            if key == c:
                return current_state.transitions[key]
            elif key == "":
                return self.next_state(c, current_state.transitions[""])
        return None

    def addstate(self, state, state_set):  # add state + recursively add epsilon transitions
        if state in state_set:
            return
        state_set.add(state)
        for eps in state.epsilon:
            self.addstate(eps, state_set)

    def add_epsilon(self, state, state_set, c):
        if state in state_set:
            return state_set
        state_set.add(state)
        if any(["" == k for k in state.transitions.keys()]):
            for estate in state.transitions[""]:
                if c in estate.transitions.keys():
                    self.add_epsilon(estate, state_set,c)

        
    def match(self, msg):
        current_states = set()
        # self.addstate(self.accept, current_states)
        current_states.add(self.begin)
        print(self.begin)

        for c in msg:
            next_states = set()
            for state in current_states:

                    # then add ones that match
                if c in state.transitions.keys():
                    # next_states = self.addstate_recursive(state,next_states)
                    trans_state = state.transitions[c]
                    for ts in trans_state:
                        next_states.add(ts)
                
                if any([k == "" for k in state.transitions.keys()]):
                    trans_state = state.transitions[""]
                    for ts in trans_state:
                        next_states.add(ts)

            current_states = next_states

        print("---")
        for s in current_states:
            print(s)
            if s.final_state:
                return True
        return False


class Compiler():

    def __init__(self, regex):
        self.regex = regex
        self.states = 1
        self.automata = self.compile()

    def add_state(self) -> State:
        self.states += 1
        return State(f"q{self.states}")

    def compile(self):

        nfa_stack = []

        # go through character by character
        for c in self.regex:
            # concat
            if c == "?":
                """
                n2 = nfa_stack.pop()
                n1 = nfa_stack.pop()
                n1.end.is_end = False
                n1.end.epsilon.append(n2.start)
                nfa = NFA(n1.start, n2.end)
                nfa_stack.append(nfa)
                """
                # pop
                nfa2 = nfa_stack.pop()
                nfa1 = nfa_stack.pop()

                nfa1.end.final_state = False
                nfa1.end.add_transition("", nfa2.begin)

                newNFA = NFA(nfa1.begin, nfa2.end)
                nfa_stack.append(newNFA)

                # nfa1.begin.add_transition("",nfa2.begin)

                # push onto stack
                # nf2 = nfa_stack.pop()
                # nf1 = nfa_stack.pop()
                # # make the first not end and set its final state to go to nf2
                # nf1.accept.is_end = False
                # nf1.initial.epsilon.append(nf2)
                # # merge nf1 and nf2 via removing nf1.accept & nf2.initial
                # newNFA = nfa(nf1.initial, nf2.accept)
                # nfa_stack.append(newNFA)

            else:
                s0 = self.add_state()
                s1 = self.add_state()

                s0.add_transition(c, s1)
                # push onto stack
                newNFA = NFA(s0, s1)
                nfa_stack.append(newNFA)

        return nfa_stack[-1]
