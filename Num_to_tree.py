# !/bin/python3
# -*- coding: utf-8 -*-

import Dot_to_num as dn
import parse_mid as pm


# todo (((.(((..[))).(((]...))).(((..[[[))).))).]]]

# ((.((..))(((.(((...))).((..)).)))))
# (((((..(((((....)))))..((((....))))......))))).
# .((.(((.((....)))))...(((.(((...)))...)))))
# ....(((.((....)))))...(((.(((...)))...)))..
# ((((.((([[[[.(((((((((...[[(((((.(....).)))))......))))))))).........)))))))......]].............]]]]
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


def showfragimf(inode, d_stems, stempos):
    '''根据命题来  打印输出，并返回   每个节点都是什么模块
        命题:1.若节点i没有子节点，则i处有一个发卡环
            2.若节点i仅有一个子节点j，则i与j之间存在凸环/内环（通过后续茎的下标关系推断）
            3.若节点i有k(k>=2)个子节点，则i与其k个子节点构成多分枝环（分支环数=k+1）'''
    if len(inode._children) == 0:
        '''命题1'''
        print(f'{inode} need a hairpin_loop', end=':')
        l_stems = d_stems[inode._name][0]
        # print(f'stems:{l_stems}', end='+')
        # 茎段的 结束位-起始位-1-（茎长-1）*2
        l_hairpin = d_stems[inode._name][2] - d_stems[inode._name][1] - 1 - (l_stems - 1) * 2
        print(f'nts={l_hairpin + 2};[{l_hairpin}]')
        return l_hairpin
    elif len(inode._children) == 1:
        '''命题2'''
        # 节点a名字->2,子节点b名字->3
        a = inode._name
        b = inode._children[0]._name
        # 父节点的茎长l_stems_a->3，和子节点的茎长l_stems_b->2
        l_stems_father = d_stems[a][0]
        '''  根据父子茎的下标关系推断 是凸环/或内环   （父起始... （子起始 ...子结尾）... 父结尾）
            （子起始-父起始）/ （父结尾-子结尾） == 父茎长  --->  bulge
            （子起始-父起始）/ （父结尾-子结尾） == 父茎长  --->  interior
        '''
        if d_stems[b][1] - d_stems[a][1] == l_stems_father or d_stems[a][2] - d_stems[b][2] == l_stems_father:
            print(f'Between {inode} and {inode._children[0]} need a bulge_loop', end=':')
            # bulge: nts=5; [1,0]; 5 = 1+4
            l_bulge = [d_stems[b][1] - d_stems[a][1] - l_stems_father, d_stems[a][2] - d_stems[b][2] - l_stems_father]
            nt_num = sum(l_bulge) + 4
            print(f'nts={nt_num}; {l_bulge}')
            return l_bulge
        else:
            print(f'Between {inode} and {inode._children[0]} need a interior_loop', end=':')
            # internal loop: nts=8; [2,2]
            l_iloop = [d_stems[b][1] - d_stems[a][1] - l_stems_father, d_stems[a][2] - d_stems[b][2] - l_stems_father]
            nt_num = sum(l_iloop) + 4
            print(f'nts={nt_num}; {l_iloop}')
            return l_iloop

    elif len(inode._children) >= 2:
        '''命题3'''
        # 算出多分支的分支数目
        childre_node = '+'.join([str(m) for m in inode._children])
        n_way = len(inode._children) + 1

        if inode._name != 0:
            print(f'Between {inode} and {childre_node} need a {n_way}-way multi_loop', end=':')
        else:
            # TODO 我也不知道这种情况叫什么
            print(f'Between {inode} and {childre_node} need a {n_way}-way faker_multi_loop', end=':')

        # 节点名-->[1, 4, 2]
        lst_node_num = list(range(n_way))
        lst_node_num[0] = inode._name
        for j in range(n_way - 1):
            lst_node_num[j + 1] = inode._children[j]._name

        # 把节点名-->排个序[1, 2, 4]
        lst_node_num.sort()

        # 各个茎的下标二维数组
        # [[2, 3, 42, 43], [5, 6, 7, 17, 18, 19], [23, 24, 25, 39, 40, 41]]
        lst_index = list(range(n_way))
        for inode in range(n_way):
            lst_index[inode] = [j for j, x in enumerate(stempos) if x == lst_node_num[inode]]
        # print(lst_index)

        # 调整下标二维数组的形式，把junction的入口茎端的列表 分开 放两头
        # [[2, 3], [5, 6, 7, 17, 18, 19], [23, 24, 25, 39, 40, 41], [42, 43]]
        # 如果是实根开始，则直接表示开始和结束的原子位置
        if lst_node_num[0] != 0:
            num_enter = len(lst_index[0])
            demi_num_enter = int(num_enter / 2)
            lst_index.append(lst_index[0][demi_num_enter:])
            lst_index[0] = lst_index[0][:demi_num_enter]
        # 如果是虚根开始，则直接表示开始和结束的原子位置
        elif lst_node_num[0] == 0:
            # lst_index.append([lst_index[0][-1] + 1])
            # lst_index[0] = [0]
            lst_index.append([len(stempos)])
            lst_index[0] = [0]

        # 分段总是用下一个数组的[0]-上一个数组的[-1]再-1就是环的长度
        l_multiloop = []
        for j in range(len(lst_index) - 1):
            l_multiloop.append(lst_index[j + 1][0] - lst_index[j][-1] - 1)
        nt_num = sum(l_multiloop) + 4
        print(f'nts={nt_num}; {l_multiloop}')
        return l_multiloop


