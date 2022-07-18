# !/bin/python3
# -*- coding: utf-8 -*-
# .((.(((.((....)))))...(((.(((...)))...)))))
# .[[[..((((((]]].).).)))).
# [[[[[[........(((((((((]]]]]]........))))))))).
# ((.((..))(((.(((...))).((..)).)))))
# (((((..(((((....)))))..((((....))))......))))).
# ....(((.((....)))))...(((.(((...)))...)))..
# ((((.((([[[[.(((((((((...[[(((((.(....).)))))......))))))))).........)))))))......]].............]]]]
import os
import glob
import shutil


class Node:
    """
    树结点 定义树，并加上深度优先搜索方法
    """

    def __init__(self, name, value=0):
        # 嵌套列表表示树结构
        # name 表示这个节点的名字，方便后续显示和确定树结构
        # value 用于存放茎长度
        self._name = name
        self._value = value
        self._children = []

    # 用来表示
    def __repr__(self):
        return 'Node({!r})'.format(self._name)

    def add_child(self, node):
        """
        添加子节点
        """
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        """
        深度优先搜索
        """
        yield self
        for c in self:
            yield from c.depth_first()
    # 它首先返回自己本身并迭代每一个子节点并通过调用子节点的depth_first() 方法(使用yield from 语句) 返回对应元素。


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


def To_num_small(txt):
    lt = list(txt)
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
            if guid_index == len(ls) - 1 or ls[guid_index][1] == ')' and ls[guid_index + 1][1] != ')':
                break
            guid_index += 1

        # print(s.items)
        # ['.', '(', '(', '.', '(', '(', '(', '.', '(', '(', '.', '.', '.', '.', ')', ')', ')', ')', ')']

        # 每次循环获得出来的 最右端 和num_) == num_( 的包围结构 存入list_mid
        list_mid = []
        # num_right  【)的数目】= s.items.count(')')
        num_right = 0
        for _, ch in s.items:
            if ch == ')':
                num_right += 1
        while num_right != 0:
            k = s.pop()
            list_mid.append(k)
            if k[1] == '(':
                num_right -= 1
        # print(list_mid) [(19, ')'), (18, ')'), (17, ')'), (16, ')'), (15, ')'), (14, '.'), (13, '.'), (12, '.'),
        # (11, '.'), (10, '('), (9, '('), (8, '.'), (7, '('), (6, '('), (5, '(')]
        list_mid.reverse()
        # [(5, '('), (6, '('), (7, '('), (8, '.'), (9, '('), (10, '('), (11, '.'), (12, '.'), (13, '.'), (14, '.'),
        # (15, ')'), (16, ')'), (17, ')'), (18, ')'), (19, ')')]
        list_first.append(list_mid)
        # 移动头指针，从下一个下标开始重新读入
        begin_index = guid_index + 1
    '''第二次筛选，根据  【左右括号一定对称，且右边括号一定连续的原理】  来锁定list_first里面粗略分割出来的片段，实现列表中 嵌套的  只是 茎的片段'''
    list_stems = []
    for i in list_first:
        # 弄两个指针指向每个字符串的头和尾，往中间靠
        # 在弄两个指针a.b来固定打印的起始和结束位
        head_index = index_a = 0
        end_index = index_b = len(i) - 1
        while head_index < end_index:
            # A((( head.((....)))end)))B  分开
            while i[head_index][1] == '(' and head_index < end_index:
                head_index += 1
                end_index -= 1
            # print(i[:head_index]+i[end_index+1:])
            # [(5, '('), (6, '('), (7, '('), (17, ')'), (18, ')'), (19, ')')]
            list_stems.append(i[index_a:head_index] + i[end_index + 1:index_b + 1])
            # print(list_stems)
            # [[(5, '('), (6, '('), (7, '('), (17, ')'), (18, ')'), (19, ')')]]
            # 继续移动左边指针，到下一个（左括号，尾巴指针不动，因为右边一定都是右括号

            while i[head_index][1] != '(' and head_index < end_index:
                head_index += 1
            index_a = head_index
            index_b = end_index

    '''最后更具茎段头下标的数字来排序，保证我的茎嵌套列表list_stems是根据5‘-3’的顺序弄出  S=S1S2...Sm'''
    list_stems.sort(key=lambda x: x[0][0])
    # print(list_.((.(((.((....)))))...(((.((...))...)))))tems)
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


