from abc import ABC
import prettytable as pt
import copy


class FA(ABC):
    def __init__(self, *, all_states, input_alphabet, transitions,
                 initial_state, final_states):
        self.all_states = all_states.copy()
        self.input_alphabet = input_alphabet.copy()
        self.transitions = copy.deepcopy(transitions)
        self.initial_state = initial_state
        self.final_states = final_states.copy()

    def copy(self):
        return copy.deepcopy(self)

    def print_transition_matrix(self):
        table = pt.PrettyTable()
        states = list(self.all_states)
        inputs = list(self.input_alphabet)
        states.sort()
        inputs.sort()
        table.field_names = ["State"] + [char for char in inputs]
        for state in states:
            table.add_row([state] + [self.transitions[state][input_char] for input_char in inputs])
        print(table)
