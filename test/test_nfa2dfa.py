from regex2nfa import Regex2NFA
from nfa2dfa import NFA2DFA
def test_nfa():
    nfa = Regex2NFA('l(l|d)*').nfa # type: nfa
    dfa = NFA2DFA(nfa).dfa
    dfa.show_diagram('output/nfa2dfa/res.jpg')
    # nfa.print_transition_matrix()
    # nfa.show_diagram('res.jpg')
