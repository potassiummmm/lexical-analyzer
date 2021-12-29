from finite_automata.regex2nfa import Regex2NFA
from finite_automata.nfa2dfa import NFA2DFA


def test_nfa2dfa():
    nfa = Regex2NFA('l(l|d)*').nfa  # type: nfa
    nfa.label_dict[nfa.final_states[0]] = "V"
    nfa.print_transition_matrix()
    nfa.show_diagram('../output/NFA2DFA/nfa.png')
    dfa = NFA2DFA(nfa).dfa
    dfa.print_transition_matrix()
    dfa.show_diagram('../output/NFA2DFA/dfa.png')
    assert dfa.transitions == {
        0: {'l': 1},
        1: {'l': 3, 'd': 2},
        2: {'l': 3, 'd': 2},
        3: {'l': 3, 'd': 2},
    } or dfa.transitions == {
        0: {'l': 1},
        1: {'l': 2, 'd': 3},
        2: {'l': 2, 'd': 3},
        3: {'l': 2, 'd': 3},
    }
