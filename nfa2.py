
from os import remove, stat
from graphviz import Digraph

from ref.nfa import state

# individual states


class State():

    def __init__(self, name) -> None:
        self.name = name
        self.transitions = {}
        # self.epsilon = []
        self.final_state = False

    def add_transition(self, c, state):
        # adds the transition to the array of possible transitions
        if c in self.transitions:
            self.transitions[c].add(state)
        else:
            self.transitions.setdefault(c, set()).add(state)
            # self.transitions.update({c: []})
            # self.transitions[c].append(state)

    def __str__(self) -> str:
        output = f"[{self.name}]"

        # for k, v in self.transitions.items():
        #     for state in v:
        #         try:
        #             output += f"-{k}->{state}"
        #         except RecursionError:
        #             output += "INF"

        return output
        # return f"{self.name} -{}-> {self.transitions}"


# device to hold start and finished
class NFA():

    def __init__(self, begin, end):
        self.begin = begin
        self.end = end
        end.final_state = True

    def epsilon_resolve(self, state, c):
        if "" not in state.transitions:
            return []
        estates = set([e for e in state.transitions[""]])
        finished = False
        counter = 0
        resolve_to = []

        while not finished:
            counter += 1
            # capture what the epsilon states were previously
            old_set = estates
            next_estates = set()

            # go through all lambda transitions
            for estate in estates:
                # if the character we want add it to the transition table
                if c in estate.transitions.keys():
                    for ts in estate.transitions[c]:
                        resolve_to.append(ts)
                # otherwise add to the estate list for next iteration
                if any([k == "" for k in estate.transitions.keys()]):
                    for es in estate.transitions[""]:
                        next_estates.add(es)

            # check if the sets have changed
            estates = next_estates
            if estates == old_set:
                finished = True

        return resolve_to

    def match(self, msg):
        current_states = set()
        # add the head of the NFA
        current_states.add(self.begin)
        print(self.begin)

        # go through each character in message
        for c in msg:
            # blank out the next_states sets
            next_states = set()

            # iterate through all the states
            for state in current_states:

                # then add ones that match
                if c in state.transitions.keys():
                    # next_states = self.addstate_recursive(state,next_states)

                    # all transitions that include the character `c`
                    trans_state = state.transitions[c]
                    for ts in trans_state:
                        next_states.add(ts)

                # handle epsilon transitions
                if any([k == "" for k in state.transitions.keys()]):

                    # magic code to resolve epsilons (which are removed after construction)
                    for ts in self.epsilon_resolve(state, c):
                        next_states.add(ts)

            current_states = next_states

        finished = False
        next_states = current_states
        old_set = set()
        # we once again traverse the  transition from the current state to determine
        # whether there are lambda transitions leading us to the final state
        while not finished:
            old_set = current_states
            next_states = set()
            for s in current_states:
                # add lambda transitions
                if any([k == "" for k in s.transitions.keys()]):
                    # go through the lambda transitions
                    for es in s.transitions[""]:
                        # and add it to the next up
                        next_states.add(es)
                # or check if s is a final state and return
                if s.final_state:
                    return True

            current_states = next_states
            if current_states == old_set:
                break

        return False


