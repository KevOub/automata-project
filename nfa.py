# from os import stat
# from nfa_class import NFA
import json

# # Represents a state with two arrows, labelled by 'label'
# # Use 'None' for a label representing 'e' arrows


class state:
    label = None
    edge = {}  # {from label : {input : [output]}}


class State():

    def __init__(self, name) -> None:
        self.name = name
        self.epsilon = []
        self.transitions = {}  # char -> []state
        self.is_end = False

    # def add_transition(self,char, to):
    #     if char in self.transitions:
    #         self.transitions[char].append(to)
    #     else:
    #         self.transitions.update({char:[]})
    #         self.transitions[char].append(to)

    # def pretty_transitions(self):
    #     output = ""
    #     for char,state in self.transitions.items():
    #         output += f" initial {self.name} - {char} : {state} \n"

    #     return output
    def pretty(self,d, indent=0):
        for key, value in d.items():
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                self.pretty(value, indent+1)
            else:
                print('\t' * (indent+1) + str(value))

    def __str__(self) -> str:
        output = f"{self.name} : {self.is_end}"
        output += "\n---\n"
        output += f"\tT={self.pretty(self.transitions)}\n"
        output += f"\tE={''.join([str(e) for e in self.epsilon])}"
        return output

# # An NFA is represented by it's initial and accept states


class nfa:

    # 'self' represents current instance of the class - similar to 'this'
    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept
        accept.is_end = True

    def __str__(self) -> str:
        # return f"{self.initial} -{self.initial.pretty_transitions()}-> {self.accept} "
        return f"{self.initial} -> {self.accept}"

    def addstate(self, state, state_set):  # add state + recursively add epsilon transitions
        if state in state_set:
            return
        state_set.add(state)
        for eps in state.epsilon:
            self.addstate(eps, state_set)

    def match(self, s):
        current_states = set()
        self.addstate(self.accept, current_states)

        for c in s:
            next_states = set()
            for state in current_states:
                if c in state.transitions.keys():
                    trans_state = state.transitions[c]
                    self.addstate(trans_state, next_states)

            current_states = next_states

        for s in current_states:
            print(s)
            if s.is_end:
                return True
        return False


# takes postfix and compiles it
class Compiler():

    def __init__(self) -> None:
        self.states = 0

    def add_state(self) -> State:
        self.states += 1
        return State(f"q{self.states}")

    def concat(self, target, nfa_stack):
        # take the two topmost NFAs
        nf2 = nfa_stack.pop()
        nf1 = nfa_stack.pop()
        # make the first not end and set its final state to go to nf2
        nf1.accept.is_end = False
        nf1.accept.epsilon.append(nf2)
        # merge nf1 and nf2 via removing nf1.accept & nf2.initial
        newNFA = nfa(nf1.initial, nf2.accept)
        nfa_stack.append(newNFA)

    def char(self, target, nfa_stack):
        # create two new states
        s0 = self.add_state()
        s1 = self.add_state()
        # add a new transition based via character
        s0.transitions[target] = s1
        # finally, add it to the NFA stack
        newNFA = nfa(s0, s1)
        nfa_stack.append(newNFA)

    def compile(self, msg):
        nfa_stack = []
        for c in msg:
            if c == "?":
                self.concat(c, nfa_stack)
            else:
                self.char(c, nfa_stack)

        print("\n\n\n~~~")
        # print(nfa_stack[0].initial)
        # print(nfa_stack[0].accept)
        print(nfa_stack[0])

        return nfa_stack.pop()


""" compile() takes the postfix regex to NFA using Thompsons construct"""