# d_stems用字典的形式来表示各个茎(不包括下标为0的虚根)的长度、起始位、结束位(dn.l_long)
# {1: (2, 2, 43), 2: (3, 5, 19), 3: (2, 9, 16), 4: (3, 23, 41), 5: (3, 27, 35)}
# {1: (3, 5, 19), 2: (2, 9, 16), 3: (3, 23, 41), 4: (3, 27, 35)}
def Bref_Fragimf(inode, d_stems, stempos, sec_txt):
    """

    输入：
        i:Node信息
        d_stems: Tree_imf函数的返回结果
        stempos: Dot_to_num.py中函数To_num返回的结果
        sec_txt: 二级结构用来找到开头茎的区分

    返回：
        ('hairpin_loop', '4', 'stems', 4)这种简单形式表示结构片段信息
        如果是假借上面的发卡环，则会变成('Hairpin_loop', '4', 'stems', 2)，大写字母开头以便区分

    """
    frag_value_Y = inode._value
    frag_name_Y = 'stems'
    frag_value_X = 0
    frag_name_X = ''
    # 这个if是区分头原子代码段，不区分就直接删掉
    # if int(inode._name) == 1:
    #     if '[' in sec_txt:
    #         star = l_mid
    #         stop = r_mid
    #     elif '(' in sec_txt:
    #         star = l_small
    #         stop = r_small
    #     frag_value_Y = f'{star-0}_{inode._value}_{len(sec_txt)-1-stop}'
    #     frag_name_Y = 'stems_begin'

    num_pse_in = 0
    if len(inode._children) == 0:
        # 茎秆长度
        l_stems = d_stems[inode._name][0]
        # d_stems用字典的形式来表示各个茎(不包括下标为0的虚根)的长度、起始位、结束位(dn.l_long)
        # {1: (6, 2, 30)}      .((((((.......[[...[[[[[))))))
        # {1: (2, 1, 37), 2: (2, 6, 32), 3: (2, 8, 29), 4: (1, 10, 26)}    [[...[[[[[)))))).........].]].]]...]].
        # 环区长度 .(((...))) 为3
        l_hairpin = [d_stems[inode._name][2] - d_stems[inode._name][1] - 1 - (l_stems - 1) * 2]
        '''发卡环环区部分，括号中的点内容'''
        contents_in_txt = sec_txt[d_stems[inode._name][1] - 1 + l_stems: d_stems[inode._name][2] - l_stems]
        # print("------",sec_txt[d_stems[inode._name][1]-1 + l_stems: d_stems[inode._name][2] - l_stems])
        '''
        看区间内'('')'是否有杂质
        # sec_txt = .((((...[[[[[[.))))
        '''
        # for c in contents_in_txt:
        #     # 发现杂质直接退出，库变成大写的库。
        #     if c != "." and c != "&":
        #         frag_name_X = 'hybrid_hairpin_loop'
        #         break
        #     else:
        #         frag_name_X = 'hairpin_loop'
        for c in contents_in_txt:
            # 发现杂质直接退出，库变成大写的库。
            if c != "." and c != "&":
                num_pse_in += 1
        if num_pse_in != 0:
            frag_name_X = 'hybrid_hairpin_loop'
            l_hairpin.append(num_pse_in)
        else:
            frag_name_X = 'hairpin_loop'
        frag_value_X = l_hairpin
        # frag_name_X = 'hairpin_loop'
    elif len(inode._children) == 1:
        # .((((((.......[[...[[[[[)))))).........].]].]]...]].
        # [[...[[[[[)))))).........].]].]]...]].
        # [0, 1, 1, 0, 0, 0, 2, 2, 3, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 3, 3, 0, 2, 2, 0, 0, 0, 1, 1, 0]
        # 父节点
        a = inode._name
        # 子节点
        b = inode._children[0]._name
        # 父节点茎秆长度
        l_stems_father = d_stems[a][0]
        # l_stems_child = d_stems[b][0]
        if d_stems[b][1] - d_stems[a][1] == l_stems_father or d_stems[a][2] - d_stems[b][2] == l_stems_father:
            l_bulge = [d_stems[b][1] - d_stems[a][1] - l_stems_father, d_stems[a][2] - d_stems[b][2] - l_stems_father]
            frag_value_X = l_bulge
            contents_in_txt = sec_txt[d_stems[a][1] - 1 + l_stems_father: d_stems[b][1] - 1] + sec_txt[d_stems[b][2] : d_stems[a][2] - l_stems_father]
            for c in contents_in_txt:
                # 发现杂质直接退出，库变成大写的库。
                if c != "." and c != "&":
                    frag_name_X = 'hybrid_bulge_loop'
                    break
                else:
                    frag_name_X = 'bulge_loop'
            # frag_name_X = 'bulge_loop'
        else:
            l_iloop = [d_stems[b][1] - d_stems[a][1] - l_stems_father, d_stems[a][2] - d_stems[b][2] - l_stems_father]
            frag_value_X = l_iloop
            contents_in_txt = sec_txt[d_stems[a][1] - 1 + l_stems_father: d_stems[b][1] - 1] + sec_txt[d_stems[b][2]: d_stems[a][2] - l_stems_father]
            for c in contents_in_txt:
                # 发现杂质直接退出，库变成大写的库。
                if c != "." and c != "&":
                    frag_name_X = 'hybrid_interior_loop'
                    break
                else:
                    frag_name_X = 'interior_loop'
            # frag_name_X = 'interior_loop'
        # print(contents_in_txt)
    elif len(inode._children) >= 2:
        name_node = inode._name
        n_way = len(inode._children) + 1
        lst_node_num = list(range(n_way))
        lst_node_num[0] = inode._name
        for j in range(n_way - 1):
            lst_node_num[j + 1] = inode._children[j]._name
        lst_node_num.sort()
        lst_index = list(range(n_way))
        for inode in range(n_way):
            lst_index[inode] = [j for j, x in enumerate(stempos) if x == lst_node_num[inode]]

        # 区分第一个节点是正规multi/faker_multi
        if lst_node_num[0] != 0:
            # 正常multi
            # 将开头stems对半切开然后放在两头，这样来锁定中间环位置和个数
            num_enter = len(lst_index[0])
            demi_num_enter = int(num_enter / 2)
            lst_index.append(lst_index[0][demi_num_enter:])
            lst_index[0] = lst_index[0][:demi_num_enter]
        elif lst_node_num[0] == 0:
            # faker_multi
            # 直接让首位数组下标变成两头，就可以锁定中间环位置和个数
            lst_index.append([len(stempos)])
            lst_index[0] = [0]
        l_multiloop = []
        for j in range(len(lst_index) - 1):
            l_multiloop.append(lst_index[j + 1][0] - lst_index[j][-1] - 1)
        frag_value_X = l_multiloop
        if name_node != 0:
            frag_name_X = 'multi_loop'
        else:
            # frag_value_X = l_multiloop
            frag_name_X = 'faker_multi_loop'
    frag_value_X = '_'.join([str(ii) for ii in frag_value_X])
    return frag_name_X, frag_value_X, frag_name_Y, frag_value_Y


