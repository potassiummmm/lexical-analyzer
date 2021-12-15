from .fa import FA


class NFA(FA):
    def __init__(self, *, all_states, input_alphabet, transitions,
                 initial_state, final_states):
        super().__init__(all_states=all_states, input_alphabet=input_alphabet, transitions=transitions,
                         initial_state=initial_state, final_states=final_states)
