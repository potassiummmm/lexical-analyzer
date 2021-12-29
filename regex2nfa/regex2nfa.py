import finite_automata.nfa
from .build_automata import BuildAutomata


class Regex2NFA:
    def __init__(self, regex, type='K'):
        self.star = '*'
        self.dot = '.'
        self.oor = '|'
        self.openingBracket = '('
        self.closingBracket = ')'
        self.operators = [self.oor, self.dot]
        self.regex = regex
        self.alphabet = [chr(i) for i in range(65, 91)]
        self.alphabet += [chr(i) for i in range(97, 123)]
        self.alphabet += [chr(i) for i in range(48, 58)]
        self.stack = [] # character stack
        self.automata = [] # for synthesizing an overall automata
        self.automata_new = None

        self.build_nfa(type)


    def get_nfa(self):
        return self.nfa

    def process_stack(self, op):
        if op == self.star:
            a = self.automata.pop()
            self.automata.append(BuildAutomata.starstruct(a))
        elif op in self.operators:
            b = self.automata.pop()
            a = self.automata.pop()

            if op == self.dot:
                self.automata.append(BuildAutomata.dotstruct(a, b))
            elif op == self.oor:
                self.automata.append(BuildAutomata.orstruct(a, b))


    def add_operator_to_stack(self, op):
        '''
        Adding an op to stack, and checking whether the bracket could be eliminated.
        :param op:
        :return:
        '''
        while len(self.stack):
            # continuously process all binary elements.
            if self.stack[-1] == self.openingBracket:
                break
            if self.stack[-1] == op or self.stack[-1] == self.dot or self.stack[-1] == self.oor:
                to_process = self.stack.pop()
                self.process_stack(to_process)
            else:
                break
        self.stack.append(op)


    def build_nfa(self, type='K'):
        '''
        Mid-exp to Post-exp, which is suitable for processing.
        :return:
        '''
        language = set()

        previous = "::e::"
        for char in self.regex:
            if type == 'K':
                if char in self.alphabet:
                    language.add(char) # a new accept language
                    if previous in self.alphabet + [self.closingBracket] + [self.star]:
                        self.add_operator_to_stack(self.dot)
                    self.automata.append(BuildAutomata.basicstruct(char))
                elif char == self.openingBracket:
                    if previous in self.alphabet + [self.closingBracket] + [self.star]:
                        self.add_operator_to_stack(self.dot)
                    self.stack.append(char)
                elif char == self.closingBracket:
                    while 1:
                        op = self.stack.pop()
                        if op == self.openingBracket:
                            break
                        elif op in self.operators:
                            self.process_stack(op)
                elif char == self.star:
                    self.process_stack(char)

                elif char in self.operators:
                    self.add_operator_to_stack(char)
                previous = char
            else:
                if char in self.alphabet:
                    language.add(char)
                if self.automata_new is not None:
                    self.automata_new = BuildAutomata.dotstruct(self.automata_new, BuildAutomata.basicstruct(char))
                else:
                    self.automata_new = BuildAutomata.basicstruct(char)

        while len(self.stack):
            op = self.stack.pop()
            self.process_stack(op)
        if type == 'K':
            self.nfa = self.automata[-1]
        else:
            self.nfa = self.automata_new
        self.nfa.language = language