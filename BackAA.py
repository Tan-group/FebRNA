import os
import shutil


def cg_to_aa(path):
    if os.path.exists(r"./AA_Result.pdb"):
        os.remove(r"./AA_Result.pdb")
    route = f"./reconstruction {path}"
    os.system(route)


if __name__ == "__main__":
    if os.path.exists(r"./AA_Result"):
        shutil.rmtree(r"./AA_Result")
    os.mkdir(r"./AA_Result")
    select_dir = "minrmsdCG_Result"
    for cg_file in os.listdir(select_dir):
        file_path = fr'{select_dir}/{cg_file}'
        cg_to_aa(file_path)
        top_name = cg_file.split("_")[0].split(".")[0]
        shutil.move(rf'./AA_Result.pdb', rf'./AA_Result/{top_name}_Allatom.pdb')
