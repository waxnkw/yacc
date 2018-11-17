from YaccInput import *
from YaccFuncs import *
from YaccDataStructures import *
from YaccOutput import *


if __name__ == '__main__':
    import sys

    if len(sys.argv)<3:
        print("参数不完整")
        quit(0)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    ps, nts, ts = yac_input(input_path)
    Production.terminal_syms = ts
    Production.non_terminal_syms = nts
    firsts = calc_every_first_of_nt(ps, nts)
    states, lr1_table = construct_LR1_table(ps, firsts)
    yacc_output(lr1_table, output_path)