prefix = """class Production(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        ret = self.left.__str__() + " -> "
        if len(self.right) == 0:
            return ret + "epsilon"
        for word in self.right:
            ret += str(word) + " "
        return ret
"""

suffix = """def get_input(input_path):
    ret = []
    with open(input_path, 'r+') as f:
        line = f.readline()
        ret = line.strip().split()
    return ret


def str_expression(expression, i):
    ret = ' '.join([str(s) for s in expression[i:]])
    return ret


def analysis(expression):

    expression.append('$')
    i = 0
    is_success = False
    symbol_stack = []
    state_stack = [0]
    a = expression[0]
    k = 1
    while i < len(expression):
        out_str = '('+str(k)+')       '
        k += 1
        out_str += str_expression(state_stack, 0)+"       "
        out_str += str_expression(symbol_stack, 0)+"\t       "
        out_str += str_expression(expression, i)+"       "

        s = state_stack[-1]
        action = lr_table[s].get(a, None)
        if type(action[0]) is int:
            state_stack.append(action[0])
            symbol_stack.append(a)
            i += 1
            a = expression[i]
            out_str += 'shift '+str(action[0])
        elif action[0] == 'acc':
            is_success = True
            out_str += 'accept'
            print(out_str)
            break
        elif type(action[0]) is Production:
            for j in range(len(action[0].right)):
                symbol_stack.pop()
                state_stack.pop()
            goto = lr_table[state_stack[-1]].get(action[0].left, None)
            # if goto is not None:
            state_stack.append(goto[0])
            symbol_stack.append(action[0].left)
            out_str += 'reduce by '+str(action[0])
        else:
            break
        print(out_str)

    if is_success:
        print('complete')
    else:
        print('error')


if __name__ == '__main__':
    import sys

    input_path = sys.argv[1]
    # output_path = sys.argv[2]
    # input_path = "TestExpression1.txt"
    expression = get_input(input_path)
    analysis(expression)"""


def yacc_output(lr1_table, path):
    """
    输出yacc程序
    :param lr1_table: lr1 parsing table
    :param path: 要输出的语法分析程序
    :return:
    """
    ret = prefix
    ret += "lr_table = "
    ret += str(lr1_table)+"\n"
    ret += suffix
    with open(path, 'w+') as f:
        f.write(ret)