from .dfa import DFA


class NFA2DFA:
    def __init__(self, nfa):
        self.build_dfa(nfa)

    def build_dfa(self, nfa):
        '''
        Algorithm to get dfa from nfa.
        In detail:
            1. Get m-cast expression of original nfa.
            2. Construct the new state transition matrix thru e-closure.
            3. Rename the status.
        :param nfa:
        :return:
        '''
        nfa = self.get_m_cast(nfa)
        states = dict()
        start_e_closure = nfa.get_e_closure(1)
        cur_state = 0
        states[frozenset(start_e_closure)] = cur_state
        transitions = dict()
        q_acc_states = [[cur_state, start_e_closure]]
        cur_state += 1
        while len(q_acc_states):
            state_num, cur_closure = q_acc_states.pop()
            # if state_num == 16:
            for char in nfa.language:
                if char == nfa.epsilon():
                    continue
                acc_state = self.get_accepted_states(nfa, cur_closure, char)
                if len(acc_state) == 0:
                    continue
                if frozenset(acc_state) not in states:
                    states[frozenset(acc_state)] = cur_state
                    q_acc_states = [[cur_state, acc_state]] + q_acc_states
                    cur_state += 1
                if not state_num in transitions:
                    transitions[state_num] = dict()
                transitions[state_num][char] = states[frozenset(acc_state)]
        new_language = nfa.language
        new_language.discard(nfa.epsilon())
        original_final_state = nfa.final_states
        final_states = []
        final_dict = dict()
        for item in states:
            for original_item in original_final_state:
                if original_item in item:
                    final_states.append(states[item])

                    if states[item] not in final_dict:
                        final_dict[states[item]] = {nfa.label_dict[original_item]}
                    else:
                        if final_dict[states[item]] == 'identifier' or final_dict[states[item]] == 'number':
                            final_dict[states[item]] = {nfa.label_dict[original_item]}
        dfa = DFA(all_states=[_ for _ in range(cur_state)], input_alphabet=new_language, transitions=transitions,
                  initial_state=0, final_states=final_states, label_dict=final_dict)
        self.dfa = dfa
        # dfa.print_transition_matrix()
        # dfa.show_diagram('test.jpg')
        # print(transitions)

    def get_accepted_states(self, nfa, closure, char):
        reachable_states = set()

        # if char == nfa.epsilon():
        #     continue
        for item in closure:
            # accept a char
            if item in nfa.transitions:

                if char in nfa.transitions[item]:
                    # make each state accept this char.
                    # e_closure = set()
                    for target in nfa.transitions[item][char]:
                        reachable_states = nfa.get_e_closure(target).union(reachable_states)

        return reachable_states

    def get_m_cast(self, nfa):
        nfa, end = nfa.rebuild_from_number(2)
        init_state = 1
        end_state = end
        nfa.set_start_state(init_state)

        nfa.add_transition(init_state, 2, nfa.epsilon())
        # We got the NFA from standard construction, thus it contains only one final state.
        for item in nfa.final_states:
            nfa.add_transition(item, end_state, nfa.epsilon())
        # nfa.final_states = [end - 1]
        # nfa.final_states = [end_state]
        return nfa