def To_num(txt, mark_left, mark_right):
    lt = list(txt)
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
    '''第二次筛选，根据  【左右括号一定对称，且右边括号一定连续的原理】  来锁定list_first里面粗略分割出来的片段，实现列表中 嵌套的  只是 茎的片段'''
    list_stems = []
    for i in list_first:
        # 弄两个指针指向每个字符串的头和尾，往中间靠
        # 在弄两个指针a.b来固定打印的起始和结束位
        head_index = index_a = 0
        end_index = index_b = len(i) - 1
        while head_index < end_index:
            # todo 20210905 增加了一条规则，用于区分((( ((...)) )))的情况
            while i[head_index + 1][1] == f'{mark_left}' and i[head_index + 1][0] - i[head_index][0] == 1 and head_index < end_index:
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


def To_tree(l_5, l_long, l_3, m, stempos):
    """
        input:
                stempos:数字形式二级结构
                m:茎种类数
        return:
                这个函数用来返回d_stems,和order_lt,lst_node,index
    """
    # 拼装顺序列表
    order_lt = []
    # 节点列表长度m == 多少个茎 + 1(1是因为算上数组下标为0 处 存放一个无效节点)
    m += 1
    # 来存储节点的列表[Node(-1), Node(-1), Node(-1), Node(-1), Node(-1), Node(-1)]
    lst_node = [Node(-1) for _ in range(m)]
    # 栈对象s
    s = Stack()
    # d_stems用字典的形式来表示各个茎(不包括下标为0的虚根)的长度、起始位、结束位(dn.l_long)
    # {1: (2, 2, 43), 2: (3, 5, 19), 3: (2, 9, 16), 4: (3, 23, 41), 5: (3, 27, 35)}
    # {1: (3, 5, 19), 2: (2, 9, 16), 3: (3, 23, 41), 4: (3, 27, 35)}
    d_stems = dict(enumerate(zip(l_long, l_5, l_3), 1))

    # todo 20210904 加一个0节点，这里面只存第一个非零下标和最后一个非零下标
    begin = 1
    end = len(stempos) - 1
    d_stems.update({0: (0, begin, end)})

    '''step1:设定头尾指针i/j ,然后分别向内移动，找到第一个不为零的地方，令其位置为i0,j0'''
    # 头指针i,尾指针j
    i = 0
    j = len(stempos) - 1

    # i,j移动到第一个不为零的地方,令其为i0,j0
    while stempos[i] == 0:
        i += 1
    i0 = i
    while stempos[j] == 0:
        j -= 1
    j0 = j

    '''step2:看i0和j0处的stempos值是否一样来确定是否需要生成 虚根节点
    若 stempos[i0] != stempos[j0] 生成虚根节点s(0), 且 0 进栈S，并 生成子节点s(stempos(j0)),stempos(j0)进栈S'''
    if stempos[i0] != stempos[j0]:
        lst_node[0] = Node(0)
        s.push(0)
        lst_node[stempos[j0]] = Node(stempos[j0])
        lst_node[0].add_child(lst_node[stempos[j0]])
        s.push(stempos[j0])
        # [Node(0), Node(-1), Node(-1), Node(3), Node(-1)]
    else:
        lst_node[1] = Node(1)
        s.push(stempos[i0])
        # [Node(-1), Node(1), Node(-1), Node(-1), Node(-1), Node(-1)]

    '''step3:不断移动j指针，向左移动至下一段非0区的结束位，移动j是为了后续指针顺序是个从 右子树读入的顺序 
    并查看 栈顶元素k 和此时stempos[j0] 值，相等则出栈，不相等则入栈'''
    while i0 <= j0:
        # 寻找j向左移的下一个非0的结束位（末端）
        j = j0
        while (stempos[j - 1] == stempos[j] or stempos[j - 1] == 0) and i0 < j:
            j -= 1
        j0 = j - 1
        # 查看栈顶元素
        k = s.peek()
        # num_index树节点下标
        num_index = stempos[j0]
        if k != num_index:
            lst_node[num_index] = Node(num_index)
            lst_node[k].add_child(lst_node[num_index])
            s.push(num_index)
        else:
            s.pop()
        '''step4:每一次都判断一下栈是否为空，空就结束，否则跳转到step3'''
        if s.isEmpty():
            break

    index = 0
    # 通过这一步来区分非闭合茎和闭合茎的下标,非闭合茎有虚根Node(0)所以 index = 0
    for index in range(len(lst_node)):
        if lst_node[index]._name != -1:
            break

    # 在这里，把茎长度载入每个实例对象的_value值中
    for i in range(1, len(lst_node)):
        lst_node[i]._value = l_long[i - 1]

    # todo 20210904
    if index == 0:
        lst_node[0]._value = 0

    for ch in lst_node[index].depth_first():
        order_lt.append(ch)
    return order_lt, d_stems, lst_node, index