class Compiler():

    def __init__(self, regex):
        self.regex = regex
        self.states = 1
        self.language = [""]
        self.state_table = {}
        self.final_states = []
        self.delta = {}  # transition table
        self.automata = self.compile()

    def add_state(self) -> State:
        self.states += 1
        newName = f"q{self.states}"
        newState = State(newName)
        self.state_table.update({newName: newState})

        return newState

    def transition_table(self):
        # HEADER
        header = "\t| " + "".join([f"{c}\t| " for c in self.language])
        header_sep = "-"*len(header)*3
        row = ""
        # go through the list of states
        for k, v in self.state_table.items():
            is_final = "+" if v.final_state else ""
            row += f"{is_final}{k}\t|"
            # go through each character in language
            for c in self.language:
                # if there exists `c` in the transition table of the state
                if c in v.transitions:
                    # add it to the table
                    resultant = "".join(
                        [f"+{t.name}," if t.final_state else f"{t.name}," for t in v.transitions[c]])
                    row += f"{resultant}\t| "
                else:
                    row += "\t| "
            row += "\n"
        print(f"{header}\n{header_sep}\n{row}")

    def draw_transition_table(self, fileName, format="png",color="white",font_color="black"):
        # HEADER
        # header = "\t| " + "".join([f"{c}\t| " for c in self.language])
        # header_sep = "-"*len(header)*3
        # row = ""
        # go through the list of states
        dot = Digraph(name=fileName, format=format )
        dot.graph_attr['rankdir'] = 'LR'

        # dot.node("", "", shape='plaintext')
        # dot.attr =

        # first draw each state
        for k, v in self.state_table.items():
            # print(type(k) == str)
            if v.final_state:
                dot.node(k, k, shape='doublecircle',color=color,fontcolor=font_color)
            else:
                dot.node(k, k, shape='circle',color=color,fontcolor=font_color)

        # then draw all edges
        for k, v in self.state_table.items():
            # row += f"{k}\t|"
            # go through each character in language
            for c in self.language:
                # if there exists `c` in the transition table of the state
                if c in v.transitions:
                    # goto next state from current state `k`
                    for ns in v.transitions[c]:
                        if c == "":
                            dot.edge(k, ns.name, label="ε",color=color,fontcolor=font_color)
                        else:
                            dot.edge(k, ns.name, label=c,color=color,fontcolor=font_color)

        dot.render()

    def flatten(self):
        # go through table
        to_delete = []

        for k, v in self.state_table.items():
            # iterate over language
            for c in self.language:
                # if there exists `c` in the transition table of the state
                if "" in v.transitions:
                    for estate in self.automata.epsilon_resolve(v, c):
                        # if estate.final_state:
                            # v.final_state = True
                        if v.final_state:
                            estate.final_state = True
                        
                        if c in v.transitions:
                            if estate not in v.transitions[c]:
                                v.add_transition(c, estate)
                        else:
                            v.add_transition(c, estate)


                        to_delete.append(v)

                    #
                    # goto next state from current state `k`
                    # for ns in v.transitions[c]:
        
        current_states = set()
        for k,v in self.state_table.items():
            finished = False
            current_states.add(v) 
            while not finished:
                old_set = current_states
                next_states = set()
                for s in current_states:
                    # add lambda transitions
                    if any([k == "" for k in s.transitions.keys()]):
                        # go through the lambda transitions
                        for es in s.transitions[""]:
                            # and add it to the next up
                            next_states.add(es)
                    # or check if s is a final state and return
                    if s.final_state:
                        if all([(l == "") for l in s.transitions.keys()]) or len(s.transitions.keys()) == 0:
                            v.final_state = True

                current_states = next_states
                if current_states == old_set:
                    finished = True

        

        removed = []
        for d in to_delete:
            if "" in d.transitions:

                for state in d.transitions[""]:
                    if state.name not in removed:
                        self.state_table.pop(state.name)
                        removed.append(state.name)
                d.transitions[""] = []

    def compile(self, DEBUG=True) -> NFA:

        nfa_stack = []

        # go through character by character
        for c in self.regex:

            # kleene
            if c == "*":
                """
                n1 = nfa_stack.pop()
                s0 = self.create_state()
                s1 = self.create_state()
                s0.epsilon = [n1.start]
                if t.name == 'STAR':
                    s0.epsilon.append(s1)
                n1.end.epsilon.extend([s1, n1.start])
                n1.end.is_end = False
                nfa = NFA(s0, s1)
                nfa_stack.append(nfa)
                """

                nfa1 = nfa_stack.pop()
                s0 = self.add_state()
                s1 = self.add_state()

                s0.add_transition("", nfa1.begin)
                s0.add_transition("", s1)
                nfa1.end.add_transition("", nfa1.begin)
                nfa1.end.add_transition("", s1)

                nfa1.end.final_state = False
                newNFA = NFA(s0, s1)
                nfa_stack.append(newNFA)

            # concat
            elif c == "?" or c == "\x08":
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

            # union
            elif c == "+":
                """
                n2 = nfa_stack.pop()
                n1 = nfa_stack.pop()
                s0 = self.create_state()
                s0.epsilon = [n1.start, n2.start]
                s3 = self.create_state()
                n1.end.epsilon.append(s3)
                n2.end.epsilon.append(s3)
                n1.end.is_end = False
                n2.end.is_end = False
                nfa = NFA(s0, s3)
                nfa_stack.append(nfa)
                """

                nfa2 = nfa_stack.pop()
                nfa1 = nfa_stack.pop()
                s0 = self.add_state()
                s0.add_transition("", nfa1.begin)
                s0.add_transition("", nfa2.begin)
                s1 = self.add_state()
                nfa2.end.add_transition("", s1)
                nfa1.end.add_transition("", s1)
                nfa1.end.final_state = False
                nfa2.end.final_state = False
                # s1.final_state = True
                newNFA = NFA(s0, s1)
                nfa_stack.append(newNFA)

            # elif c == "\0x08":
            #     s0 = self.add_state()
            #     s1 = self.add_state()

            #     s0.add_transition(c, s1)
            #     # push onto stack
            #     newNFA = NFA(s0, s1)
            #     nfa_stack.append(newNFA)

            else:

                # add c into language if not already there (uses set so magic)
                if c not in self.language:
                    self.language.append(c)

                s0 = self.add_state()
                s1 = self.add_state()

                s0.add_transition(c, s1)
                # push onto stack
                newNFA = NFA(s0, s1)
                nfa_stack.append(newNFA)

            pc = c  # is the previous char

        assert len(nfa_stack) == 1
        return nfa_stack[-1]
