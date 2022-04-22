import time
import os
import shutil


def Select_structure(allnum, chosenum):
    """
    在最终的结构文件里，利用统计势挑选最优的结构
    :param chosenum: 所有构想数
    :param chosenum: 提供需要选取最优解的数目
    计算每个pdb的能量值，并写入./Energy_out.csv文件"""
    name = rf'Select_Result'
    # os.system("ulimit -s unlimited")
    route = fr'ulimit -s unlimited; ./cgRNASP-Feb ./CG_Result/ {allnum} ./Energy_out.csv'
    with os.popen(route) as p:
        p.read()

    """给能量值排序，然后选出前几项的pdb文件拷贝到新文件夹:Select_Result"""
    with open('Energy_out.csv', 'r') as f:
        num = 1
        lines = f.readlines()
        lines.sort(key=lambda x: float(x.split(',')[1].strip()))
        for jjj in lines[:chosenum]:
            old_path = fr"./CG_Result/{jjj.split(',')[0]}"
            new_dir_path = fr'./{name}'
            if not os.path.exists(new_dir_path):
                os.makedirs(new_dir_path)
            new_file_path = fr'{new_dir_path}/{name.split("_")[0]}_Top{num}.pdb'
            num += 1
            shutil.copy(old_path, new_file_path)


if __name__ == "__main__":
    Total_num = len(os.listdir(r"./CG_Result"))
    time_start = time.time()
    while True:
        select_num = input('Seleted Num(0=all):')
        if select_num.isdigit():
            if select_num == "0":
                print("SELETED ALL RESULT")
                exit()
            else:
                select_num = int(select_num)
                Select_structure(Total_num, select_num)
                time_end = time.time()
                print(
                    f'It takes {time_end - time_start:.3f}s to complete [the structure selection] at ""./Select_Result"')
                break
        else:
            print("Please enter the correct instruction!")
            continue
