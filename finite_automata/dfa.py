from collections import deque
from .fa import FA
from pydot import Dot, Edge, Node
from lexer.token import Token


class DFA(FA):
    def __init__(self, *, all_states, input_alphabet, transitions,
                 initial_state, final_states, label_dict):
        super().__init__(all_states=all_states, input_alphabet=input_alphabet, transitions=transitions,
                         initial_state=initial_state, final_states=final_states)
        self.label_dict = label_dict

    def remove_unreachable_states(self):
        reachable_states = self.get_reachable_states()
        unreachable_states = self.all_states - reachable_states
        for state in unreachable_states:
            self.all_states.remove(state)
            del self.transitions[state]
            if state in self.final_states:
                self.final_states.remove(state)

    def get_reachable_states(self):
        """
        Use BFS to search all reachable states
        :return: A set of states that are reachable
        """
        reachable_states = set()
        state_queue = deque()
        state_queue.append(self.initial_state)
        reachable_states.add(self.initial_state)
        while state_queue:
            state = state_queue.popleft()
            for symbol, dst_state in self.transitions[state].items():
                if dst_state not in reachable_states:
                    reachable_states.add(dst_state)
                    state_queue.append(dst_state)
        return reachable_states

    def merge_states(self):
        """
        Merge states into equivalent sets
        """

        # Initial division
        groups = []
        if len(self.final_states) != 0:
            groups.append(frozenset(self.final_states))
        if len(self.final_states) != len(self.all_states):
            groups.append(
                frozenset(set(self.all_states).difference(self.final_states))
            )
        groups = set(groups)

        # Use a queue-like structure to process
        groups_copy = set(groups)

        while len(groups_copy) > 0:
            cur_states = groups_copy.pop()
            if len(cur_states) == 1:
                continue
            for input_char in self.input_alphabet:
                next_states = frozenset(self.transitions[state][input_char] for state in cur_states)
                if not next_states.issubset(cur_states):
                    # Try each character to prevent an infinite loop
                    for split_char in self.input_alphabet:
                        next_states = frozenset(self.transitions[state][split_char] for state in cur_states)
                        split_results = []
                        for next_state in next_states:
                            split_results.append(set(state for state in cur_states
                                                     if self.transitions[state][split_char] == next_state))
                        if len(split_results) > 1:
                            groups.remove(frozenset(cur_states))
                            for result in split_results:
                                groups.add(frozenset(result))
                                groups_copy.add(frozenset(result))
                            break
                    break

        # Maintain relative order of the states: initial, ... , final
        groups = list(groups)
        groups.sort(
            key=lambda x: 1 if self.initial_state in x else -1 if len(self.final_states.intersection(x)) > 0 else 0,
            reverse=True)

        # Index mapping
        state_index = {}
        for i, equal_states in enumerate(groups):
            for state in equal_states:
                state_index[state] = str(i)

        # Generate new state number
        new_states = (set(str(i) for i in range(len(groups))))
        new_initial_state = state_index[self.initial_state]
        new_final_states = set([state_index[final_state] for final_state in self.final_states])
        new_transitions = {}
        for i, equal_states in enumerate(groups):
            name = str(i)
            new_transitions[name] = {}
            for input_char in self.input_alphabet:
                new_transitions[name][input_char] = state_index[
                    self.transitions[list(equal_states)[0]][input_char]
                ]

        # Update
        self.all_states = new_states
        self.transitions = new_transitions
        self.initial_state = new_initial_state
        self.final_states = new_final_states

    def minimize(self):
        """
        Minimize dfa using the Equivalence Theorem, return a copy of minimized dfa without modifying current one.
        :return: A copy of minimized dfa
        """
        new_dfa = self.copy()
        new_dfa.remove_unreachable_states()
        new_dfa.merge_states()
        return new_dfa

    def accept_input(self, input_str: str):
        input_list = input_str.split(' ')
        cur_state = self.initial_state
        for string in input_list:
            accepted = ''
            for input_char in string:
                if input_char in self.transitions[cur_state]:
                    accepted += input_char
                    cur_state = self.transitions[cur_state][input_char]
                else:
                    if cur_state in self.final_states:
                        Token.print_token(accepted)
                        if input_char in self.transitions[self.initial_state]:
                            accepted = input_char
                        else:
                            print('error')
                            return
                    else:
                        print('error')
                        return
            Token.print_token(string)

    def show_diagram(self, path):
        """
        Creates the graph associated with this DFA
        :param path: path to save the image file
        """
        graph = Dot(graph_type='digraph', rankdir='LR')
        nodes = {}
        for state in self.all_states:
            if state == self.initial_state:
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
                    if self.label_dict != dict():
                        state_node = Node(str(state) + ', ' + '_'.join(list(self.label_dict[state])), peripheries=2)
                    else:
                        state_node = Node(str(state) , peripheries=2)
                else:
                    state_node = Node(state)
                nodes[state] = state_node
                graph.add_node(state_node)
        # Add edges
        for from_state, lookup in self.transitions.items():
            for to_label, to_state in lookup.items():
                if to_label != ',':
                    graph.add_edge(Edge(
                        nodes[from_state],
                        nodes[to_state],
                        label=to_label
                    ))
                else:
                    graph.add_edge(Edge(
                        nodes[from_state],
                        nodes[to_state],
                        label='，'
                    ))
        graph.write(path, format='png')
