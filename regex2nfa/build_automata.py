from finite_automata.nfa import NFA
class BuildAutomata:
    @staticmethod
    def basicstruct(inp):
        '''
        Create a basic struct, which accepts a inp.
        :param inp:
        :return:
        '''

        state1 = 1
        state2 = 2
        basic = NFA({inp})
        basic.set_start_state(state1)
        basic.add_final_states([state2])
        if inp is None:
            return basic
        basic.add_transition(state1, state2, inp)
        return basic

    @staticmethod
    def starstruct(automata):
        '''
        Create a star struct (As shown in Thompson algorithm.)
        In detail:
            1. Expand the automata, making it start from second.
             (on default, the first state is from 1, we expect to
              add one state, thus making it start from 2)
            2. Create a new automata, add its init & final state.
            3. Link as what the graph shows.

        :param automata: Automata that needs to create * closure.
        :return: star automata.
        '''
        a, m1 = automata.rebuild_from_number(2) # type: NFA, int
        state1 = 1
        state2 = m1
        star = NFA(automata.language)
        star.set_start_state(state1)
        star.add_final_states([state2])
        star.add_transition(star.start_state, a.start_state, a.epsilon())
        star.add_transition(a.final_states[0], a.start_state, a.epsilon())
        star.add_transition(star.start_state, star.final_states[0], a.epsilon())
        star.add_transition(a.final_states[0], star.final_states[0], a.epsilon())
        star.add_transition_dict(a.transitions)
        return star

    @staticmethod
    def dotstruct(a: NFA, b: NFA):
        '''
        Create a dot struct (As shown in Thompson Algorithm).
        In Detail:
            1. Rearrange the number of a&b automata, making the last state of a to be the init state of b.
            2. Link the final of a to the init of b.
            3. Return
        :param a:
        :param b:
        :return: dotted automata
        '''
        a, m1 = a.rebuild_from_number(1)
        b, m2 = b.rebuild_from_number(m1)

        init_state = 1
        final_state = m2 - 1
        dot = NFA(a.language)
        dot.set_start_state(init_state)
        dot.add_final_states([final_state])
        dot.add_transition(a.final_states[0], b.start_state, a.epsilon())
        dot.add_transition_dict(a.transitions)
        dot.add_transition_dict(b.transitions)
        return dot

    @staticmethod
    def orstruct(a: NFA, b: NFA):
        '''
        Create an or struct (As shown in Thompson Algorithm):
        In Detail:
            1. Rearrange a start from 2, b start b from the last of a + 1.
            2. Add an initial state, who accepts epsilon to transit to start of a / b.
            3. Add a final state.
            4. Link the final state of a and b to the new final state.
            5. Return.
        :param a:
        :param b:
        :return:
        '''

        a, m1 = a.rebuild_from_number(2)
        b, m2 = b.rebuild_from_number(m1)
        init_state = 1
        final_state = m2
        oor = NFA(a.language)
        oor.set_start_state(init_state)
        oor.add_final_states([final_state])
        oor.add_transition(oor.start_state, 2, NFA.epsilon())
        oor.add_transition(oor.start_state, m1, NFA.epsilon())
        oor.add_transition(a.final_states[0], oor.final_states[0], NFA.epsilon())
        oor.add_transition(b.final_states[0], oor.final_states[0], NFA.epsilon())
        oor.add_transition_dict(a.transitions)
        oor.add_transition_dict(b.transitions)
        return oor