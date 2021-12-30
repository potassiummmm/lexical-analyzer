from finite_automata.nfa2dfa import NFA2DFA
from finite_automata.token import Token
from finite_automata.regex2nfa import Regex2NFA
from finite_automata.nfa import NFA
import copy


class Lexer:
    def __init__(self):
        self.nfa = None
        self.dfa = None

    def read_input(self):
        pass

    def run(self, mode='test', output_mode=None):
        """
        Run lexer
        :param mode: construct lexer with test/pl0/custom rules
        :param output_mode: graph/table/all
        """
        if mode == 'test':
            self._run_test(output_mode)
        elif mode == 'pl0':
            self._run_pl0(output_mode)
        elif mode == 'custom':
            self._run_custom(output_mode)

    def _run_custom(self, output_mode):
        token_dict = {}
        while True:
            input_line = input('Input token id and regex, split by space, press enter to end input:')
            if input_line == '' or len(input_line.split(' ')) != 2:
                break
            token_dict[input_line.split(' ')[1]] = input_line.split(' ')[0]
        self.construct_custom_nfa(token_dict)
        if output_mode == 'all':
            self.nfa.print_transition_matrix()
            self.dfa.print_transition_matrix()
            self.nfa.show_diagram('output/LEX/custom_nfa.png')
            self.dfa.show_diagram('output/LEX/custom_dfa.png')
        elif output_mode == 'graph':
            self.nfa.show_diagram('output/LEX/custom_nfa.png')
            self.dfa.show_diagram('output/LEX/custom_dfa.png')
        elif output_mode == 'table':
            self.nfa.print_transition_matrix()
            self.dfa.print_transition_matrix()
        while True:
            input_str = input('Input string, press enter to quit:')
            if input_str == '':
                break
            self.dfa.accept_input(input_str)

    def _run_test(self, output_mode):
        self.construct_test_nfa()
        if output_mode == 'all':
            self.nfa.print_transition_matrix()
            self.dfa.print_transition_matrix()
            self.nfa.show_diagram('output/LEX/test_nfa.png')
            self.dfa.show_diagram('output/LEX/test_dfa.png')
        elif output_mode == 'graph':
            self.nfa.show_diagram('output/LEX/test_nfa.png')
            self.dfa.show_diagram('output/LEX/test_dfa.png')
        elif output_mode == 'table':
            self.nfa.print_transition_matrix()
            self.dfa.print_transition_matrix()
        while True:
            input_str = input('Input string, press enter to quit:')
            if input_str == '':
                break
            self.dfa.accept_input(input_str)

    def _run_pl0(self, output_mode):
        self.construct_pl0_nfa()
        if output_mode == 'all':
            self.nfa.print_transition_matrix()
            self.dfa.print_transition_matrix()
            self.nfa.show_diagram('output/LEX/pl0_nfa.png')
            self.dfa.show_diagram('output/LEX/pl0_dfa.png')
        elif output_mode == 'graph':
            self.nfa.show_diagram('output/LEX/pl0_nfa.png')
            self.dfa.show_diagram('output/LEX/pl0_dfa.png')
        elif output_mode == 'table':
            self.nfa.print_transition_matrix()
            self.dfa.print_transition_matrix()
        while True:
            input_str = input('Input string, press enter to quit:')
            if input_str == '':
                break
            self.dfa.accept_input(input_str)

    def construct_test_nfa(self):
        self.nfa = NFA(language=set(NFA.epsilon()))
        self.nfa.set_start_state(0)
        self.nfa.add_final_states([0], ' ')
        self.nfa.add_transition(0, 0, NFA.epsilon())
        cur_state = 1

        test_token = {'VAR': 'K', ',': 'D', ';': 'D'}

        for regex, id in test_token.items():
            nfa = Regex2NFA(regex, id).nfa
            nfa, new_state = nfa.rebuild_from_number(cur_state)
            self.nfa.add_transition(0, cur_state, NFA.epsilon())
            self.nfa.add_transition_dict(nfa.transitions)
            self.nfa.add_final_states([new_state - 1], id)
            cur_state = new_state

        # declare compositions
        alphabet = [chr(i) for i in range(65, 91)]
        alphabet += [chr(i) for i in range(97, 123)]
        digit = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        l = "(" + '|'.join(alphabet) + ")"
        d = "(" + '|'.join(digit) + ")"
        l_or_d = l + '|' + d
        var_alphabet = l + '(' + l_or_d + ')*'
        var_num = d + d + '*'
        fake_total_nfa = copy.deepcopy(self.nfa)
        nfa = Regex2NFA(var_alphabet).nfa
        nfa.label_dict[nfa.final_states[0]] = "V"
        nfa, new_state = nfa.rebuild_from_number(cur_state)
        self.nfa.add_transition(0, cur_state, NFA.epsilon())
        self.nfa.add_transition_dict(nfa.transitions)
        self.nfa.add_final_states([new_state - 1], 'V')

        self.dfa = NFA2DFA(self.nfa).dfa
        # print(self.dfa.label_dict)

        # Fake part
        fake_nfa = Regex2NFA('l(l|d)*').nfa
        fake_nfa.label_dict[fake_nfa.final_states[0]] = 'V'
        fake_nfa, new_state = fake_nfa.rebuild_from_number(cur_state)
        fake_total_nfa.add_transition(0, cur_state, NFA.epsilon())
        fake_total_nfa.add_final_states([new_state - 1], 'V')
        fake_total_nfa.add_transition_dict(fake_nfa.transitions)
        fake_total_nfa.show_diagram('output/LEX/test_nfa.png')



    def construct_pl0_nfa(self):
        self.nfa = NFA(language=set(NFA.epsilon()))
        self.nfa.set_start_state(0)
        self.nfa.add_final_states([0], ' ')
        self.nfa.add_transition(0, 0, NFA.epsilon())
        cur_state = 1

        for i, key in enumerate(Token.reserved_word):
            nfa = Regex2NFA(key, Token.reserved_word[key].value).nfa
            # nfa.label = key
            nfa, new_state = nfa.rebuild_from_number(cur_state)
            self.nfa.add_transition(0, cur_state, NFA.epsilon())
            self.nfa.add_transition_dict(nfa.transitions)
            self.nfa.add_final_states([new_state - 1], key)
            cur_state = new_state

        # declare compositions
        alphabet = [chr(i) for i in range(65, 91)]
        alphabet += [chr(i) for i in range(97, 123)]
        digit = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        l = "(" + '|'.join(alphabet) + ")"
        d = "(" + '|'.join(digit) + ")"
        l_or_d = l + '|' + d
        var_alphabet = l + '(' + l_or_d + ')*'
        var_num = d + d + '*'
        fake_total_nfa = copy.deepcopy(self.nfa)
        nfa = Regex2NFA(var_alphabet).nfa
        nfa.label_dict[nfa.final_states[0]] = "identifier"
        nfa, new_state = nfa.rebuild_from_number(cur_state)
        self.nfa.add_transition(0, cur_state, NFA.epsilon())
        self.nfa.add_transition_dict(nfa.transitions)
        self.nfa.add_final_states([new_state - 1], 'identifier')

        cur_state = new_state
        num_nfa = Regex2NFA(var_num).nfa
        num_nfa.label_dict[num_nfa.final_states[0]] = "number"
        num_nfa, new_state = num_nfa.rebuild_from_number(cur_state)
        self.nfa.add_transition(0, cur_state, NFA.epsilon())
        self.nfa.add_transition_dict(num_nfa.transitions)
        self.nfa.add_final_states([new_state - 1], 'number')

        self.dfa = NFA2DFA(self.nfa).dfa
        # print(self.dfa.label_dict)

        # Fake part
        fake_nfa = Regex2NFA('l(l|d)*').nfa
        fake_nfa.label_dict[fake_nfa.final_states[0]] = "identifier"
        fake_nfa, new_state = fake_nfa.rebuild_from_number(cur_state)
        fake_total_nfa.add_transition(0, cur_state, NFA.epsilon())
        fake_total_nfa.add_final_states([new_state - 1], 'identifier')
        fake_total_nfa.add_transition_dict(fake_nfa.transitions)
        cur_state = new_state
        fake_nfa = Regex2NFA('dd*').nfa
        fake_nfa.label_dict[fake_nfa.final_states[0]] = "number"
        fake_nfa, new_state = fake_nfa.rebuild_from_number(cur_state)
        fake_total_nfa.add_transition(0, cur_state, NFA.epsilon())
        fake_total_nfa.add_final_states([new_state - 1], 'number')
        fake_total_nfa.add_transition_dict(fake_nfa.transitions)
        fake_total_nfa.show_diagram('output/LEX/pl0_nfa.png')

    def construct_custom_nfa(self, token_dict):
        self.nfa = NFA(language=set(NFA.epsilon()))
        self.nfa.set_start_state(0)
        self.nfa.add_final_states([0], ' ')
        self.nfa.add_transition(0, 0, NFA.epsilon())
        cur_state = 1

        for regex, id in token_dict.items():
            nfa = Regex2NFA(regex, id).nfa
            nfa, new_state = nfa.rebuild_from_number(cur_state)
            self.nfa.add_transition(0, cur_state, NFA.epsilon())
            self.nfa.add_transition_dict(nfa.transitions)
            self.nfa.add_final_states([new_state - 1], id)
            cur_state = new_state

        self.dfa = NFA2DFA(self.nfa).dfa