def Bref_Frag_index(inode, d_stems, stempos, n_bp, star_flag, stop_flag):
    """
    得到结构信息，和片段下标index
    :param inode:
    :param d_stems:
    :param stempos:
    :param n_bp:
    :return:
    """
    frag_value_Y = inode._value
    frag_name_Y = 'stems'
    frag_value_X = 0
    frag_name_X = ''
    index_long, index_5, index_3 = d_stems[inode._name]
    # 区分begin_stems
    if int(inode._name) == 1:
        index_lt_Y = [star_flag, index_5 + (index_long - 1), index_3 - (index_long - 1), stop_flag]
        frag_value_Y = f'{index_5 - star_flag}_{inode._value}_{stop_flag - index_3}'
        frag_name_Y = 'stems_begin'
    elif int(inode._name) == 0:
        index_lt_Y = [0]
        frag_name_Y = 'faker_stems'
    else:
        index_lt_Y = [index_5, index_5 + (index_long - 1), index_3 - (index_long - 1), index_3]
    # print(inode._name)
    # d_stems = dict(enumerate(zip(index_long, index_5, index_3), 1))
    if len(inode._children) == 0:
        # index_long, index_5, index_3 = d_stems[inode._name]
        l_stems = index_long
        l_hairpin = [index_3 - index_5 - 1 - (l_stems - 1) * 2]
        frag_value_X = l_hairpin
        frag_name_X = 'hairpin_loop'
        # 增加读取下标
        index_lt_X = [index_5 + (index_long - 1), index_3 - (index_long - 1)]

    elif len(inode._children) == 1:
        a = inode._name
        b = inode._children[0]._name
        l_stems_father = d_stems[a][0]
        if d_stems[b][1] - d_stems[a][1] == l_stems_father or d_stems[a][2] - d_stems[b][2] == l_stems_father:
            l_bulge = [d_stems[b][1] - d_stems[a][1] - l_stems_father, d_stems[a][2] - d_stems[b][2] - l_stems_father]
            frag_value_X = l_bulge
            frag_name_X = 'bulge_loop'
        else:
            l_iloop = [d_stems[b][1] - d_stems[a][1] - l_stems_father, d_stems[a][2] - d_stems[b][2] - l_stems_father]
            frag_value_X = l_iloop
            frag_name_X = 'interior_loop'

        index_lt_X = [index_5 + (index_long - 1), d_stems[b][1], d_stems[b][2], index_3 - (index_long - 1)]
        # # print(index_lt_X)
        # flag = -1
        # for mm in range(len(index_lt_X)):
        #     index_lt_X[mm] += flag * (n_bp-1)
        #     flag *= -1
        # # print(index_lt_X)

    elif len(inode._children) >= 2:
        name_node = inode._name
        n_way = len(inode._children) + 1
        lst_node_num = list(range(n_way))
        # print(lst_node_num)  [0, 1, 2]
        lst_node_num[0] = inode._name
        # print(lst_node_num) [1, 1, 2]
        for j in range(n_way - 1):
            lst_node_num[j + 1] = inode._children[j]._name
        # print(lst_node_num) [1, 4, 2]
        lst_node_num.sort()
        lst_index = list(range(n_way))
        for inode in range(n_way):
            lst_index[inode] = [j for j, x in enumerate(stempos) if x == lst_node_num[inode]]
        # print(lst_index)
        if lst_node_num[0] != 0:
            num_enter = len(lst_index[0])
            demi_num_enter = int(num_enter / 2)
            lst_index.append(lst_index[0][demi_num_enter:])
            lst_index[0] = lst_index[0][:demi_num_enter]
        elif lst_node_num[0] == 0:
            lst_index.append([len(stempos)])
            lst_index[0] = [0]
        # print(lst_index)
        l_multiloop = []
        for j in range(len(lst_index) - 1):
            l_multiloop.append(lst_index[j + 1][0] - lst_index[j][-1] - 1)
        frag_value_X = l_multiloop
        if name_node != 0:
            frag_name_X = 'multi_loop'
        else:
            frag_name_X = 'faker_multi_loop'

        # todo 20210904
        if frag_name_X == 'multi_loop':
            index_lt_X = [index_5 + (index_long - 1), index_3 - (index_long - 1)]
        else:
            index_lt_X = [index_5, index_3]

        for j in lst_node_num[1:]:
            for k in d_stems[j][1:]:
                index_lt_X.insert(-1, k)

    '''这里末端多读取的bp数目'''
    flag = -1
    # 如果是'faker_multi_loop' 则不动收尾下标，只动中间的下标
    if frag_name_X == 'faker_multi_loop':
        for mm in range(1, len(index_lt_X)-1):
            flag *= -1
            index_lt_X[mm] += flag * (n_bp - 1)
    else:
        for mm in range(len(index_lt_X)):
            index_lt_X[mm] += flag * (n_bp - 1)
            flag *= -1

    frag_value_X = '_'.join([str(ii) for ii in frag_value_X])
    return frag_name_X, frag_value_X, index_lt_X, frag_name_Y, frag_value_Y, index_lt_Y


