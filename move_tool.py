#!/bin/python3

# -*- coding: utf-8 -*-

__doc__ = """
拼装程序，用于对接拼装和侧拼函数的输出
"""

__version__ = "1.0"

import copy
import sys
import numpy as np

def rmsd(V, W):
    """
    Calculate Rmsd from two sets of vectors V and W.

    Parameters
    ----------
    V : array
        (N,D) matrix, where N is points and D is dimension.(N,D)矩阵，其中N为点，D为维数。
    W : array
        (N,D) matrix,  where N is points and D is dimension.

    Returns
    -------
    rmsd : float
        Root-mean-square deviation between the two vectors向量
    """
    diff = np.array(V) - np.array(W)
    N = len(V)
    return np.sqrt((diff * diff).sum() / N)


def kabsch_rmsd(P, Q, translate=False):
    """
    将矩阵P旋转到Q

    Parameters
    ----------
    P : array
        (N,D) matrix, where N is points and D is dimension.
    Q : array
        (N,D) matrix, where N is points and D is dimension.
    translate : bool
        Use centroids to translate vector P and Q unto each other.使用质心将向量P和Q相互转换。

    Returns
    -------
    rmsd : float
        root-mean squared deviation
    """

    if translate:
        Q = Q - centroid(Q)  # 质心
        P = P - centroid(P)

    P = kabsch_rotate(P, Q)
    return rmsd(P, Q)


def centroid(X):
    """
    质心是从向量集X出发，在所有坐标方向上所有点的平均位置。

    C = sum(X)/len(X)

    Parameters
    ----------
    X : array
        (N,D) matrix, where N is points and D is dimension.

    Returns
    -------
    C : array
        centroid
    """
    C = X.mean(axis=0)  # 计算每一列的均值
    return C


def kabsch_rotate(P, Q):
    """
    Rotate matrix P unto matrix Q using Kabsch algorithm.

    Parameters
    ----------
    P : array
        (N,D) matrix, where N is points and D is dimension.
    Q : array
        (N,D) matrix, where N is points and D is dimension.

    Returns
    -------
    P : array
        (N,D) matrix, where N is points and D is dimension,
        rotated

    """
    U = kabsch(P, Q)

    # Rotate P
    # np.dot()矩阵乘法，让旋转矩阵U右乘矩阵
    P = np.dot(P, U)
    return P


def kabsch(P, Q):
    """
    Using the Kabsch algorithm with two sets of paired point P and Q, centered
    around the centroid. Each vector set is represented as an NxD
    matrix, where D is the the dimension of the space.
    The algorithm works in three steps:
    - a centroid translation of P and Q (assumed done before this function
      call)
    - the computation of a covariance matrix C
    - computation of the optimal rotation matrix U

    - P和Q的质心平移(假设在这个函数调用之前完成)
    -计算协方差矩阵C
    -计算最佳旋转矩阵U

    For more info see http://en.wikipedia.org/wiki/Kabsch_algorithm
    Parameters
    ----------
    P : array
        (N,D) matrix, where N is points and D is dimension.
    Q : array
        (N,D) matrix, where N is points and D is dimension.
    Returns
    -------
    U : matrix
        Rotation matrix (D,D)
    """

    # Computation of the covariance matrix
    # 协方差矩阵的计算
    # np.transpose（）求转置
    C = np.dot(np.transpose(P), Q)
    # 计算最佳旋转矩阵
    # 这可以使用奇异值分解(SVD)
    # 来实现。
    # 通过det(V) * (W)
    # 的符号来决定我们是否需要修正我们的旋转矩阵以确保一个右手坐标系。最后计算出最优旋转矩阵U
    # Computation of the optimal rotation matrix
    # This can be done using singular value decomposition (SVD)
    # Getting the sign of the det(V)*(W) to decide
    # whether we need to correct our rotation matrix to ensure a
    # right-handed coordinate system.
    # And finally calculating the optimal rotation matrix U
    # see http://en.wikipedia.org/wiki/Kabsch_algorithm
    V, S, W = np.linalg.svd(C)
    d = (np.linalg.det(V) * np.linalg.det(W)) < 0.0

    if d:
        S[-1] = -S[-1]
        V[:, -1] = -V[:, -1]

    # Create Rotation matrix U
    U = np.dot(V, W)

    return U


