# !/bin/python3
# -*- coding: utf-8 -*-
"""这个函数负责
    1.提供输入txt
    2.将输入的点括号形式转换成数字形式stempos
    3.得到m ,输入中茎种类数
    4.得到   # 茎起始位  l_5 = []
            # 茎长度    l_long = []
            # 茎结束位  l_3 = []
"""
import parse_mid as pm


class Stack:
    """
    定义栈
    """

    def __init__(self):
        self.items = []

    def isEmpty(self):
        """
        判断栈空
        """
        return self.items == []

    def push(self, item):
        """
        入栈
        """
        self.items.append(item)

    def pop(self):
        """
        出栈
        """
        return self.items.pop()

    def peek(self):
        """
        返回栈顶元素
        """
        return self.items[-1]

    def size(self):
        """
        栈大小
        """
        return len(self.items)

    def print_stack(self):
        """
        输出栈中的元素
        """
        print(self.items)


def To_num(txt, mark_left, mark_right):
    lt = list(txt)
    # 让序列信息和数字1开始的信息绑定
    # (((((...)))((....))))
    # 123456789123456789123
    ls = list(enumerate(lt, 1))
    # 点括号输入的起始指针
    begin_index = 0
    # 茎起始位
    stems_5 = []
    # 茎长度
    stems_long = []
    # 茎结束位
    stems_3 = []
    # 栈
    s = Stack()
    '''第一次筛选，根据 【“)”的右边不再有“)”的入栈出栈方法，再把栈中最右端和右括号数量对应的左括号包围结构】  eg:((..))/(.((..))) 提取出来放入list_first（嵌套列表（嵌套每一种段的[
    list_mid]）） '''
    list_first = []
    while begin_index < len(ls):
        # 从头指针的位置开始读
        guid_index = begin_index
        while guid_index < len(ls):
            s.push(ls[guid_index])
            # 考虑数组越界加上guid_index == len(ls) - 1
            if guid_index == len(ls) - 1 or ls[guid_index][1] == f'{mark_right}' and ls[guid_index + 1][
                1] != f'{mark_right}':
                break
            guid_index += 1

        # print(s.items)
        # ['.', '(', '(', '.', '(', '(', '(', '.', '(', '(', '.', '.', '.', '.', ')', ')', ')', ')', ')']

        # 每次循环获得出来的 最右端 和num_) == num_( 的包围结构 存入list_mid
        list_mid = []
        # num_right  【)的数目】= s.items.count(')')
        num_right = 0
        for _, ch in s.items:
            if ch == f'{mark_right}':
                num_right += 1
        while num_right != 0:
            k = s.pop()
            list_mid.append(k)
            if k[1] == f'{mark_left}':
                num_right -= 1
        # print(list_mid) [(19, ')'), (18, ')'), (17, ')'), (16, ')'), (15, ')'), (14, '.'), (13, '.'), (12, '.'),
        # (11, '.'), (10, '('), (9, '('), (8, '.'), (7, '('), (6, '('), (5, '(')]
        list_mid.reverse()
        # [(5, '('), (6, '('), (7, '('), (8, '.'), (9, '('), (10, '('), (11, '.'), (12, '.'), (13, '.'), (14, '.'),
        # (15, ')'), (16, ')'), (17, ')'), (18, ')'), (19, ')')]
        list_first.append(list_mid)
        # 移动头指针，从下一个下标开始重新读入
        begin_index = guid_index + 1
    # for ls in list_first:
    #     print(ls)
    #     for i in ls:
    #         print(i[1],end='')
    #     print()
    '''第二次筛选，根据  【左右括号一定对称，且右边括号一定连续的原理】  来锁定list_first里面粗略分割出来的片段，实现列表中 嵌套的  只是 茎的片段'''
    list_stems = []
    # (((((...)))((....))))
    # [(3, '('), (4, '('), (5, '('), (6, '.'), (7, '.'), (8, '.'), (9, ')'), (10, ')'), (11, ')')]
    # [(1, '('), (2, '('), (12, '('), (13, '('), (14, '.'), (15, '.'), (16, '.'), (17, '.'), (18, ')'), (19, ')'), (20, ')'), (21, ')')]

    for i in list_first:
        # 弄两个结束指针 head,end指向每个字符串的头和尾，往中间靠
        # 弄两个打印指针 a,b 来确定打印的起始和结束位
        head_index = index_a = 0
        end_index = index_b = len(i) - 1
        while head_index < end_index:
            # todo 20210905 增加了一条规则，用于区分((( ((...)) )))的情况
            while i[head_index + 1][1] == f'{mark_left}' and i[head_index + 1][0]-i[head_index][0] == 1 and head_index < end_index:
                head_index += 1
                end_index -= 1
            list_stems.append(i[index_a:head_index + 1] + i[end_index:index_b + 1])
            # 让指针移动到下一位，然后开始检测
            head_index += 1
            # 检测下一个（左括号，不是就移动下一位。尾巴指针不动放在外围弄。
            while i[head_index][1] != f'{mark_left}' and head_index < end_index:
                head_index += 1
            # 右边的括号一定连续，所以只用在最后想左移动一个位置
            end_index -= 1
            # 移动打印指针
            index_a = head_index
            index_b = end_index

    '''最后更具茎段头下标的数字来排序，保证我的茎嵌套列表list_stems是根据5‘-3’的顺序弄出  S=S1S2...Sm'''
    list_stems.sort(key=lambda x: x[0][0])
    '''这样子，片段信息就全出来了'''
    # [[(2, '('), (3, '('), (42, ')'), (43, ')')],
    #  [(5, '('), (6, '('), (7, '('), (17, ')'), (18, ')'), (19, ')')],
    #  [(9, '('), (10, '('), (15, ')'), (16, ')')],
    #  [(23, '('), (24, '('), (25, '('), (39, ')'), (40, ')'), (41, ')')],
    #  [(27, '('), (28, '('), (29, '('), (33, ')'), (34, ')'), (35, ')')]]
    for k in list_stems:
        stems_5.append(k[0][0])
        stems_3.append(k[-1][0])
        stems_long.append(int(len(k) / 2))

    '''n 是 碱基长度 ,m_kinds 是 S茎序列种类数目'''
    n = len(txt)
    m_kinds = len(list_stems)
    stem_pos = [0 for _ in range(n + 1)]
    # print(stem_pos)[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    # 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for l in range(1, m_kinds + 1):
        z = l - 1
        for i in range(len(stem_pos)):
            if stems_5[z] <= i <= stems_5[z] + stems_long[z] - 1 or stems_3[z] - stems_long[z] + 1 <= i <= stems_3[z]:
                stem_pos[i] = l
    return stems_5, stems_long, stems_3, m_kinds, stem_pos


