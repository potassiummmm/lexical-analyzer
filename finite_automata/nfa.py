import prettytable as pt
from pydot import Dot, Edge, Node
# from finite_automata.fa import *
class NFA:
    def __init__(self, language: set):
        self.states = set()
        self.start_state = None
        self.final_states = []
        self.transitions = dict()
        self.language = language

    @staticmethod
    def epsilon():
        return 'ε'

    def set_start_state(self, state):
        self.start_state = state
        self.states.add(state)

    def add_final_states(self, states):
        for state in states:
            if state not in self.final_states:
                self.final_states.append(state)

    def add_transition(self, start, end, inp):
        '''
        This function adds the transition from start to end and accepts p
        :param start:
        :param end:
        :param inp:
        :return:
        '''
        self.language.add(inp)
        self.states.add(start)
        self.states.add(end)
        if start in self.transitions:
            if inp in self.transitions[start]:
                self.transitions[start][inp].add(end)
            else:
                self.transitions[start][inp] = {end}

        else:
            self.transitions[start] = {inp : {end}}

    def rebuild_from_number(self, start_num):
        translations = {}
        for item in list(self.states):
            translations[item] = start_num
            start_num += 1
        rebuild = NFA(self.language)
        rebuild.set_start_state(translations[self.start_state])
        rebuild.add_final_states([translations[self.final_states[0]]])
        # print(self.transitions)
        for start, trans in self.transitions.items():
            for tran in trans:
                for item in trans[tran]:
                    rebuild.add_transition(translations[start], translations[item], tran)

        return rebuild, start_num

    def add_transition_dict(self, transitions):
        for start, trans in transitions.items():
            for tran in trans:
                for item in trans[tran]:
                    self.add_transition(start, item, tran)

    def print_transition_matrix(self):
        table = pt.PrettyTable()
        states = list(self.states)
        inputs = list(self.language)
        inputs += [self.epsilon()]
        states.sort()
        inputs.sort()
        table.field_names = ["State"] + [char for char in inputs]
        for state in states:
            if state not in self.transitions:
                table.add_row([state] + [None] * len(inputs))
                continue
            transition_row = []
            for input_char in inputs:
                if input_char in self.transitions[state]:
                    transition_row.append(self.transitions[state][input_char])
                else:
                    transition_row.append(None)
            table.add_row([state] + transition_row)
        print(table)

    def show_diagram(self, path):
        """
        Creates the graph associated with this DFA
        :param path: path to save the image file
        """
        graph = Dot(graph_type='digraph', rankdir='LR')
        nodes = {}
        for state in self.states:
            if state == self.start_state:
                if state in self.final_states:
                    initial_state_node = Node(
                        state,
                        peripheries=2)
                else:
                    initial_state_node = Node(
                        state)
                nodes[state] = initial_state_node
                graph.add_node(initial_state_node)
            else:
                if state in self.final_states:
                    state_node = Node(state, peripheries=2)
                else:
                    state_node = Node(state)
                nodes[state] = state_node
                graph.add_node(state_node)
        # Add edges
        for from_state, lookup in self.transitions.items():
            for to_label, to_state_set in lookup.items():
                for to_state in to_state_set:
                    graph.add_edge(Edge(
                        nodes[from_state],
                        nodes[to_state],
                        label=to_label
                    ))
        graph.write(path, format='png')
