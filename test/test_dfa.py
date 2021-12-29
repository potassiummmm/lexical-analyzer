from finite_automata.dfa import DFA


def test_min_dfa_1():
    dfa = DFA(
        all_states={0, 1, 2, 3, 4, 5, 6},
        input_alphabet={'a', 'b'},
        transitions={
            0: {'a': 1, 'b': 2},
            1: {'a': 3, 'b': 2},
            2: {'a': 1, 'b': 5},
            3: {'a': 3, 'b': 4},
            4: {'a': 6, 'b': 5},
            5: {'a': 6, 'b': 5},
            6: {'a': 3, 'b': 4},
        },
        initial_state=0,
        final_states={3, 4, 5, 6},
        label_dict={}
    )
    dfa.print_transition_matrix()
    dfa.show_diagram('../output/DFA/test1_before.png')
    min_dfa = dfa.minimize()
    min_dfa.print_transition_matrix()
    min_dfa.show_diagram('../output/DFA/test1_after.png')
    assert min_dfa.transitions == {
            0: {'a': 2, 'b': 1},
            1: {'a': 2, 'b': 3},
            2: {'a': 3, 'b': 1},
            3: {'a': 3, 'b': 3},
        } or min_dfa.transitions == {
            0: {'a': 1, 'b': 2},
            1: {'a': 3, 'b': 2},
            2: {'a': 1, 'b': 3},
            3: {'a': 3, 'b': 3},
        }


def test_min_dfa_2():
    dfa = DFA(
        all_states={0, 1, 2, 3, 4, 5},
        input_alphabet={'a', 'b'},
        transitions={
            0: {'a': 1, 'b': 3},
            1: {'a': 0, 'b': 3},
            2: {'a': 1, 'b': 4},
            3: {'a': 5, 'b': 5},
            4: {'a': 3, 'b': 3},
            5: {'a': 5, 'b': 5},
        },
        initial_state=0,
        final_states={3, 5},
        label_dict={}
    )
    dfa.print_transition_matrix()
    dfa.show_diagram('../output/DFA/test2_before.png')
    min_dfa = dfa.minimize()
    min_dfa.print_transition_matrix()
    min_dfa.show_diagram('../output/DFA/test2_after.png')
    assert min_dfa.transitions == {
            0: {'a': 1, 'b': 2},
            1: {'a': 0, 'b': 2},
            2: {'a': 2, 'b': 2},
        }


def test_min_dfa_3():
    dfa = DFA(
        all_states={'A', 'B', 'C', 'D'},
        input_alphabet={'l', 'd'},
        transitions={
            'A': {'l': 'B'},
            'B': {'l': 'C', 'd': 'D'},
            'C': {'l': 'C', 'd': 'D'},
            'D': {'l': 'C', 'd': 'D'},
        },
        initial_state='A',
        final_states={'B', 'C', 'D'},
        label_dict={}
    )
    dfa.print_transition_matrix()
    dfa.show_diagram('../output/DFA/test3_before.png')
    min_dfa = dfa.minimize()
    min_dfa.print_transition_matrix()
    min_dfa.show_diagram('../output/DFA/test3_after.png')
    assert 1
    # assert min_dfa.transitions == {
    #         0: {'a': 2, 'b': 1},
    #         1: {'a': 2, 'b': 3},
    #         2: {'a': 3, 'b': 1},
    #         3: {'a': 3, 'b': 3},
    #     } or min_dfa.transitions == {
    #         0: {'a': 1, 'b': 2},
    #         1: {'a': 3, 'b': 2},
    #         2: {'a': 1, 'b': 3},
    #         3: {'a': 3, 'b': 3},
    #     }