"""
数字型二级结构表示,注意这里会增加一个stempos[0]=0这个值，这个值很重要，
一个是为了让数组下标和碱基编号对应（没有碱基编号为0的碱基）
二是为了在非闭合茎的情况下，一开始有0值入栈，为了pop(0)而定的
"""


# To_num函数返回（stems_5, stems_long, stems_3, m_kinds, stem_pos）
# To_tree这个函数用来返回d_stems,和order_lt,lst_node,index
def To_tree(l_5, l_long, l_3, m, stempos):
    """
        input:
                stempos:数字形式二级结构
                m:茎种类数
        return:
                这个函数用来返回d_stems,和order_lt(拼装顺序列表),lst_node,index
                # d_stems用字典的形式来表示各个茎(不包括下标为0的虚根)的长度、起始位、结束位(dn.l_long)
                # {1: (2, 2, 43), 2: (3, 5, 19), 3: (2, 9, 16), 4: (3, 23, 41), 5: (3, 27, 35)}
                # {1: (3, 5, 19), 2: (2, 9, 16), 3: (3, 23, 41), 4: (3, 27, 35)}
    """
    order_lt_f = []
    # 节点列表长度m == 多少个茎 + 1(1是因为算上数组下标为0 处 存放一个无效节点)
    m += 1
    # 来存储节点的列表[Node(-1), Node(-1), Node(-1), Node(-1), Node(-1), Node(-1)]
    lst_node_f = [Node(-1) for _ in range(m)]
    # 栈对象s
    s = Stack()
    d_stems_f = dict(enumerate(zip(l_long, l_5, l_3), 1))
    # # todo 20210904 加一个0节点，这里面只存第一个非零下标和最后一个非零下标
    begin = 1
    end = len(stempos) - 1
    d_stems_f.update({0: (0, begin, end)})

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
        lst_node_f[0] = Node(0)
        s.push(0)
        lst_node_f[stempos[j0]] = Node(stempos[j0])
        lst_node_f[0].add_child(lst_node_f[stempos[j0]])
        s.push(stempos[j0])
        # [Node(0), Node(-1), Node(-1), Node(3), Node(-1)]
    else:
        lst_node_f[1] = Node(1)
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
            lst_node_f[num_index] = Node(num_index)
            lst_node_f[k].add_child(lst_node_f[num_index])
            s.push(num_index)
        else:
            s.pop()
        '''step4:每一次都判断一下栈是否为空，空就结束，否则跳转到step3'''
        if s.isEmpty():
            break

    index = 0
    # 通过这一步来区分非闭合茎和闭合茎的下标,非闭合茎有虚根Node(0)所以 index = 0
    for index in range(len(lst_node_f)):
        if lst_node_f[index]._name != -1:
            break

    # 在这里，把茎长度载入每个实例对象的_value值中
    for i in range(1, len(lst_node_f)):
        lst_node_f[i]._value = l_long[i - 1]
    # todo 20210904
    if index == 0:
        lst_node_f[index]._value = 0

    for ch in lst_node_f[index].depth_first():
        order_lt_f.append(ch)

    # print(d_stems)
    # print(lst_node)
    # for i in range(index, len(lst_node)):
    #     print(lst_node[i]._value)

    return order_lt_f, d_stems_f, lst_node_f, index


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

    j = '()'
    num = 1
    # 2021年8月17日 加入环区个数,不算juction
    loop_num = 0
    for sec_dot in imf[0]:
        ii = dn.To_num(sec_dot, j[0], j[1])
        # .((((...[[[[[[.))))..].]].]]].
        # ([2], [4], [19], 1, [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1])
        # ([1, 4, 6], [3, 2, 1], [21, 17, 14], 3, [0, 1, 1, 1, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2, 2, 0, 1, 1, 1, 0])
        print(f'{num}_group')
        print('————————二级数字结构————————')
        print(ii[4])
        print('————————二级树型结构————————')
        order_lt, d_stems, lst_node, index = To_tree(ii[0], ii[1], ii[2], ii[3], ii[4])
        # To_tree这个函数用来返回order_lt, d_stems, lst_node, index
        for i in lst_node[index:]:
            # 分别读取每个节点 和 其子节点
            print(i, end='->')
            print(i._children)
        print('————————片段结构信息————————')
        for i in lst_node[index:]:
            showfragimf(i, d_stems, ii[4])
            # 加上了loop_num 2021年8月17日
            imf_loop, long_loop, imf_stem, long_stem = Bref_Fragimf(i, d_stems, ii[4], sec_dot)
            # if imf_loop.lower() in ['hairpin_loop', 'interior_loop', 'bulge_loop']:
            if "loop" in imf_loop:
                loop_num += 1
            print((imf_loop, long_loop, imf_stem, long_stem))
        print('————————拼装节点顺序————————')
        order_lt.reverse()
        print(order_lt)
        print('————————是否存在侧拼————————')
        print(imf)
        if imf[1] == -1:
            print('不用侧拼')
        else:
            print('需要侧拼')
            print(f'侧拼信息:\nL = {imf[2]}')
            print(f'insert = {imf[3]}')
        print()
        num += 1
        j = '[]'
    print('————————环的数目————————')
    print(loop_num)
