from finite_automata import DFA


class NFA2DFA:
    def __init__(self, nfa):
        self.dfa = None
        self.build_nfa(nfa)

    def build_nfa(self, nfa):
        """
        Algorithm to get dfa from nfa.
        In detail:
            1. Get m-cast expression of original nfa.
            2. Construct the new state transition matrix thru e-closure.
            3. Rename the status.
        :param nfa:
        :return:
        """
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
                if state_num not in transitions:
                    transitions[state_num] = dict()
                transitions[state_num][char] = states[frozenset(acc_state)]
        new_language = nfa.language
        new_language.discard(nfa.epsilon())
        original_final_state = nfa.final_states[0]
        final_states = []
        for item in states:
            if original_final_state in item:
                final_states.append(states[item])

        dfa = DFA(all_states=[_ for _ in range(cur_state)], input_alphabet=new_language, transitions=transitions,
                  initial_state=0, final_states=final_states)
        self.dfa = dfa
        # dfa.print_transition_matrix()
        # dfa.show_diagram('test.jpg')
        # print(transitions)

    @staticmethod
    def get_accepted_states(nfa, closure, char):
        reachable_states = set()

        # if char == nfa.epsilon():
        #     continue
        for item in closure:
            # accept a char
            if item in nfa.transitions:

                if char in nfa.transitions[item]:
                    # make each state accept this char.
                    e_closure = set()
                    for target in nfa.transitions[item][char]:
                        e_closure = nfa.get_e_closure(target).union(e_closure)
                    if char not in reachable_states:
                        reachable_states = e_closure  # type:set
                    else:
                        reachable_states.union(e_closure)
        return reachable_states

    @staticmethod
    def get_m_cast(nfa):
        nfa, end = nfa.rebuild_from_number(2)
        init_state = 1
        end_state = end
        nfa.set_start_state(init_state)

        nfa.add_transition(init_state, 2, nfa.epsilon())
        # We got the NFA from standard construction, thus it contains only one final state.
        nfa.add_transition(nfa.final_states[0], end_state, nfa.epsilon())
        nfa.final_states = [end_state]
        return nfa
