import time
import os
import glob
import shutil
import random
from move_tool import func, func_beside
import multiprocessing
import math
import numpy as np
import BackAA as ba
import Dot_to_num as dn
import parse_mid as pm
import Num_to_tree as nt
import Select_structure as ss


def Combination(input_path, filex_path, filey_path, node_name, n, x_switch=0, y_switch=0):
    """
    input_path 彻底把每一次拼装都分开
    根据提供的A片段的地址和B片段地址,node_name,接口bp数n 来拼装
    并得到以node_name(Node(n))命名的文件夹，里面装着这一步完成后所有拼装出来的结构以{num++}.pdb命名
    加入开关控制是否随机选取片段x_switch ,y_switch
    """
    num = 0
    x_list = glob.glob(filex_path)
    # todo 20220226
    # 判断这个头是不是假结头，如果是
    if "hybrid" in filex_path:
        # 判断全取是否数量够，不够就去正常库里取
        if x_switch > len(x_list):
            rest_num = x_switch - len(x_list)
            filex_path = filex_path.replace("hybrid_", "")
            filex_path = filex_path[:filex_path.rfind("_")] + filex_path[filex_path.rfind("_") + 2:]
            # 看剩下需要的片段  是否 大于变换后的库里的片段
            x_change_list = glob.glob(filex_path)
            if rest_num > len(x_change_list):
                rest_num = len(x_change_list)
            x_list += random.sample(glob.glob(filex_path), rest_num)
    else:
        # 如果不是假借头，正常判断
        if x_switch != 0 and len(x_list) > x_switch:
            # 根据参数x_switch, y_switch 来确定随机取的数目，外部参数不传则全部取
            x_list = random.sample(glob.glob(filex_path), x_switch)

    # y_list = glob.glob(filey_path)
    # if y_switch != 0 and len(y_list) > y_switch:
    #     y_list = random.sample(glob.glob(filey_path), y_switch)
    y_list = glob.glob(filey_path)
    if "hybrid" in filey_path:
        # 判断全取是否数量够，不够就去正常库里取
        if y_switch > len(y_list):
            rest_num = y_switch - len(y_list)
            filey_path = filey_path.replace("hybrid_", "")
            # 看剩下需要的片段  是否 大于变换后的库里的片段
            y_change_list = glob.glob(filey_path)
            if rest_num > len(y_change_list):
                rest_num = len(y_change_list)
            y_list += random.sample(glob.glob(filey_path), rest_num)
    else:
        # 如果不是假借头，正常判断
        if y_switch != 0 and len(y_list) > y_switch:
            # 根据参数x_switch, y_switch 来确定随机取的数目，外部参数不传则全部取
            y_list = random.sample(glob.glob(filey_path), y_switch)

    # 这里的循环xy可以换一下位置，因为Y一般少一点
    for y in y_list:
        for x in x_list:
            num += 1
            # 构建文件夹和文件路径
            try:
                old_file_path = func(input_path, x, y, n)
            except:
                print("error", x)
                print("error", y)

            new_dir_path = node_name
            if not os.path.exists(new_dir_path):
                os.mkdir(new_dir_path)
            new_file_path = new_dir_path + fr'/{num}.pdb'
            # 重命名然后放入以NODE(i)命名的文件夹下
            shutil.copyfile(old_file_path, new_file_path)


def Combination_beside(input_path, filex_path, filey_path, beside_name, insect, long, flag, x_switch=0, y_switch=0):
    """
    def func_beside(X, Y, insect, long, flag=0):
    根据提供的A片段的地址和B片段地址,node_name,接口bp数n 来拼装
    并得到以node_name(Node(n))命名的文件夹，里面装着这一步完成后所有拼装出来的结构以{num++}.pdb命名
    加入开关控制是否随机选取片段x_switch ,y_switch
    """
    num = 0
    # 根据参数x_switch, y_switch 来确定随机取的数目，外部参数不传则全部取
    x_list = glob.glob(filex_path)
    if x_switch != 0 and len(x_list) >= x_switch:
        x_list = random.sample(glob.glob(filex_path), x_switch)
    y_list = glob.glob(filey_path)
    if y_switch != 0 and len(y_list) >= y_switch:
        y_list = random.sample(glob.glob(filey_path), y_switch)

    for x in x_list:
        for y in y_list:
            num += 1
            old_file_path = func_beside(input_path, x, y, insect, long, flag)
            new_dir_path = beside_name
            if not os.path.exists(new_dir_path):
                os.mkdir(new_dir_path)
            new_file_path = new_dir_path + fr'/{num}.pdb'
            # 重命名然后放入以NODE(i)命名的文件夹下
            shutil.copyfile(old_file_path, new_file_path)
            # 超过7000个结构就自动退出
            # if num > 7000:
            #     return


