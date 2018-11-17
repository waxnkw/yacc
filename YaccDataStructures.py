from enum import Enum, unique


@unique
class SymbolType(Enum):
    NonTerminal = 0
    Terminal = 1
    Unknown = -1


@unique
class MoveType(Enum):
    pass


class Output_Production(object):
    def __init__(self, s):
        self.s = s

    def __str__(self):
        return self.s

    def __repr__(self):
        return self.__str__()


class Production(object):
    """
    产生式
    """

    # 静态变量
    # 非终止符集合
    non_terminal_syms = []
    # 终止符集合
    terminal_syms = []

    def __init__(self, left, right):
        # 产生式左边
        self.left = left
        # 产生式右边
        self.right = right

    def __str__(self):
        ret = self.left.__str__() + " -> "
        if len(self.right) == 0:
            return ret+"epsilon"
        for word in self.right:
            ret += str(word)+" "
        return ret

    def to_output(self):
        ret = "Production('"+str(self.left)+"',"+str(self.right)+')'
        return Output_Production(ret)

    def str_with_point(self, index):
        ret = self.left.__str__() + " -> "
        if len(self.right) == 0:
            ret += '.'
        for word, i in zip(self.right, range(len(self.right))):
            if i == index:
                ret += '.'
            ret += str(word) + " "
        if index == len(self.right):
            ret += '.'
        return ret

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __repr__(self):
        return self.__str__()

    def right_contains_terminal(self):
        for word in self.right:
            if word in Production.terminal_syms:
                return True
        return False

    def is_epsilon_production(self):
        return self.right is None

    def composed_with(self, l):
        is_composed = True
        if self.right is None:
            return False
        for sym in self.right:
            if sym not in l:
                is_composed = False
        return is_composed

    def right_begin_with_terminal(self):
        if len(self.right) == 0:
            return False
        return self.right[0] in Production.terminal_syms


class Item(object):
    """
    LR1 item
    """

    @classmethod
    def from_production(cls, prd, next_predict):
        item = Item(prd, next_predict, 0)
        # item.predict_next(firsts)
        return item

    def __init__(self, production, next_predict, index):
        """
        :param production: 产生式
        :param next_predict: 预测项
        :param index: 当前 . 的位置
        """
        self.production = production
        self.next_predict = next_predict
        self.index = index

    def __eq__(self, other):
        return self.production == other.production \
               and self.next_predict == other.next_predict \
               and self.index == other.index

    def __str__(self):
        s = '( '
        s += self.production.str_with_point(self.index)
        s += ', ' + str(self.next_predict) + ')'
        return s

    def is_reduction_item(self):
        if len(self.production.right) <= self.index:
            return True
        return False

    def is_next_symbol(self, symbol):
        right = self.production.right
        if len(right) <= self.index:
            return False
        return right[self.index] == symbol

    def move_to_next(self):
        new_item = Item(self.production, self.next_predict, self.index+1)
        return new_item

    def next_non_terminal(self):
        right = self.production.right
        if len(right) <= self.index:
            return False
        return right[self.index] in Production.non_terminal_syms

    def predict_next(self, firsts):
        right = self.production.right
        if len(right) <= self.index+1:
            return self.next_predict.copy()
        next_symbol = right[self.index+1]
        if next_symbol in Production.terminal_syms:
            return set([next_symbol])
        else:
            next_predict = [x for x in firsts[next_symbol] if x is not None]
            if None in firsts[next_symbol]:
                next_predict.extend(self.next_predict)
                next_predict = set(next_predict)
            return next_predict


class State(object):
    """
    状态
    """

    def __init__(self, items):
        """
        :param items: 该状态内的item
        """
        self.items = items

    def __eq__(self, other):
        if len(self.items) != len(other.items):
            return False

        for item in self.items:
            if item not in other.items:
                return False
        return True

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = ''
        for item in self.items:
            s += str(item)+'\n'
        return s

    def through_edge(self, edge):
        """
        :param edge: 通过的边
        :return:
        """
        new_items = [item.move_to_next() for item in self.items if item.is_next_symbol(edge)]
        # failed
        if len(new_items) == 0:
            return None
        return State(new_items)

    def expand(self, productions, firsts):
        """
        :param productions: 产生式集合
        :param firsts: 所有非终止符first
        :return:
        """
        # print("before: ")
        # print(self.__str__())
        is_changed = True
        while is_changed:
            is_changed = False
            for item in self.items:
                if item.next_non_terminal():
                    for prd in productions:
                        if item.is_next_symbol(prd.left):
                            next_predict = item.predict_next(firsts)
                            new_item = Item.from_production(prd, next_predict)
                            added = self.add_new_item(new_item)
                            if added:
                                is_changed = True
        # print("after:")
        # print(self.__str__())

    def add_new_item(self, new_item):
        for item in self.items:
            if item.production == new_item.production:
                if not item.next_predict.issuperset(new_item.next_predict):
                    item.next_predict = item.next_predict.union(new_item.next_predict)
                    return True
                else:
                    return False
        self.items.append(new_item)
        return True

    def find_reduction_item(self):
        return [item for item in self.items if item.is_reduction_item()]

    def contain_item_core(self, item):
        prds = [it.production for it in self.items]
        return item.production in prds

    def has_the_same_core(self, other):
        if len(self.items) != len(other.items):
            return False
        for item in self.items:
            if not other.contain_item_core(item):
                return False
        return True


