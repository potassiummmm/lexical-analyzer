import nfa2dfa
import regex2nfa
from finite_automata import Token
import regex2nfa
from finite_automata import NFA
import copy
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
        l_or_d =  l + '|' + d
        var_alphabet = l + '(' + l_or_d  + ')*'
        var_num = d + d + '*'
        fake_total_nfa = copy.deepcopy(total_nfa)
        # Real part
        nfa = regex2nfa.Regex2NFA(var_alphabet).nfa
        nfa.label_dict[nfa.final_states[0]] = "identifier"
        nfa, new_state = nfa.rebuild_from_number(cur_state)
        total_nfa.add_transition(0, cur_state, NFA.epsilon())
        total_nfa.add_transition_dict(nfa.transitions)
        total_nfa.add_final_states([new_state - 1], 'identifier')

        cur_state = new_state
        num_nfa = regex2nfa.Regex2NFA(var_num).nfa
        num_nfa.label_dict[num_nfa.final_states[0]] = "number"
        num_nfa, new_state = num_nfa.rebuild_from_number(cur_state)
        total_nfa.add_transition(0, cur_state, NFA.epsilon())
        total_nfa.add_transition_dict(num_nfa.transitions)
        total_nfa.add_final_states([new_state - 1], 'number')

        dfa = nfa2dfa.NFA2DFA(total_nfa).dfa
        print(dfa.label_dict)


        # Fake part
        fake_nfa = regex2nfa.Regex2NFA('l(l|d)*').nfa
        fake_nfa.label_dict[fake_nfa.final_states[0]] = "identifier"
        fake_nfa, new_state = fake_nfa.rebuild_from_number(cur_state)
        fake_total_nfa.add_transition(0, cur_state, NFA.epsilon())
        fake_total_nfa.add_final_states([new_state - 1], 'identifier')
        fake_total_nfa.add_transition_dict(fake_nfa.transitions)
        cur_state = new_state
        fake_nfa = regex2nfa.Regex2NFA('dd*').nfa
        fake_nfa.label_dict[fake_nfa.final_states[0]] = "number"
        fake_nfa, new_state = fake_nfa.rebuild_from_number(cur_state)
        fake_total_nfa.add_transition(0, cur_state, NFA.epsilon())
        fake_total_nfa.add_final_states([new_state - 1], 'number')
        fake_total_nfa.add_transition_dict(fake_nfa.transitions)
        fake_total_nfa.show_diagram('test.jpg')