def create_pdb(file_origin_lt, struct_imf, new_file_path):
    """

    :param file_origin_lt: pdb_lines初始pdb文件所有内容列表形式
    :param struct_imf: ('stems_begin', 6, [1, 6, 33, 39])/('bulge_loop', '0_3', [6, 7, 29, 33])
    :param new_file_path: 新模块的pdb文件路径
    """
    if struct_imf[0] == 'faker_stems':
        # 如果是 'faker_stems'就不创建模块文件，返回False ,让后续也不移动文件
        return False

    index_ls = struct_imf[2]
    # [3, 5, 19, 23, 41, 42]/[7, 9, 16, 17]/[9, 16]
    with open(new_file_path, 'w') as f:
        for n in range(0, len(index_ls), 2):
            begin_index = index_ls[n]
            end_index = index_ls[n + 1]
            for line in file_origin_lt:
                if begin_index <= int(line[22:26]) <= end_index:
                    f.write(line)
    return True


def move_pdb(old_path, struct_imf, n, name_num):
    """
    将得到的结构模块pdb,移动到数据库中
    :param old_path:
    :param struct_imf:
    """
    if 'stems' in struct_imf[0]:
        new_pdb_path = rf'./database/{struct_imf[0]}/{struct_imf[1]}'
    elif struct_imf[0] == 'pseudoknot_loop':
        new_pdb_path = rf'./database/{struct_imf[0]}/{struct_imf[1]}'
    else:
        new_pdb_path = rf'./database/{n}_bp/{struct_imf[0]}/{struct_imf[1]}'
    if not os.path.exists(new_pdb_path):
        os.mkdir(new_pdb_path)
    shutil.move(old_path, new_pdb_path)
    shutil.move(new_pdb_path+r'/'+old_path, new_pdb_path+r'/'+old_path.split('.')[0]+fr'_{name_num}.pdb')


