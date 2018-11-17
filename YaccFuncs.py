from YaccDataStructures import *


def calc_every_first_of_nt(productions, nts):
    """
    计算每一个非终止符的first
    :param productions: 产生式集合
    :param nts: 非终止符集合
    :return: 所有非终止符first集合
    """
    firsts = {nt: [] for nt in nts}

    for nt in nts:
        is_changed = True
        first_of_nt = [prd for prd in productions if prd.left == nt]
        # new_first_of_nt = first_of_nt.copy()

        while is_changed:
            is_changed = False
            for first_prd in first_of_nt:
                left = first_prd.left
                right = first_prd.right

                # A->epsilon
                if len(right) == 0:
                    if None not in firsts[left]:
                        is_changed = True
                        firsts[left].append(None)
                # A->a
                elif first_prd.right_begin_with_terminal():
                    sym = right[0]
                    if sym not in firsts[left]:
                        is_changed = True
                        firsts[left].append(sym)
                # A->Bx
                else:
                    # B not contains epsilon
                    if None not in firsts[right[0]]:
                        for x in firsts[right[0]]:
                            if x not in firsts[left]:
                                is_changed = True
                                firsts[left].append(x)
                    # B contains epsilon
                    elif None in firsts[right[0]]:
                        for x in firsts[right[0]]:
                            if x not in firsts[left] and x is not None:
                                is_changed = True
                                firsts[left].append(x)
                        new_prd = Production(left, right[1:])
                        if new_prd not in first_of_nt:
                            first_of_nt.append(new_prd)
                            is_changed = True

                    for prd in productions:
                        if prd not in first_of_nt:
                            first_of_nt.append(prd)
                            is_changed = True
    return firsts


def construct_LR1_table(productions, firsts):
    states = []
    lr1_table = []

    # init s0
    item = Item(productions[0], set(['$']), 0)
    s0 = State([item])
    s0.expand(productions, firsts)
    states.append(s0)

    all_symbols = Production.non_terminal_syms + Production.terminal_syms

    cur_index = 0
    while cur_index < len(states):
        lr1_table.append({})
        cur_state = states[cur_index]

        for edge in all_symbols:
            new_state = cur_state.through_edge(edge)
            if new_state is not None:
                to_state = 0
                new_state.expand(productions, firsts)
                if new_state not in states:
                    to_state = len(states)
                    states.append(new_state)
                else:
                    to_state = states.index(new_state)
                lr1_table[cur_index][edge] = [to_state]

        reduction_items = cur_state.find_reduction_item()
        if len(reduction_items) > 0:
            for reduction_item in reduction_items:
                next_predict = reduction_item.next_predict
                for predict_symbol in next_predict:
                    if lr1_table[cur_index].get(predict_symbol, None) is None:
                        lr1_table[cur_index][predict_symbol] = []
                    if reduction_item.production == productions[0]:
                        lr1_table[cur_index][predict_symbol].append('acc')
                    else:
                        lr1_table[cur_index][predict_symbol].append(reduction_item.production.to_output())

        cur_index += 1

    return states, lr1_table

# def find_all_epsilon_nts(productions):
#     ret = [prd.left for prd in productions if prd.is_epsilon_production()]
#     last_len = -1
#     while last_len != len(ret):
#         last_len = len(ret)
#         for prd in productions:
#             # prd = Production(prd)
#             if prd.right is not None \
#                 and prd.composed_with(ret) \
#                 and prd.left not in ret:
#                 ret.append(prd.left)
#     return ret