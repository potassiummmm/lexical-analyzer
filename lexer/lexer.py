import nfa2dfa
import regex2nfa
from finite_automata import Token
import regex2nfa
from finite_automata import NFA
class Lexer:
    # TODO
    def read_input(self):
        pass

    def run(self):
        pass

    @staticmethod
    def construct_lexical_nfa():
        total_nfa = NFA(language=set(NFA.epsilon()))
        total_nfa.set_start_state(0)
        total_nfa.add_final_states([0], ' ')
        total_nfa.add_transition(0, 0, NFA.epsilon())
        cur_state = 1

        for i, key in enumerate(Token.reserved_word):
            nfa = regex2nfa.Regex2NFA(key, Token.reserved_word[key].value).nfa
            # nfa.label = key
            nfa, new_state = nfa.rebuild_from_number(cur_state)
            total_nfa.add_transition(0, cur_state, NFA.epsilon())
            total_nfa.add_transition_dict(nfa.transitions)
            total_nfa.add_final_states([new_state - 1], key)
            cur_state = new_state
            # break
            # if i == len(Token.reserved_word) - 2:
            #     break
        #

        # declare compositions
        alphabet = [chr(i) for i in range(65, 91)]
        alphabet += [chr(i) for i in range(97, 123)]
        # alphabet = ['V', 'A', 'R']
        digit = ['0', '1' , '2', '3', '4', '5', '6', '7', '8', '9']
        l = "(" + '|'.join(alphabet) + ")"
        d = "(" + '|'.join(digit) + ")"
        l_or_d = '' + l + '|' + d + ''
        var_alphabet = '(' + l_or_d  + ')*'


        # todo: nfa
        nfa = regex2nfa.Regex2NFA(var_alphabet).nfa
        nfa.label_dict[nfa.final_states[0]] = "identifier"

        tmp_dfa = nfa2dfa.NFA2DFA(total_nfa).dfa
        # tmp_dfa.show_diagram('test5.jpg')
        # nfa.print_transition_matrix()
        # nfa.show_diagram('test.jpg')
        # nfa.show_diagram('test.jpg')
        nfa, new_state = nfa.rebuild_from_number(cur_state)
        # print(total_nfa.label_dict)
        total_nfa.add_transition(0, cur_state, NFA.epsilon())
        total_nfa.add_transition_dict(nfa.transitions)
        total_nfa.add_final_states([new_state - 1], 'identifier')

        dfa = nfa2dfa.NFA2DFA(total_nfa).dfa
        # # print(dfa.final_states)
        print(dfa.label_dict)
        # dfa.show_diagram('output/total_dfa/res2.png')
        # # total_nfa.show_diagram('output/total_dfa/res.png')