def change_coordinates_Bpdb(filename_Y, changefile_Y, V, decimals=3):
    """
    将旋转平移完成后的  坐标V矩阵   写入到   PDB格式 (即有坐标信息又有其余的信息) 的文件中去，N行D列，即pdb片段里面N个原子
    """
    N, D = V.shape
    fmt = ("{:8." + str(decimals) + "f}") * 3
    with open(filename_Y, "r") as f:
        lines = f.readlines()
    with open(changefile_Y, 'w') as f:
        for i in range(N):
            # 把原来片段的X Y Z 坐标修改后写入修改的文件里面
            # f.write(lines[i].replace(lines[i][30:-2], fmt.format(V[i, 0], V[i, 1], V[i, 2])))
            lines[i] = lines[i][:30] + fmt.format(V[i, 0], V[i, 1], V[i, 2]) + lines[i][-2:]
            f.write(lines[i])


def assemble(filename_X, changefile_Y, resultname, inf, N):
    """
    将旋转平移后得到的文件 和 原来没有动的文件组合，和成一个RNA结构PDB文件
    """
    '''可以看一下内置模块fileinput'''
    # fileinput.input是最重要的函数，它返回一个迭代器对象，如果要处理多个文件，可以向这个函数提供一个或多个文件名。
    # 还可将参数inplace设置为True（inplace=True），对于你访问的每一行，都需打印出替代内容，这些内容将被写回到当前输入文件中，此时可选参数backup用于给从原始文件创建的备份文件指定扩展名。

    # fileinput.input (files='filename', inplace=False, backup='', bufsize=0, mode='r', openhook=None)
    # files:     # 文件的路径列表，默认是stdin方式，多文件['1.txt','2.txt',...]
    # inplace:    # 是否将标准输出的结果写回文件，默认不取代
    # backup:    # 原文件已经修改,备份文件的扩展名，只指定扩展名，如.bak。如果该文件的备份文件已存在，则会自动覆盖。
    # bufsize:    # 缓冲区大小，默认为0，如果文件很大，可以修改此参数，一般默认即可
    # mode:　　　　　　# 读写模式，默认为只读
    # openhook:　　　 # 该钩子用于控制打开的所有文件，比如说编码方式等;
    with open(filename_X, 'r') as f:
        lines_a = f.readlines()
        l_a = len(lines_a)
    with open(changefile_Y, 'r') as f:
        lines_b = f.readlines()
        # for i in range(len(lines_b)):
        #     print(lines_b[i][22:26])
        # exit()
    with open(resultname, 'w') as f:
        # 先将stem的一边读入
        for line in lines_b[:inf - N + 1]:
            f.write(line.strip() + " \n")

        # 再将连着的hairpin一次性读入
        for line in lines_a:
            f.write(line.strip() + " \n")

        # 最后将剩下的stem另一半读入
        for line in lines_b[inf + N + 1:]:
            f.write(line.strip() + " \n")

    # 更改碱基序号base_cnt +  更改原子序号atom_cnt
    with open(resultname, 'r') as f:
        lines = f.readlines()
    with open(resultname, 'w') as f:
        # 取index下一组的碱基编号，然后往上面倒着读和修改,确保多端口时，端口下面的断点不被消除，保留断点
        base_cnt = int(lines_b[inf + N][22:26])
        # PNC三个原子一组
        k = 0
        # 倒着读取i值
        for i in range(len(lines) - 1, -1, -1):
            # 从index往上读，有可能变成负数
            if i < inf - N + l_a + 1:
                lines[i] = lines[i][:22] + f'{base_cnt:>4}' + lines[i][26:]
                # lines[i] = lines[i].replace(lines[i][22:26], f'{base_cnt:>4}')
                k += 1
                if k % 3 == 0:
                    base_cnt -= 1
        # 把碱基序号变成1开头的碱基编号，去除负数开头，或者大于1的数开头的序号
        first_num = int(lines[0][22:26])
        # 更改原子序号atom_cnt
        atom_cnt = 1
        for i in range(len(lines)):
            num = int(lines[i][22:26]) - first_num + 1
            lines[i] = lines[i][:22] + f'{num:>4}' + lines[i][26:]
            # 更改原子序号atom_cnt
            lines[i] = lines[i][:6] + f'{atom_cnt:>5}' + lines[i][11:]
            atom_cnt += 1
            f.write(lines[i])