if __name__ == '__main__':
    dir_path = r'pdb'
    for i in os.listdir(dir_path):
        print(i)
        # Long_mid_start = 0
        num = 0
        pdb_id = i
        new_path = f'{pdb_id}.pdb'

        pdb_file = dir_path + fr'/{pdb_id}/{pdb_id}.pdb'
        with open(pdb_file, 'r') as f:
            pdb_lines = f.readlines()
        path = dir_path + fr'/{pdb_id}/{pdb_id}.dbn'
        with open(path, 'r') as f:
            lines = f.readlines()
            # 去除头尾的空行
            txt = lines[2].strip()
            # print(txt)
        while True:
            # txt = input('请输入二级结构（点括号形式）：')
            if txt.count('(') == txt.count(')') and txt.count('[') == txt.count(']') and txt.count('{') == txt.count('}'):
                break
            else:
                print('Error ,input again')
                break

        print('————————片段结构信息+下标信息————————')

        txt = txt.replace('{', '.')
        txt = txt.replace('<', '.')
        txt = txt.replace('}', '.')
        txt = txt.replace('>', '.')

        fflag = 0
        star_mark = 1
        stop_mark = len(txt)
        l_small = txt.find('(')
        l_mid = txt.find('[')
        r_small = txt.rfind(')')
        r_mid = txt.rfind(']')

        # todo 20210905
        if l_small < l_mid and r_small > r_mid:
            txt = txt.replace('[', '.')
            txt = txt.replace(']', '.')

        if '[' in txt:
            if l_small < l_mid:
                # 先小括号开头.((..[[))...]]..
                star_mark = l_mid + 1
                stop_mark = r_small + 1
                fflag = 1
            elif l_small > l_mid:
                # 先中括号开头.[[..((]]...))..
                star_mark = l_small + 1
                stop_mark = r_mid + 1
                fflag = -1

        '''各自括号类型的片段截取'''
        for j in ['()', '[]']:
            num_imf_tuple = To_num(txt, f'{j[0]}', f'{j[1]}')
            # return stems_5, stems_long, stems_3, m_kinds, stem_pos

            try:
                order_lt, d_stems, lst_node, index = To_tree(*num_imf_tuple)
            except:
                print(f'there is no "{j}" in input')
                continue

            for i in lst_node[index:]:
                # 用num_bp = 0 来把stem段和loop段分离开，不然stem段会重复出现好几次
                for num_bp in range(0, 4):
                    '''这里用Node._value,以及chiledre的_value来比较，看这个片段最长可以多分解几个口子,
                    添加一个检测，防止有些片段本身就不能保留3bp'''
                    stem_long_lt = [i._value]
                    for chil in i._children:
                        # print(chil._value)
                        stem_long_lt.append(chil._value)
                    # num_bp是从小到大，所以一旦超过允许最大的bp数就直接退出这个节点
                    # todo 20210904
                    if min(stem_long_lt) == 0:
                        stem_long_lt.remove(0)

                    if num_bp > min(stem_long_lt):
                        break

                    # 用fflag来区分这个模块有无假结/假结[开头/假借(开头
                    if fflag == 0:
                        imf = Bref_Frag_index(i, d_stems, num_imf_tuple[4], num_bp, star_mark, stop_mark)
                    elif fflag == 1:
                        if j == '()':
                            imf = Bref_Frag_index(i, d_stems, num_imf_tuple[4], num_bp, 1, stop_mark)
                        elif j == '[]':
                            imf = Bref_Frag_index(i, d_stems, num_imf_tuple[4], num_bp, star_mark, len(txt))
                    elif fflag == -1:
                        if j == '()':
                            imf = Bref_Frag_index(i, d_stems, num_imf_tuple[4], num_bp, star_mark, len(txt))
                        elif j == '[]':
                            imf = Bref_Frag_index(i, d_stems, num_imf_tuple[4], num_bp, 1, stop_mark)

                    # 用0bp来把stem段和loop段分离开，不然stem段会重复出现好几次
                    if num_bp != 0:
                        input_imf = imf[:3]
                        print(num_bp, end=f'----{imf[:3]}\n')
                        # 1----('bulge_loop', '0_3', [6, 7, 29, 33], 'stems', 6, [1, 6, 33, 39])
                    else:
                        # if imf[-3] == 'stems_begin':
                        #     if j == '[]':
                        #         # 求出假借的[]头茎长方便后面分离假借环
                        #         Long_mid_start = imf[-2].split('_')[1]
                        input_imf = imf[-3:]
                        print(imf[-3:])

                    '''根据信息创建 模块的pdb'''
                    # switch 开关，有创建才移动
                    switch = create_pdb(pdb_lines, input_imf, new_path)
                    if switch:
                        move_pdb(new_path, input_imf, num_bp,num)
                    num += 1

        # todo 修改版
        '''假借模块'''
        # if Long_mid_start != 0:
        if '[' in txt:
            # ((((.((([[[[.(((((((((...[[(((((.(....).)))))......))))))))).........)))))))......]].............]]]]
            num_bp = 0
            p_imf = ['pseudoknot_loop']
            # L = int(Long_mid_start)
            # print(L,end='+++')
            # if '(' in txt[l_mid:r_mid + 1]:
            if l_small > l_mid:
                # p_imf.append(l_small - l_mid - (L - 1) - 1)
                p_imf.append(txt.find('(') - txt.rfind('[') - 1)
                p_imf.append([txt.rfind('[') + 1, txt.find('(') + 1])
            # elif ')' in txt[l_mid:r_mid + 1]:
            elif l_small < l_mid:
                # p_imf.append(r_mid - (L - 1) - r_small - 1)
                p_imf.append(txt.find(']') - txt.rfind(')') - 1)
                p_imf.append([txt.rfind(')') + 1, txt.find(']') + 1])
            print(tuple(p_imf))
            create_pdb(pdb_lines, p_imf, new_path)
            move_pdb(new_path, p_imf, num_bp, num)

        '''用来删除垃圾'''
        for k in glob.glob(r'./*.pdb'):
            os.remove(k)
