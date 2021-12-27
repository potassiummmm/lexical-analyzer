from regex2nfa import Regex2NFA
def test_nfa():
    nfa = Regex2NFA('l(l|d)*').nfa # type: nfa
    nfa.print_transition_matrix()
    nfa.show_diagram('res.jpg')