def assemble_beside(filename_X, changefile_Y, resultname, inf, Flag):
    """
    将旋转平移后得到的文件 和 原来没有动的文件组合，和成一个RNA结构PDB文件
    assemble2 也需要组合后再重新排序，但不是排成顺序，因为需要序列缺口来进行后续的操作
    """
    with open(filename_X, 'r') as f:
        lines_a = f.readlines()
        l_a = len(lines_a)
    with open(changefile_Y, 'r') as f:
        lines_b = f.readlines()
    with open(resultname, 'w') as f:
        if Flag == 0:
            # 先读X片段一整段
            f.write(''.join(lines_a))
            # 再把Y片段下半段放到最后
            for line in lines_b[inf + 1:]:
                f.write(line)
        elif Flag == 1:
            # 先读Y片段上半段放在开头
            for line in lines_b[:inf + 1]:
                f.write(line)
            # 然后读入X片段一整段
            f.write(''.join(lines_a))

    # 侧边拼装不需要重新排序原子序号，只用调整碱基编号就可
    # 因为在Y片段下半部分拼接时（Flag==0）需要重排序列防止末尾碰巧连上了
    # Flag ==1 时，一定是能找到断口的
    # 更改碱基序号base_cnt
    if Flag == 0:
        with open(resultname, 'r') as f:
            lines = f.readlines()
        with open(resultname, 'w') as f:
            base_cnt = 1
            # PNC三个原子一组
            k = 0
            for i in range(len(lines)):
                # 只是把最后长于X片段的序号改变改变一下，其余不变
                if i > l_a - 1:
                    lines[i] = lines[i][:22] + f'{base_cnt:>4}' + lines[i][26:]
                    # lines[i] = lines[i].replace(lines[i][22:26], f'{base_cnt:>4}')
                    k += 1
                    if k % 3 == 0:
                        base_cnt += 1
                f.write(lines[i])


def get_coordinates_pdb(filename):
    """
    Get coordinates from the first chain in a pdb file
    and return a vectorset with all the coordinates.

    Parameters
    ----------
    filename : string
        Filename to read

    Returns
    -------
    V : array
        (N,3) where N is number of atoms
    """

    V = list()

    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                for j in range(len(line)):
                    if '.' == line[j] and '.' == line[j + 8]:
                        x_index = j
                        break
                x = line[x_index - 4:x_index + 4]
                y = line[x_index + 4:x_index + 12]
                z = line[x_index + 12:x_index + 20]
                V.append(np.asarray([x, y, z], dtype=float))

    V = np.asarray(V)

    return V


def get_coordinates_Apdb(filename, N):
    """
    只保留1bp/2bp/3bp 的读取方法 N==3/6/9
    一端开口的片段，比如hairpin
    filename : 片段中只保留1bp/2bp/3bp的数据库地址string

    Return
    V : array
        (N,3) where N is number of atoms
    """

    V = list()

    with open(filename, "r") as f:
        lines = f.readlines()
        list_lines = [lines[:N], lines[-N:]]
        for lines_choice in list_lines:
            for line in lines_choice:
                # 修改加上HETATM
                if line.startswith("ATOM") or line.startswith("HETATM"):
                    for j in range(len(line)):
                        if '.' == line[j] and '.' == line[j + 8]:
                            x_index = j
                            break
                    x = line[x_index - 4:x_index + 4]
                    y = line[x_index + 4:x_index + 12]
                    z = line[x_index + 12:x_index + 20]
                    V.append(np.asarray([x, y, z], dtype=float))

    V = np.asarray(V)
    # array([[1., 2., 3.]])这样就变成了一个二维数组
    # a = np.asarray([[1, 2, 3], [4, 5, 6]])
    # size-用来计算数组和矩阵中所有元素的个数6
    # shape-用来计算矩阵每维的大小(2, 3)

    return V


