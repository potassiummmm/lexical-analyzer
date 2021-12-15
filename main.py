from finite_automata.dfa import DFA

if __name__ == '__main__':
    dfa = DFA(
        all_states={'0', '1', '2', '3', '4', '5', '6'},
        input_alphabet={'a', 'b'},
        transitions={
            '0': {'a': '1', 'b': '2'},
            '1': {'a': '3', 'b': '2'},
            '2': {'a': '1', 'b': '5'},
            '3': {'a': '3', 'b': '4'},
            '4': {'a': '6', 'b': '5'},
            '5': {'a': '6', 'b': '5'},
            '6': {'a': '3', 'b': '4'},
        },
        initial_state='0',
        final_states={'3', '4', '5', '6'}
    )
    dfa.print_transition_matrix()
    new_dfa = dfa.minimize()
    new_dfa.print_transition_matrix()