def Drop_line(string, filey_path):
    """
        删除假借茎区侧拼之前的环区，提供假借段点括号字符串，和假借茎的文件位置
        再原文件上修改，修改完后，继续保存到源文件上
    """
    left_num = string.rfind('[') - string.find('[')
    right_num = string.find(']') - string.find('[')
    with open(filey_path, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if int(lines[i][22:26]) == left_num + 1:
                left_index = i
            elif int(lines[i][22:26]) == right_num + 1:
                right_index = i
    with open(filey_path, 'w') as f:
        for line in lines[:left_index + 1]:
            f.write(line)
        for line in lines[right_index - 2:]:
            f.write(line)


def Random_sampling(l_num):
    """

    :param l_num: 环区数目，接口数目
    :return: 返回随机数组
    """
    # 设定值
    key = 30
    # 顶峰
    if l_num < 9:
        max_num = 10000
    elif l_num <= 25:
        max_num = 5000
    else:
        max_num = 2000
    for iii in range(1, 20):
        if (key / iii) ** iii > max_num:
            # 最大顶峰环数
            break
    max_num_loop = iii
    # print(max_num_loop)
    # print(max_num) 59049
    # 当接口太对，整个(30/m)^m函数单调递减，所以设一个最大值，然后平行

    # num_p是片段的概率，3.3意味着更容易取到3，不容易取到4
    if l_num >= max_num_loop:
        num_p = 10 ** (math.log10(max_num) / l_num)
    else:
        num_p = key / l_num
    # print(f"接口数：{l_num}-->片段取值：{num_p}")
    for i in range(1, l_num + 1):
        sum = math.floor(num_p) ** i * math.ceil(num_p) ** (l_num - i)
        if sum < max_num:
            break
    # 向上取整
    # print(math.ceil(num_p))
    # 向下取整
    # print(math.floor(num_p))
    lt = []
    # print(f"取左边值({math.floor(num_p)} ): {i}个")
    lt += [math.floor(num_p)] * i
    j = l_num - i
    # print(f"取右边值({math.ceil(num_p)} ): {j}个")
    lt += [math.ceil(num_p)] * j
    np.random.shuffle(lt)
    # print(lt)
    return lt


def Move_file():
    """
    拼装结束后有很多有用的结果文件，我们将其全部存进BINGO文件价
    """
    Final_path = r'./RESULT'
    if not os.path.exists(Final_path):
        os.mkdir(Final_path)
    if os.path.exists(r'./Energy_out.csv'):
        shutil.move(r'./Energy_out.csv', Final_path)
    if os.path.exists(r'./CG_Result'):
        shutil.move(r'./CG_Result', Final_path)
    if os.path.exists(r'./AA_Result'):
        shutil.move(r'./AA_Result', Final_path)
    if os.path.exists(r'./Select_Result'):
        shutil.move(r'./Select_Result', Final_path)


def Begin_clear():
    """
    再次运行程序之前清扫一下文件里面多余的文件夹，不要的文件夹
    :return: none
    """
    for name in os.listdir():
        if name not in ['cgRNAfrag', 'fragment', 'reconstruction', 'database', 'cgRNASP-Feb', 'data', 'move_tool.py', 'Num_to_tree.py', 'parse_mid.py', 'FebRNA.py', 'cgRNASP-Feb.c', '__pycache__', 'reconstruction.c', 'BackAA.py', 'Dot_to_num.py', 'readme.txt', 'Select_structure.py']:
            try:
                shutil.rmtree(name)
            except NotADirectoryError:
                os.remove(name)


def End_clear(path, num_dir):
    """
    拼装中途结束时清理垃圾

    """
    for iii in range(1, num_dir):
        shutil.rmtree(rf'{path}/{iii}')
    os.remove(rf"{path}/change_b.pdb")
    os.remove(rf'{path}/result.pdb')


def Change_sequence(path, sequence):
    """
    修改最终PDB的序列成用户输入的序列,从后往前填充
    :param sequence: 用户输入序列
    """
    # n_change_rate_lt = []
    for i in os.listdir(rf'{path}/FINAL_Result'):
        with open(rf'{path}/FINAL_Result/{i}', 'r') as f:
            lines = f.readlines()
        with open(rf'{path}/FINAL_Result/{i}', 'w') as f:
            lt = list(range(len(lines)))
            lt.reverse()
            count = 0
            k = len(sequence) - 1
            for ll in range(len(lt)):
                alpha = sequence[k]
                count += 1
                if count % 3 == 0:
                    k -= 1
                if 'HETATM' in lines[lt[ll]]:
                    lines[lt[ll]] = lines[lt[ll]].replace('HETATM', 'ATOM  ', 1)
                lines[lt[ll]] = lines[lt[ll]][:17] + f'  {alpha}' + lines[lt[ll]][20:]

            for line in lines:
                f.write(line)


def Delet_Andsymbol(path):
    """
    删除文件中序列是&的行
    """
    for i in os.listdir(rf'{path}/FINAL_Result'):
        with open(rf'{path}/FINAL_Result/{i}', 'r') as f:
            lines = f.readlines()
        with open(rf'{path}/FINAL_Result/{i}', 'w') as f:
            for line in lines:
                if '&' in line[17:20]:
                    continue
                f.write(line)
    # 删完之后还需要更新序列


def Change_base(path):
    """根据序列修改碱基N的类型"""
    for file in os.listdir(path):
        file_path = rf"./{path}/{file}"
        with open(file_path, 'r') as f:
            lines = f.readlines()
        with open(file_path, 'w') as f:
            for line in lines:
                if "N" in line[13:16]:
                    if line[19:20] == "G" or line[19:20] == "A":
                        line = line.replace(line[13:16], 'N9 ', 1)
                    elif line[19:20] == "C" or line[19:20] == "U":
                        line = line.replace(line[13:16], 'N1 ', 1)
                f.write(line)


def Add_Chain(path):
    """添加链的信息"""
    for file in os.listdir(path):
        file_path = rf"./{path}/{file}"
        with open(file_path, 'r') as f:
            lines = f.readlines()
        with open(file_path, 'w') as f:
            for line in lines:
                line = line[:21] + "A" + line[22:]
                f.write(line)


def Check_input(line_words):
    '''
    检查输入，不符合规则的输入会让用户重新输入
    :param line_words:
    :return: 返回input_list, flag, L, insert, L_loop
            (['((((((....).).)))).', '.[[[........]]]'], 1, 3, 6, 2)
    '''
    while True:
        if line_words.count('(') == line_words.count(')') and line_words.count('[') == line_words.count(']'):
            # if line_words.count('(') == line_words.count(')'):
            # input_list, flag, L, insert, L_loop
            # (['((((((....).).)))).', '.[[[........]]]'], 1, 3, 6, 2)
            break
        else:
            print('Error ,input again')
            line_words = input('请输入二级结构（点括号形式）：')
            # line_words = line_words.replace('{', '(')
            # line_words = line_words.replace('}', ')')
    return pm.parse_mid(line_words)


def check_bpnum_dir(path, num, type, long):
    """
    在有n_bp的库路径下，加一个判断，如果这个长度的片段在这个nbp下找不到，就只能降一档去找
    :return: 最终确定的bp数目
    """
    while True:
        # 0bp直接退出
        if num == 0:
            break
        elif (os.path.exists(path + fr'/{num}_bp/{type}/{long}') and len(
                glob.glob(path + fr'/{num}_bp/{type}/{long}/*.pdb')) == 0) or \
                (not os.path.exists(path + fr'/{num}_bp/{type}/{long}')):
            num -= 1
            # 减一个nbp后重新开始头尾长度筛选
        else:
            break
    return num


def Assembly_func(input_path_f, sequence_txt_f, txt_f, path_f, fix_bp_switch):
    """
    拼装函数
    :param sequence_txt_f: 二级结构序列形式
    :param input_path_f 存放拼装结构
    :param txt_f:输入的二级点括号结构
    :param path_f: 数据库的地址
    :param fix_bp_switch: 用来设定是否固定bp为1，flag-0自动，-1固定1bp
    """
    # 用来判定这个结构是不是有FAKER_MULTI,来决定如何保留头尾序列
    sequence_flag = 0
    # Begin_clear(input_path_f)
    stems_num = []  # 用来后续比较接口bp数，自动比对的参数
    # flag_keep = 'f'  # 这个开关 用来确定此时结构里包不包含大主体(即需不需要保留全部结构进行下一步)
    # (['((((((....).).)))).', '.[[[........]]]'], 1, 3, 6, 2) input_list, flag, L, insert, L_loop
    # print(imf)
    imf = Check_input(txt_f)
    #  5分枝环成倍标志
    global junction_num
    '''算环区个数'''
    loop_num = 0
    j = '()'
    for sec_dot in imf[0]:
        ii = dn.To_num(sec_dot, j[0], j[1])
        order_lt, d_stems, lst_node, index = nt.To_tree(ii[0], ii[1], ii[2], ii[3], ii[4])
        order_lt.reverse()
        for iii in order_lt:
            # Y代表着stems
            type_x, long_x, type_y, long_y = nt.Bref_Fragimf(iii, d_stems, ii[4], sec_dot)
            if "loop" in type_x:
                loop_num += 1
        j = '[]'

    """根据接口数确定随机选片段的数组"""
    '''有几个环拼几次，假结中因为侧发卡环固定数字1，并不用加一次'''

    mm = Random_sampling(loop_num)
    # print(mm)

    # 用来判定是否需要侧拼，并且确定文件夹名字
    num_result = 1
    '''开始组装'''
    j = '()'
    for sec_dot in imf[0]:
        ii = dn.To_num(sec_dot, j[0], j[1])
        order_lt, d_stems, lst_node, index = nt.To_tree(ii[0], ii[1], ii[2], ii[3], ii[4])
        order_lt.reverse()
        dir_path = fr'{input_path_f}/{num_result}'
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        '''按照 order_lt 进行的拼装顺序'''
        for iii in order_lt:
            # Y代表着stems
            type_x, long_x, type_y, long_y = nt.Bref_Fragimf(iii, d_stems, ii[4], sec_dot)
            # 没有特殊情况，取标准碱基对1个
            type_y = 'stems_standard'
            if loop_num <= 2:
                # 小于2个环的结构stems取所有
                type_y = 'stems_all'

            # 临时结构存储位置，会根据片段种类不同而改变
            dir_name = dir_path + fr'/{iii}_0'
            if True:
                if type_x in ['hairpin_loop', 'hybrid_hairpin_loop']:
                    '''判断接口的碱基对数目'''
                    # fix_bp_switch外部传参，用来选择是否固定接口BP数，0为自动，否则为固定值1
                    if fix_bp_switch == 0:
                        if long_y >= 3:
                            n = 3
                        else:
                            n = long_y
                    else:
                        n = 1
                    """数据库中查找是否存在所需片段"""
                    # 在n_bp的库路径下，如果这个长度的片段在这个nbp下找不到，就只能n-1去找
                    temp_num = n
                    n = check_bpnum_dir(path_f, n, type_x, long_x)
                    # 如果只是因为杂环中没有结构，那就去纯环结构中找。
                    if n == 0 and type_x == "hybrid_hairpin_loop":
                        # 拼的时候文件夹名称也要换了
                        type_x = "hairpin_loop"
                        long_x = long_x.split("_")[0]
                        n = temp_num
                        n = check_bpnum_dir(path_f, n, type_x, long_x)
                    # 如果最终还是没有结构，就返回无模板。
                    if n == 0:
                        print(f"Missing template :{type_x}->{long_x}")
                        exit()
                    '''面对中括号的发卡环，即假结侧环我们只取一个，因为后面也是要删除的'''
                    if j == '[]':
                        x_boot = 1
                        type_x = "hairpin_loop"
                        long_x = long_x.split("_")[0]
                    elif type_x == "hybrid_hairpin_loop":
                        x_boot = max(mm)
                        mm.remove(x_boot)
                    else:
                        # 20220303
                        # x_boot = mm.pop()
                        x_boot = min(mm)
                        mm.remove(x_boot)
                    y_boot = 0
                    # if loop_num <= 2:
                    #     # 小于2个环的结构stems取所有
                    #     type_y = 'stems_all'
                    file_x_path = path_f + fr'/{n}_bp/{type_x}/{long_x}/*.pdb'
                    file_y_path = path_f + fr'/{type_y}/{long_y}/*.pdb'
                    # 针对最后一步把文件名变成FINAL
                    if iii == order_lt[-1]:
                        dir_name = dir_path + fr'/FINAL_Result'
                    Combination(input_path_f, file_x_path, file_y_path, dir_name, n, x_boot, y_boot)
                    stems_num.append(long_y)
                elif type_x in ['bulge_loop', 'interior_loop', 'hybrid_bulge_loop', 'hybrid_interior_loop']:
                    child_name = iii._children  # [Node(3)]
                    # 'bulge_loop', 'interior_loop'只用分两次拼
                    # 1.确定接口取几个
                    if fix_bp_switch == 0:
                        min_num = min(long_y, stems_num[-1])
                        if min_num > 3:
                            n = 3
                        else:
                            n = min_num
                    else:
                        n = 1
                    # 20220303
                    # 片段选取数目,因为这里面右两个循环，不然多POP一次
                    # num_part = mm.pop()
                    num_part = min(mm)
                    mm.remove(num_part)
                    # 2.开始拼接
                    for m in range(2):
                        if m == 0:
                            # 中间的环，需要用两步来拼，第一步拼bulge_loop/interior_loop，生成的结构放在NODE(i)_1文件夹下面
                            file_x_path = dir_path + fr'/{child_name[0]}_0/*.pdb'
                            temp_num = n
                            """20220223"""
                            n = check_bpnum_dir(path_f, n, type_x, long_x)
                            # 如果只是因为杂环中没有结构，那就去存环结构中找。
                            if n == 0 and type_x in ['hybrid_bulge_loop', 'hybrid_interior_loop']:
                                # 拼的时候文件夹名称也要换了
                                type_x = type_x.split('_')[1] + '_' + type_x.split('_')[2]
                                n = temp_num
                                n = check_bpnum_dir(path_f, n, type_x, long_x)
                            # 如果最终还是没有结构，就返回无模板。
                            if n == 0:
                                print(f"Missing template :{type_x}->{long_x}")
                                exit()
                            """"""
                            file_y_path = path_f + fr'/{n}_bp/{type_x}/{long_x}/*.pdb'
                        else:
                            # 第二部，把第一步得到的NODE(i)_1文件夹下面的东西拿出来和stems拼，然后放在NODE(i)文件夹下面,最后一定要放到节点名的文件夹下
                            file_x_path = dir_name + r'/*.pdb'
                            file_y_path = path_f + fr'/{type_y}/{long_y}/*.pdb'
                        dir_name = dir_path + fr'/{iii}_{1 - m}'
                        # 针对拼装的最后一模块里面的拼装最后一步把文件名变成FINAL
                        if iii == order_lt[-1] and m == 1:
                            dir_name = dir_path + fr'/FINAL_Result'
                        # 随机选取片段数目
                        x_boot = 0
                        y_boot = num_part
                        Combination(input_path_f, file_x_path, file_y_path, dir_name, n, x_boot, y_boot)
                    stems_num[-1] = long_y
                elif type_x == 'multi_loop':
                    # 就算不用到mm中的值，也要pop一次，免得错误
                    # mm.pop()
                    # todo
                    if len(long_x.split("_")) == 5:
                        junction_num = 5
                    mm.remove(max(mm))
                    child_name_list = iii._children
                    # [Node(4), Node(2)]
                    # 因为是从右子树开始读入，所以拼装顺序应该是反过来
                    child_name_list.reverse()
                    # [Node(2), Node(4)]
                    n = min(min(stems_num), long_y)
                    if fix_bp_switch == 0:
                        if n > 3:
                            n = 3
                    else:
                        n = 1
                    # 此时这个mutiloop，stems也拼上。则需要拼n次，
                    for m in range(len(child_name_list)):
                        file_x_path = dir_path + fr'/{child_name_list[m]}_0/*.pdb'
                        if m == 0:
                            n = check_bpnum_dir(path_f, n, type_x, long_x)
                            if n == 0:
                                print(f"Missing template :{type_x}->{long_x}")
                                exit()
                            file_y_path = path_f + fr'/{n}_bp/{type_x}/{long_x}/*.pdb'
                        else:
                            file_y_path = dir_name + r'/*.pdb'
                        # 这里是3-way-junction ,最后一步不放外面了，所以只用3-1个额外文件夹
                        dir_name = dir_path + fr'/{iii}_{len(child_name_list) - m}'

                        x_boot = 0
                        y_boot = 0

                        Combination(input_path_f, file_x_path, file_y_path, dir_name, n, x_boot, y_boot)
                    file_x_path = dir_path + fr'/{iii}_1/*.pdb'
                    file_y_path = path_f + fr'/{type_y}/{long_y}/*.pdb'
                    dir_name = dir_path + fr'/{iii}_0'

                    # 针对最后一步把文件名变成FINAL
                    if iii == order_lt[-1]:
                        dir_name = dir_path + fr'/FINAL_Result'

                    Combination(input_path_f, file_x_path, file_y_path, dir_name, n)
                    stems_num.clear()
                    stems_num.append(long_y)
                    # todo 2021年8月20日 只要有junction，flag_keep 就等于't'
                    flag_keep = 't'
                elif type_x == 'faker_multi_loop':
                    # 就算不用到mm中的值，也要pop一次，免得错误
                    # mm.pop()
                    # todo 20220302 15:55
                    mm.remove(max(mm))
                    child_name_list = iii._children
                    child_name_list.reverse()
                    # [Node(2), Node(4)]
                    n = min(stems_num)
                    if fix_bp_switch == 0:
                        if n > 3:
                            n = 3
                    else:
                        n = 1
                    # 此时这个mutiloop，stems也拼上。则需要拼n次，
                    for m in range(len(child_name_list)):
                        file_x_path = dir_path + fr'/{child_name_list[m]}_0/*.pdb'
                        if m == 0:
                            long_x_copy = long_x
                            flag_trip = 1
                            num = n
                            while True:
                                # 没找到
                                if (os.path.exists(path_f + fr'/{n}_bp/{type_x}/{long_x_copy}') and len(
                                        glob.glob(path_f + fr'/{n}_bp/{type_x}/{long_x_copy}/*.pdb')) == 0) or \
                                        (not os.path.exists(path_f + fr'/{n}_bp/{type_x}/{long_x_copy}')):
                                    if flag_trip == 1:
                                        n -= 1
                                        if n == 0:
                                            flag_trip = 0
                                            n = num
                                    else:
                                        # 看头尾长度是否为0
                                        long_lt = long_x_copy.split('_')
                                        if long_lt[0] != "0":
                                            long_lt[0] = str(int(long_lt[0]) - 1)
                                            long_x_copy = "_".join(long_lt)
                                        elif long_lt[-1] != "0":
                                            long_lt[-1] = str(int(long_lt[-1]) - 1)
                                            long_x_copy = "_".join(long_lt)
                                        else:
                                            n -= 1
                                            # 减一个nbp后重新开始头尾长度筛选
                                            long_x_copy = long_x
                                            if n == 0:
                                                print(f"Missing template :{type_x}->{long_x}")
                                                exit()
                                # 找到了
                                else:
                                    break
                            # 告知一下最后替代的模板是多少
                            # print(f"{n}bp+" + long_x_copy)
                            sequence_flag = 1
                            if imf[1] == -1:
                                # 无假结
                                sequence_begin = int(long_x.split('_')[0]) - int(long_x_copy.split('_')[0])
                                sequence_end = len(sequence_txt_f) - (int(long_x.split('_')[2]) - int(long_x_copy.split('_')[2]))
                            else:
                                left_small = txt_f.find('(')
                                left_mid = txt_f.find('[')
                                right_small = txt_f.rfind(')')
                                right_mid = txt_f.rfind(']')
                                if 0 <= left_mid < left_small:
                                    # 假结在头部
                                    sequence_begin = left_mid
                                    sequence_end = len(sequence_txt_f) - (int(long_x.split('_')[2]) - int(long_x_copy.split('_')[2]))
                                elif right_mid > right_small:
                                    sequence_begin = int(long_x.split('_')[0]) - int(long_x_copy.split('_')[0])
                                    sequence_end = right_mid + 1
                            file_y_path = path_f + fr'/{n}_bp/{type_x}/{long_x_copy}/*.pdb'
                        else:
                            file_y_path = dir_name + r'/*.pdb'
                        # 这里是3-way-junction ,但是faker_multi_loop无结尾stems，所以只用3-1-1个 额外 文件夹
                        dir_name = dir_path + fr'/{iii}_{len(child_name_list) - m - 1}'

                        # 而且只要是有faker_multi_loop，那最后一步拼装，一定是结束
                        if len(child_name_list) - m - 1 == 0:
                            dir_name = dir_path + fr'/FINAL_Result'

                        # todo 2022 02 28
                        # x_boot = Random_sampling(loop_num)
                        # if flag_keep == 't':
                        #     x_boot = 0
                        x_boot = 0
                        y_boot = 0
                        Combination(input_path_f, file_x_path, file_y_path, dir_name, n, x_boot, y_boot)

        num_result += 1
        j = '[]'

    '''侧拼环节'''
    if imf[1] == -1:
        # imf = (['((.(((.((....)))))...(((.(((...)))...)))))'], -1, -1, -1)  input_list, flag, L, insert
        folder1 = rf'{input_path_f}/{num_result - 1}/FINAL_Result'
        folder2 = rf'{input_path_f}/FINAL_Result'
        shutil.copytree(folder1, folder2)
    else:
        # imf = (['((((((.......))))))', '((((((...............))))))'], 0, 6, 7, 9)
        # 侧边拼
        file_x_path = fr'{input_path_f}/1/FINAL_Result/*.pdb'
        file_y_path = fr'{input_path_f}/2/FINAL_Result/*.pdb'
        # 修改f_Y，删除环区之后再拼
        for y in glob.glob(file_y_path):
            Drop_line(imf[0][-1], y)
        dir_name = fr'{input_path_f}/Beside_Final_Result'
        x_boot = 0
        y_boot = 0
        Combination_beside(input_path_f, file_x_path, file_y_path, dir_name, imf[3], imf[2], imf[1], x_boot, y_boot)

        # 收尾拼上假借环
        file_x_path = path_f + fr'/1_bp/pseudoknot_loop/{imf[4]}/*.pdb'
        file_y_path = fr'{input_path_f}/Beside_Final_Result/*.pdb'
        dir_name = fr'{input_path_f}/FINAL_Result'
        x_boot = 0
        y_boot = 0
        # 用来占位
        # num_part = mm.pop()
        # todo 20220302 15:55
        num_part = max(mm)
        mm.remove(num_part)
        # pseudoknot_loop没有所需要长度就去hairpinloop里面找mm个
        if len(glob.glob(path_f + fr'/1_bp/pseudoknot_loop/{imf[4]}/*.pdb')) == 0:
            file_x_path = path_f + fr'/1_bp/hairpin_loop/{imf[4]}/*.pdb'
            x_boot = num_part
        Combination(input_path_f, file_x_path, file_y_path, dir_name, 1, x_boot, y_boot)
        shutil.rmtree(rf'{input_path_f}/Beside_Final_Result')
    # print('Finish [assembly] in "./FINAL_Result"')
    # return num_result
    End_clear(input_path_f, num_result)

    if sequence_flag == 0:
        # 没有faker_multi
        for index_begin in range(len(txt_f)):
            if txt_f[index_begin] == "(" or txt_f[index_begin] == "[":
                break
        for index_end in range(1, len(txt_f) + 1):
            if txt_f[-index_end] == ")" or txt_f[-index_end] == "]":
                break
        sequence_txt_f = sequence_txt_f[index_begin: len(txt_f) - index_end + 1]
    else:
        sequence_txt_f = sequence_txt_f[sequence_begin: sequence_end]
    # 修改序列 因为有一个FAKER，所以序列从后往前更新
    Change_sequence(input_path_f, sequence_txt_f)
    Delet_Andsymbol(input_path_f)


def delete_foils():
    # 删除DIR垃圾文件
    for fois_dir in os.listdir():
        if "_foils" in fois_dir:
            dir_path_begin = rf"./{fois_dir}"
            if os.path.exists(dir_path_begin):
                shutil.rmtree(dir_path_begin)
    # for i_begin in range(1, 4):
        # dir_path_begin = rf"./{i_begin}_foils"
        # if os.path.exists(dir_path_begin):
        #     shutil.rmtree(dir_path_begin)


if __name__ == '__main__':
    # 先清空文件夹，并建文件夹，存放每轮拼装得文件夹，共三轮
    Begin_clear()
    sequence_txt = input('Sequence:').upper()
    txt = input('Secondary Structure:')
    while True:
        select_num = input('Seleted Num(0=all):')
        if select_num.isdigit():
            select_num = int(select_num)
            break
        else:
            print("Input Error! Please Input again")
            continue
    while True:
        flag_aa = input("All-atom rebuilding?(y/n):").upper().strip()
        if flag_aa in "YN":
            break
        else:
            print("Input Error! Please Input again")
            continue

    time_start = time.time()
    # 数据库路径,当前文件夹下的database ，到时候和程序一起打包
    path = r'./database'
    # # 并行文件夹1_fois,2_fois,3fois
    # for ii_begin in range(1, 4):
    #     dir_path_begin = rf"./{ii_begin}_foils"
    #     os.mkdir(dir_path_begin)
    flag = 0  # 用来设定是否固定bp为1，flag-0自动，-1固定1bp
    junction_num = 0
    # todo 先弄一次
    dir_path_begin = rf"./1_foils"
    os.mkdir(dir_path_begin)
    Assembly_func(fr"./1_foils", sequence_txt, txt, path, flag)

    if junction_num == 5:
        num_flag = 6
    else:
        num_flag = 4

    # todo 建并行文件夹
    for i_begin in range(2, num_flag):
        dir_path_begin = rf"./{i_begin}_foils"
        os.mkdir(dir_path_begin)

    # todo 多进程拼装，同时把文件整合 和 更新序列 整理放在了拼装程序里。
    if num_flag == 6:
        p1 = multiprocessing.Process(target=Assembly_func, args=(fr"./2_foils", sequence_txt, txt, path, flag))
        p2 = multiprocessing.Process(target=Assembly_func, args=(fr"./3_foils", sequence_txt, txt, path, flag))
        p3 = multiprocessing.Process(target=Assembly_func, args=(fr"./4_foils", sequence_txt, txt, path, flag))
        p4 = multiprocessing.Process(target=Assembly_func, args=(fr"./5_foils", sequence_txt, txt, path, flag))
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p1.join()
        p2.join()
        p3.join()
        p4.join()
    else:
        p1 = multiprocessing.Process(target=Assembly_func, args=(fr"./2_foils", sequence_txt, txt, path, flag))
        p2 = multiprocessing.Process(target=Assembly_func, args=(fr"./3_foils", sequence_txt, txt, path, flag))
        p1.start()
        p2.start()
        p1.join()
        p2.join()

    # 文件合并,注意重名
    finish_path = r"./FINAL_Result"
    if not os.path.exists(finish_path):
        os.mkdir(finish_path)
    number = 1
    for i in range(1, num_flag):
        dir_path = rf"./{i}_foils/FINAL_Result"
        lt = os.listdir(dir_path)
        for j in lt:
            shutil.move(fr"./{i}_foils/FINAL_Result/{j}", rf"./FINAL_Result/{number}.pdb")
            number += 1
    # 多进程拼装，同时把文件整合 和 更新序列 整理放在了拼装程序里。
    # p1 = multiprocessing.Process(target=Assembly_func, args=(fr"./1_foils", sequence_txt, txt, path, flag))
    # p2 = multiprocessing.Process(target=Assembly_func, args=(fr"./2_foils", sequence_txt, txt, path, flag))
    # p3 = multiprocessing.Process(target=Assembly_func, args=(fr"./3_foils", sequence_txt, txt, path, flag))
    # p1.start()
    # p2.start()
    # p3.start()
    # p1.join()
    # p2.join()
    # p3.join()

    # # 文件合并,注意重名
    # finish_path = r"./FINAL_Result"
    # if not os.path.exists(finish_path):
    #     os.mkdir(finish_path)
    # number = 1
    # for i in range(1, 4):
    #     dir_path = rf"./{i}_foils/FINAL_Result"
    #     lt = os.listdir(dir_path)
    #     for j in lt:
    #         shutil.move(fr"./{i}_foils/FINAL_Result/{j}", rf"./FINAL_Result/{number}.pdb")
    #         number += 1

    # 构象总数
    Total_num = number - 1
    # print(Total_num) 
    # 根据序列修改碱基N的类型
    Change_base(finish_path)
    Add_Chain(finish_path)
    os.rename(finish_path, "./CG_Result")
    # time_end = time.time()
    # 统计势能
    if select_num == 0:
        print("SELETED ALL RESULT")
    else:
        ss.Select_structure(Total_num, select_num)
    # 全原子还原
    if flag_aa in "Y":
        # 全原子还原
        # time_start = time.time()
        if os.path.exists(r"./AA_Result"):
            shutil.rmtree(r"./AA_Result")
        os.mkdir(r"./AA_Result")
        if select_num == 0:
            select_dir = r"CG_Result"
        else:
            select_dir = r"Select_Result"
        for cg_file in os.listdir(select_dir):
            file_path = fr'{select_dir}/{cg_file}'
            ba.cg_to_aa(file_path)
            top_name = cg_file.split("_")[-1].split(".")[0]
            shutil.move(rf'./AA_Result.pdb', rf'./AA_Result/{top_name}_Allatom.pdb')
        time_end = time.time()
        print("Finish in folder ./RESULT")
        print(f'    Running time :{time_end - time_start:.3f}s')
        # print(f'[Rebuilding] takes {time_end - time_start:.3f}s')
    else:
        time_end = time.time()
        print("Finish in folder ./RESULT")
        print(f'    Running time :{time_end - time_start:.3f}s')
        delete_foils()
        Move_file()
        exit()
    # 删除垃圾文件
    delete_foils()
    # 移动所有的结果文件到一个文件夹下
    Move_file()
