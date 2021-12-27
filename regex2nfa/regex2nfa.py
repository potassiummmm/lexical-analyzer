import finite_automata.nfa
from .build_automata import BuildAutomata


class Regex2NFA:
    def __init__(self, regex):
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
        self.stack = []  # character stack
        self.automata = []  # for synthesizing an overall automata
        self.build_nfa()

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
        """
        Adding an op to stack, and checking whether the bracket could be eliminated.
        :param op:
        :return:
        """
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

    def build_nfa(self):
        """
        Mid-exp to Post-exp, which is suitable for processing.
        :return:
        """
        language = set()
        previous = "::e::"
        for char in self.regex:
            if char in self.alphabet:
                language.add(char)  # a new accept language
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

        while len(self.stack):
            op = self.stack.pop()
            self.process_stack(op)

        self.nfa = self.automata[-1]
        self.nfa.language = language