def get_coordinates_Bpdb(filename, N):
    """
    只保留1bp/2bp/3bp的读取方法 N==3/6/9
    读取两端接口的中间index处位置信息
    filename 片段中只保留1bp/2bp/3bp的数据库地址string
    return V , index 111222333(index)/999101010111111

    """
    V = list()
    with open(filename, "r") as f:
        lines = f.readlines()
        index = 0
        # index 用来找一个两端开口的片段开处
        # 正序找端口
        if int(lines[0][22:26]) == int(lines[3][22:26]) == 1:
            for j in range(len(lines) - 1):
                if int(lines[j+1][22:26]) != 1:
                    index = j - 3
                    break
        else:
            for i in range(len(lines) - 1):
                # i -> [22,19,16,13,10,7,4,1]
                if not (int(lines[i][22:26]) + 1 == int(lines[i + 1][22:26]) or int(lines[i][22:26]) == int(lines[i + 1][22:26])):
                    index = i
                    break

        for line in lines[index - N + 1:index + N + 1]:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                for j in range(len(line)):
                    if '.' == line[j] and '.' == line[j + 8]:
                        x_index = j
                        break
                x = line[x_index - 4:x_index + 4]
                y = line[x_index + 4:x_index + 12]
                z = line[x_index + 12:x_index + 20]
                V.append(np.asarray([x, y, z], dtype=float))

    V = np.asarray(V)

    return V, index


def get_coordinates_Apdb_beside(filename, Insect, L):
    """
    侧拼
    一端开口的片段，比如hairpin
    得到接口的坐标信息数组V
    根据传入要读取的长度L和开始读取的接口Insect来读取
    filename 一定是只保留1bp的片段库
    """
    V = list()
    # 粗粒化，三个原子一个单元
    n = Insect * 3
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines[n: n + L * 3]:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                for j in range(len(line)):
                    if '.' == line[j] and '.' == line[j + 8]:
                        x_index = j
                        break
                x = line[x_index - 4:x_index + 4]
                y = line[x_index + 4:x_index + 12]
                z = line[x_index + 12:x_index + 20]
                V.append(np.asarray([x, y, z], dtype=float))

    V = np.asarray(V)
    return V


def get_coordinates_Bpdb_beside(filename, Flag):
    """
    读取stems上半部分/下半部分片段信息
    Parameters
    ----------
    filename 一定是只保留1bp的片段库
    Flag : 0 代表读上半部分/1 代表读下半部分

    Returns 返回stems坐标数组，和index信息
    -------

    """
    V = list()

    with open(filename, "r") as f:
        lines = f.readlines()
        index = 0
        # index 用来找一个两端开口的片段开处
        # 正序找端口
        for i in range(len(lines) - 1):
            if not (int(lines[i][22:26]) + 1 == int(lines[i + 1][22:26])
                    or int(lines[i][22:26]) == int(lines[i + 1][22:26])):
                index = i
                break
        if Flag == 0:
            for line in lines[:index + 1]:
                if line.startswith("ATOM") or line.startswith("HETATM"):
                    for j in range(len(line)):
                        if '.' == line[j] and '.' == line[j + 8]:
                            x_index = j
                            break
                    x = line[x_index - 4:x_index + 4]
                    y = line[x_index + 4:x_index + 12]
                    z = line[x_index + 12:x_index + 20]
                    V.append(np.asarray([x, y, z], dtype=float))

        elif Flag == 1:
            for line in lines[index + 1:]:
                if line.startswith("ATOM") or line.startswith("HETATM"):
                    for j in range(len(line)):
                        if '.' == line[j] and '.' == line[j + 8]:
                            x_index = j
                            break
                    x = line[x_index - 4:x_index + 4]
                    y = line[x_index + 4:x_index + 12]
                    z = line[x_index + 12:x_index + 20]
                    V.append(np.asarray([x, y, z], dtype=float))

    V = np.asarray(V)
    return V, index


