from YaccInput import *
from YaccFuncs import *
from YaccDataStructures import *
from YaccOutput import *


def test_input():
    p, nt, t = yac_input('./TestInput.txt')
    print(p)
    print(nt)
    print(t)


def test_calc_all_first():
    ps, nts, ts = yac_input('./TestInput.txt')
    Production.terminal_syms = ts
    Production.non_terminal_syms = nts
    firsts = calc_every_first_of_nt(ps, nts)
    print(firsts)


def test_construct_s0():
    ps, nts, ts = yac_input('./TestInput.txt')
    Production.terminal_syms = ts
    Production.non_terminal_syms = nts
    firsts = calc_every_first_of_nt(ps, nts)
    item = Item(ps[0], set(['$']), 0)
    s = State([item])
    s.expand(ps, firsts)
    print(s)


def construct_lr1_table():
    ps, nts, ts = yac_input('./TestInput1.txt')
    Production.terminal_syms = ts
    Production.non_terminal_syms = nts
    firsts = calc_every_first_of_nt(ps, nts)
    lr1_table = construct_LR1_table(ps, firsts)
    print(lr1_table)


def test_lalr():
    ps, nts, ts = yac_input('./TestInput1.txt')
    # print(ps)
    # print("Non terminal: " + str(nts))
    # print("Terminal: " + str(ts))
    Production.terminal_syms = ts
    Production.non_terminal_syms = nts
    firsts = calc_every_first_of_nt(ps, nts)
    # print(firsts)
    states, lr1_table = construct_LR1_table(ps, firsts)
    # print(states)
    # yacc_output(lr1_table, "./test1.py")


if __name__ == '__main__':
   # test_calc_all_first()
   #  test_construct_s0()
   #  construct_lr1_table()
    test_lalr()