if __name__ == '__main__':
    txt = input('请输入二级结构（点括号形式）:')
    while True:
        if txt.count('(') == txt.count(')') and txt.count('[') == txt.count(']'):
            imf = pm.parse_mid(txt)
            # input_list, flag, L, insert, L_loop
            # (['((((((....).).)))).', '.[[[........]]]'], 1, 3, 6, 2)
            break
        else:
            print('Error ,input again')
            txt = input('请输入二级结构（点括号形式）：')
    tuple_list = []
    j = '()'
    for i in imf[0]:
        tuple_list.append(To_num(i, j[0], j[1]))
        j = '[]'

    for j in tuple_list:
        print(j)
# return stems_5, stems_long, stems_3, m_kinds, stem_pos
# (((..(.((.(..))).).((...)).)))
# ([1, 6, 8, 11, 20], [3, 1, 2, 1, 2], [30, 18, 16, 14, 26], 5, [0, 1, 1, 1, 0, 0, 2,
# 0, 3, 3, 0, 4, 0, 0, 4, 3, 3, 0, 2, 0, 5, 5, 0, 0, 0, 5, 5, 0, 1, 1, 1])

# .((((...[[[[[[.))))..].]].]]].
# ([2], [4], [19], 1, [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1])
# ([1, 4, 6], [3, 2, 1], [21, 17, 14], 3, [0, 1, 1, 1, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2, 2, 0, 1, 1, 1, 0])

# .((((((.......[[...[[[[[)))))).........].]].]]...]].
# ([2], [6], [30], 1, [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1])
# ([1, 6, 8, 10], [2, 2, 2, 1], [37, 32, 29, 26], 4, [0, 1, 1, 0, 0, 0, 2, 2, 3, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 3, 3, 0, 2, 2, 0, 0, 0, 1, 1, 0])


# (((((((((((.(((((..(((((....)))).)))))).))((((....))))((........)))))))))))
# ([1, 10, 13, 20, 21, 43], [11, 2, 5, 1, 4, 4], [75, 42, 39, 34, 32, 54], 6,
# [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 0, 3, 3, 3, 3, 3, 0, 0, 4, 5, 5, 5, 5, 0, 0, 0, 0, 5, 5, 5, 5, 0, 4, 3, 3, 3, 3, 3, 0, 2, 2, 6, 6, 6, 6, 0, 0, 0, 0, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

# (((((((((((.(((((..(((((....)))).)))))).))((((....)))))))))))))
# [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 3, 3, 3, 3, 3, 0, 0, 4, 5, 5, 5, 5, 0, 0, 0, 0, 5, 5, 5, 5, 0, 4, 3, 3, 3, 3, 3, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])