def func(path, X, Y, n):
    """
    第一套 拼装函数  X,Y分别为一端开口和两端开口的片段
        保留1bp/2bp/3bp的文件路径
    n是接口保留BP
    n = 1/2/3
    N=3/6/9
    """
    N = n * 3

    # 因为只用移动一个模块到另一个模块上，所以只用读入一个
    # 这里我们传入B，移动片段B，不修改片段A
    q_all = get_coordinates_pdb(Y)

    # 读入借口片段，根据不同N来读入
    p_insert = get_coordinates_Apdb(X, N)
    # index  444999 中4的位置
    q_insert, index = get_coordinates_Bpdb(Y, N)

    # p_all/q_all是一个（N,3）N行3列的XYZ坐标矩阵
    p_size = p_insert.shape[0]  # shape(0)指的就是N值
    q_size = q_insert.shape[0]

    if not p_size == q_size:
        raise Exception("Structures not same size")

    # 拷贝接口一份
    p_coord = copy.deepcopy(p_insert)
    q_coord = copy.deepcopy(q_insert)

    # 中心化找质心
    p_cent = centroid(p_coord)
    q_cent = centroid(q_coord)

    # 平移操作
    p_coord -= p_cent
    q_coord -= q_cent

    # 旋转
    U = kabsch(q_coord, p_coord)

    # 旋转平移完毕，在把变换好的模块移到另一个没有动的模块上
    q_all_changed = q_all - q_cent
    q_all_changed = np.dot(q_all_changed, U)
    q_all_changed += p_cent

    # 得到数据
    change_b = rf'{path}/change_b.pdb'
    resultname = rf'{path}/result.pdb'
    change_coordinates_Bpdb(Y, change_b, q_all_changed)
    assemble(X, change_b, resultname, index, N)
    # 返回相对路径
    return resultname
    # 返回绝对路径
    # return os.path.abspath(resultname)


def func_beside(path, X, Y, insect, long, flag=0):
    """
    第二套 拼装函数 专门用来 侧向拼装
     X,Y分别为一端开口和两端开口的保留1bp的片段文件路径

    insect: 是X片段中要插入的点括号形式的列表下标，0开始
    long:      侧拼的长度
    flag:   根据传入1/0来判断是要读取Y片段的上半部分还是下半部分（根据括号里包括的是[或者]来区别 ）
            (根据flag来确定是拼stem的左半边还是右半边)
    """

    # 这里我们传入B，移动片段B，不修改片段A
    q_all = get_coordinates_pdb(Y)

    # 读入借口片段，根据insect来确定读入接口，long来确定读取的长度
    p_insert = get_coordinates_Apdb_beside(X, insect, long)
    # index  444999 中4的位置
    q_insert, index = get_coordinates_Bpdb_beside(Y, flag)

    # p_all/q_all是一个（N,3）N行3列的XYZ坐标矩阵
    p_size = p_insert.shape[0]  # shape(0)指的就是N值
    q_size = q_insert.shape[0]

    if not p_size == q_size:
        # print("error: Structures not same size")
        raise Exception("Structures not same size")

    # 拷贝接口一份
    p_coord = copy.deepcopy(p_insert)
    q_coord = copy.deepcopy(q_insert)

    # 中心化找质心
    p_cent = centroid(p_coord)
    q_cent = centroid(q_coord)

    # 平移操作
    p_coord -= p_cent
    q_coord -= q_cent

    # 旋转
    U = kabsch(q_coord, p_coord)

    # 旋转平移完毕，在把变换好的模块移到另一个没有动的模块上
    q_all_changed = q_all - q_cent
    q_all_changed = np.dot(q_all_changed, U)
    q_all_changed += p_cent

    # 得到数据
    change_b = rf'{path}/change_b.pdb'
    resultname = rf'{path}/result.pdb'
    # 读取Y文件中出了坐标以外的其余信息，把旋转平移后的stems片段坐标形式变成pdb格式
    # 不用修改
    change_coordinates_Bpdb(Y, change_b, q_all_changed)
    # 组合片段，把变换完成后的stems片段拼接到不动的X片段上，然后去掉重叠处最后重新排序。
    assemble_beside(X, change_b, resultname, index, flag)
    # 返回相对路径
    return resultname
    # 返回绝对路径
    # return os.path.abspath(resultname)


if __name__ == "__main__":
    print('zhouli')
