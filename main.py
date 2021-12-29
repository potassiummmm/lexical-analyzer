from finite_automata.dfa import DFA
from regex2nfa.build_automata import BuildAutomata
from regex2nfa import Regex2NFA
from test import test_nfa2dfa, test_lexer
if __name__ == '__main__':
    # test_nfa2dfa.test_nfa()
    test_lexer.lexer_test()
    # dfa = DFA(
    #     all_states={'0', '1', '2', '3', '4', '5', '6'},
    #     input_alphabet={'a', 'b'},
    #     transitions={
    #         '0': {'a': '1', 'b': '2'},
    #         '1': {'a': '3', 'b': '2'},
    #         '2': {'a': '1', 'b': '5'},
    #         '3': {'a': '3', 'b': '4'},
    #         '4': {'a': '6', 'b': '5'},
    #         '5': {'a': '6', 'b': '5'},
    #         '6': {'a': '3', 'b': '5'},
    #     },
    #     initial_state='0',
    #     final_states={'3', '4', '5', '6'}
    # )
    # # .print_transition_matrix()
    # dfa.show_diagram(path='output/DFA/before_minimization.png')
    # new_dfa = dfa.minimize()
    # new_dfa.show_diagram(path='output/DFA/after_minimization.png')
    # dfa.print_transition_matrix()
