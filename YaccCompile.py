class Production(object):
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


lr_table = [{'b': [1], 'd': [2], 'S': [3], 'A': [4]},
            {'d': [5], 'A': [6]},
            {'c': [7], 'a': [Production('A',['d'])]},
            {'$': ['acc']},
            {'a': [8]},
            {'a': [9], 'c': [Production('A',['d'])]},
            {'c': [10]},
            {'$': [Production('S',['d', 'c'])]},
            {'$': [Production('S',['A', 'a'])]},
            {'$': [Production('S',['b', 'd', 'a'])]},
            {'$': [Production('S',['b', 'A', 'c'])]}]

lr_table = [{'E': [1], 'T': [2], 'F': [3], '(': [4], 'id': [5]},
 {'+': [6], '$': ['acc']},
  {'*': [7], '+': [Production('E',['T'])], '$': [Production('E',['T'])]},
   {'*': [Production('T',['F'])], '+': [Production('T',['F'])], '$': [Production('T',['F'])]},
    {'E': [8], 'T': [9], 'F': [10], 'id': [11]},
     {'*': [Production('F',['id'])], '+': [Production('F',['id'])], '$': [Production('F',['id'])]},
      {'T': [12], 'F': [3], '(': [4], 'id': [5]},
       {'F': [13], '(': [4], 'id': [5]},
        {'+': [14], ')': [15]},
         {'*': [16], '+': [Production('E',['T'])], ')': [Production('E',['T'])]},
          {'+': [Production('T',['F'])], ')': [Production('T',['F'])], '*': [Production('T',['F'])]},
           {'+': [Production('F',['id'])], ')': [Production('F',['id'])], '*': [Production('F',['id'])]},
            {'*': [7], '+': [Production('E',['E', '+', 'T'])], '$': [Production('E',['E', '+', 'T'])]},
             {'*': [Production('T',['T', '*', 'F'])], '+': [Production('T',['T', '*', 'F'])], '$': [Production('T',['T', '*', 'F'])]},
              {'T': [17], 'F': [10], '(': [18], 'id': [11]},
               {'*': [Production('F',['(', 'E', ')'])], ')': [Production('F',['(', 'E', ')'])], '+': [Production('F',['(', 'E', ')'])], '$': [Production('F',['(', 'E', ')'])]},
                {'F': [19], '(': [18], 'id': [11]},
                 {'*': [16], '+': [Production('E',['E', '+', 'T'])], ')': [Production('E',['E', '+', 'T'])]},
                  {'E': [20], 'T': [9], 'F': [10], 'id': [11]},
                   {'+': [Production('T',['T', '*', 'F'])], ')': [Production('T',['T', '*', 'F'])], '*': [Production('T',['T', '*', 'F'])]},
                    {'+': [14], ')': [21]},
                     {'+': [Production('F',['(', 'E', ')'])], ')': [Production('F',['(', 'E', ')'])], '*': [Production('F',['(', 'E', ')'])]}]

def get_input(input_path):
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
    analysis(expression)

