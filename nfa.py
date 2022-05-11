
from asyncore import loop
from hashlib import new
from os import remove, stat
from tabnanny import check
from tkinter.messagebox import NO
from graphviz import Digraph
from color import ColorNFA

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
            self.transitions[c].append(state)
        else:
            self.transitions.setdefault(c, list()).append(state)
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
        self.vulnerable_states = []

    def reachable(self,to,fro):
        current_states = set()
        current_states.add(fro)
        old_states = current_states
        output_string = ""
        while True:
            next_state = set()
            transition_states = set()
            for c in self.language:
                for ns in current_states:    
                    # first check if transition is defined
                    if c in ns.transitions.keys():
                        
                        for ts in ns.transitions[c]:
                            transition_states.add(ts)
                            output_string += c
                    
                    # or if there is an epsilon reachable
                    for es in self.automata.epsilon_resolve(ns,c):
                        transition_states.add(es)
            
            # finally, addit the next state
            current_states = transition_states

            if any([s == to for s in current_states]):
                print(f"TEST OUTPUT PATH {output_string}")
                return True

            if old_states == next_state:
                return False
            else:
                old_states = next_state


                    
    

    def vulnerable(self):
        
        vulnerable = False
        loopbacked = {}
        # first, determine the ones with a loopback
        for k, v in self.state_table.items():
            # go through each character in language
            for c in self.language:
                # first check if transition is defined
                if c in v.transitions.keys():
                    # if loops back to self
                    if v in v.transitions[c]:
                        # OVERWRITE ANY OTHER LOOP BACKS LOL
                        loopbacked.update({v:c})                            

                    else:
                        for es in  self.automata.epsilon_resolve(v,c):
                            if v == es:
                                # loopbacked.add(v)
                                loopbacked.update({v:c})                            

        vuln = False
        for t,tv in loopbacked.items():
            for f,fv in loopbacked.items():
                if f != t:
                        
                    r = self.reachable(t,f)
                    if r:
                        vulnerable_string = f"{f.name}*...{t.name}*"
                        if t not in self.vulnerable_states:
                            self.vulnerable_states.append(t)
                        print(vulnerable_string)
                        vuln = True
                        # return True
        return vuln

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

    def draw_transition_table(self, fileName, format="png",color=ColorNFA,shrekmode=False):
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
                if shrekmode:
                    dot.node(k,k,shape='doublecircle',imagepath="..",image="../pics/shrek.svg",fontcolor="white")
                else:
                    dot.node(k,k,shape='doublecircle')
                # dot.node(k, k, shape='doublecircle',color=color.edge_color,fillcolor=color.fill_color,fontcolor=color.font_color)
            else:
                if shrekmode:
                    dot.node(k,k,shape='circle',imagepath="..",image="../pics/shrek.svg",fontcolor="white")
                else:
                    dot.node(k,k,shape='circle')
                
                # dot.node(k, k, shape='circle',color=color.edge_color,fontcolor=color.font_color)

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
                            dot.edge(k, ns.name, label="ε")
                        else:
                            dot.edge(k, ns.name, label=c)

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
        semi_match = False
        dangling_chars = []
        for c in self.regex:

            # kleene
            if c == "*":
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

            # add two chars
            elif c == ".":
                # pop
                nfa2 = nfa_stack.pop()
                nfa1 = nfa_stack.pop()

                nfa1.end.final_state = False
                nfa1.end.add_transition("", nfa2.begin)

                newNFA = NFA(nfa1.begin, nfa2.end)
                nfa_stack.append(newNFA)

            # OR
            elif c == "|":
                nfa2 = nfa_stack.pop()
                nfa1 = nfa_stack.pop()
                s0  = self.add_state()
                s1 = self.add_state()
                s0.add_transition("",nfa1.begin)
                s0.add_transition("",nfa2.begin)
                nfa2.end.add_transition("",s1)
                nfa1.end.add_transition("",s1)
                
                nfa1.end.final_state = False
                nfa2.end.final_state = False
                newNFA = NFA(s0,s1)
                nfa_stack.append(newNFA)


            # one or more
            elif c == "+":
                semi_match = False
                nfa1 =  nfa_stack.pop()
                s1  = self.add_state()

                nfa1.end.add_transition("",s1)
                nfa1.end.final_state = False
                s1.add_transition(pc,nfa1.end)
                newNFA = NFA(nfa1.begin,s1)
                nfa_stack.append(newNFA)

            elif c == "?":
                nfa1 = nfa_stack.pop()
                s0 = self.add_state()
                s1 = self.add_state()
                
                s0.add_transition("",s1)
                s0.add_transition("",nfa1.begin)
                nfa1.end.add_transition("",s1)
                nfa1.end.final_state = False
                newNFA = NFA(s0,s1)
                nfa_stack.append(newNFA)


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
