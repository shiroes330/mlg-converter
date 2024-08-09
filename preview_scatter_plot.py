tune_path = "C:\\Users\\shiro\\Documents\\TunerStudioProjects\\202402_firmware_0\\CurrentTune.msq"


import sys
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt


def get_table(i1, i2, col_num):
    tx = root[i1][i2].text
    data = tx.split("\n")
    data = data[1:-1]
    data = [d.split(" ") for d in data]
    col = col_num+9
    data = [d[9:col] for d in data]
    table = pd.DataFrame(data)
    return table

def draw_scatter(df, xtric, ytric):
    _, axs = plt.subplots(1, figsize=(12,8), height_ratios=[1])
    axs.set_facecolor("black")
    axs.grid(which="major", color="gray", linestyle="dotted")
    s3 = axs.scatter(df["RPM"], df["MAP"], s=2, c=df["AFR_S"], cmap=plt.cm.jet)
    plt.xticks([int(float(d)) for d in xtric])
    plt.yticks([int(float(d)) for d in ytric])
    plt.tick_params(labelsize=7)
    plt.colorbar(s3)
    plt.show()

if __name__ == "__main__":
    log_path = sys.argv[1]
    log_path = log_path.replace(".mlg", ".csv")
    tree = ET.parse(tune_path)
    root = tree.getroot()
    print(root)
    for i1, one_c in enumerate(root):
        for i2, two_c in enumerate(one_c):
            print(two_c.attrib['name'])
            if "ve" in two_c.attrib['name']:
                print("i1: %s"%i1)
                print("i2: %s"%i2)
    ve_table = get_table(4,0,16)
    x_bin = get_table(4,1,1)
    y_bin = get_table(4,2,1)
    ve_table.columns=x_bin[0].to_list()
    ve_table.index=y_bin[0].to_list()
    print(ve_table.head())

    # Load log
    df = pd.read_csv(log_path, delimiter=";", skiprows=[1], index_col="Time")
    print(df.keys())
    afr_shit = df["AFR"].to_list()[1:]
    afr_shit.append(14.7)
    df['AFR_S'] = afr_shit
    draw_scatter(df, ve_table.columns.to_list(), ve_table.index.to_list())
