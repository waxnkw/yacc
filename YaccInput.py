from YaccDataStructures import *
from enum import Enum, unique

COLON = ':'
TERMINAL = 'terminal'+COLON
NON_TERMINAL = 'non_terminal'+COLON
PRODUCTION = 'production'+COLON


@unique
class InputState(Enum):
    T = 0
    N = 1
    P = 2


def yac_input(path):
    '''
    :param path:
    :return:
    '''
    productions = []
    nt_syms = []
    t_syms = []

    def get_type(word):
        if word in t_syms:
            return SymbolType.Terminal
        if word in nt_syms:
            return SymbolType.NonTerminal
        return SymbolType.Unknown

    cur_state = None
    with open(path, 'r') as f:
        for line in f.readlines():
            striped_line = line.strip()
            if striped_line == '':
                continue

            words = striped_line.split()
            if words[0] == TERMINAL:
                cur_state = InputState.T
            if words[0] == NON_TERMINAL:
                cur_state = InputState.N
            if words[0] == PRODUCTION:
                cur_state = InputState.P
                continue

            if cur_state == InputState.T:
                t_syms = [words[i] for i in range(1, len(words))]
            elif cur_state == InputState.N:
                nt_syms = [words[i] for i in range(1, len(words))]
            elif cur_state == InputState.P:
                left = words[0]
                left = left[0: -1]
                right = [words[i] for i in range(1, len(words))]
                # right = None if len(right) == 0 else right
                prd = Production(left, right)
                productions.append(prd)
    # productions.insert(0, )
    nt_syms.insert(0, "S'")
    productions.insert(0, Production("S'", [productions[0].left]))
    return productions, nt_syms, t_syms