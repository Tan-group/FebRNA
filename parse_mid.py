# .((((...[[[[[[.))))..].]].]]].
# .[[[..((((((]]].).).)))).
def match_func(in_list, market_a, market_b, flag_f, market_begin):
    """
    判断括号是否配对函数
    :param in_list: 带符号下标的元组数组
    :param market_a: 起符号类型，根据头尾假结的不容而不同
    :param market_b: 起符号的对应符号
    :param flag_f: 判断头尾假结类型
    :param market_begin: 截断符号位置
    :return:lt 数字下标，用来存放需要的符号下标。除了数组里面的下标，其余的符号只要不符合规定都进行转换
    """
    # 括号标志
    marks = {']': '[', '[': ']'}
    # 空栈
    stack = []
    # 数字下标，用来存放需要的符号下标。除了数组里面的下标，其余的符号只要不符合规定都进行转换
    lt = []
    if flag_f == 0:
        in_list.reverse()
    for tup in in_list:
        if tup[1] == market_a:
            stack.append(tup)
            # lt.append(tup[0])
        elif tup[1] == market_b:
            if stack and stack[-1][1] == marks[market_b]:
                lt.append(tup[0])
                # stack.pop()
                lt.append(stack.pop()[0])
            if not stack:
                break
    lt.sort()
    if flag_f == 0:
        lt.reverse()
    # print(lt)
    # lt得到的是一组
    # [[[((([.((]]]][)).(((]))).)))
    # [1, 2, 3, 7, 11, 12, 13, 14]
    # .(((.(((..[))).(((]...))).(((.[.[[[))).))]).]]].
    # [47, 46, 45, 42, 35, 34, 33, 31]
    # 要想办法丢掉7 和11,因为我只要保留尾端假结，其余的假结全部转换成#
    ii = 0
    for ii in range(len(lt)):
        # 如果是 头假结情况
        if flag_f == 1 and lt[ii] > market_begin + 1:
            break
        # 如果是 尾假结情况
        elif flag_f == 0 and lt[ii] < market_begin + 1:
            break
    lt = lt[:ii] + lt[-ii:]
    return lt


# def Get_Mid(mid_input_txt):


def parse_mid(input_str):
    """
        用来鉴别用户输入是否存在假结，用于判断是否进入假结拼装程序
        分析二级结构
        返回input_list, flag, L, insert, L_loop假结长度
    """
    flag = L = insert = L_loop = -1
    l_small = input_str.find('(')
    l_mid = input_str.find('[')
    r_small = input_str.rfind(')')
    r_mid = input_str.rfind(']')
    # print(l_small,l_mid,r_small,r_mid)
    ls = list(enumerate(input_str, 1))
    # 放要保留的假结下标,后续除了这几个下标，其余的位置除了点括号都变成
    index_id = []
    # 后续划分二级结构的标志
    small_begin = small_end = mid_begin = mid_end = 0
    left_s = right_s = ''

    # (1)假结在头部:.[[[(((.((]]][)).(((]))).)))..
    if 0 <= l_mid < l_small:
        # print(l_small)
        # 假结在头部信号
        flag = 1
        index_id = match_func(ls, '[', ']', flag, l_small)
        small_begin = l_small
        small_end = len(input_str) + 1
        mid_end = index_id[-1]
        left_s = '('
        right_s = '['

    # (2)假结在尾部:.(((.(((..[))).(((]...))).(((..[[[))).))).]]].
    elif r_mid > r_small:
        # 假结在尾部信号
        flag = 0
        index_id = match_func(ls, ']', '[', flag, r_small)
        small_end = r_small + 1
        mid_begin = index_id[-1] - 1
        mid_end = len(input_str) + 1
        left_s = ']'
        right_s = ')'
    # (3)假借在中间===无假结一个情况。就是index_id为空，没什么要保留的
    # print(index_id)

    # todo 把下面变成函数
    # 除了index_id 里面的下标字符保留，其余除了点括号字符全变成#
    for j in range(len(input_str)):
        if j + 1 in index_id:
            continue
        else:
            if input_str[j] not in ".()&":
                input_str = input_str[:j] + "#" + input_str[j + 1:]

    # print(input_str)
    # 存放输入，有假结就分解存放，没有就原样
    div_input = []
    # 如果有假结存在拼装
    if index_id:
        # 小括号片段
        small_input = input_str[small_begin:small_end]
        div_input.append(small_input)
        # 中括号片段
        mid_input = input_str[mid_begin : mid_end]
        div_input.append(mid_input)
        # 插入点
        insert = max(small_input.find(']'), small_input.find('['))
        # 假结在括号里面的茎秆长度
        L = abs(index_id[-1] - index_id[len(index_id) // 2]) + 1
        """
            可改进
            假结环长度
            这里很巧妙，要能兼顾到[[[..(((..))).(((]]])))这种假借id:2n8v/4jf2，所以分两部：
            1.先把中括号中间，配对的小括号转变成中括号
            2.用指针，在中括号二级结构中找(或),到前面或后面,非.处有几个点
            但拼装方法也需要改一下，直接双侧拼
        """
        # L_loop = Get_Mid(mid_input)
        L_loop = abs(mid_input.find(left_s) - mid_input.rfind(right_s)) - 1

    else:  # 无假结存在
        flag = -1
        # 小括号片段
        div_input.append(input_str)

    # print("二级结构拆分后：",div_input)
    # print("假结类型(1头/0尾/-1无假结)：", flag)
    # print("假结在括号里面的茎秆长度", L)
    # print("插入点在小括号形式上的：", insert)
    # print("假结环长度：", L_loop)

    return div_input, flag, L, insert, L_loop


if __name__ == '__main__':
    txt = input('请输入二级结构（点括号形式）：')
    while True:
        if txt.count('(') == txt.count(')') and txt.count('[') == txt.count(']'):
            print(parse_mid(txt))
            break
            # (((...)))[[..(((]]..)).).
        else:
            print('Error ,input again')
            txt = input('请输入二级结构（点括号形式）：')
