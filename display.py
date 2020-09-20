#-*- coding:utf-8 –*-
from  matplotlib import pyplot as plt
import prepareData as prd
import numpy as np
import pandas as pd
import pydotplus
from IPython.display import Image
from sklearn import tree
import featureSelect as fs

plt.rcParams['font.sans-serif']=['SimHei']

# 计算空值
def compute_zero(data, cols):
    # 记录参与计算的列和列的空值数
    res_data = []
    res_col = []
    # 转化数据格式
    data = np.array(data)[:, 1:].astype(np.float)
    
    # 计算空值数
    for i in range(len(data[0])):
        zero_count = 0
        cur_col_data = data[:, i].astype(np.float)
        # 存在过0值则此列的空值为0
        if any(cur_col_data < 0) and any(cur_col_data > 0):
            pass
        else:
            zero_count = len(cur_col_data) - len(np.nonzero(cur_col_data)[0])
            if zero_count != 40 and zero_count != 0:
                res_col.append(cols[i])
                res_data.append(zero_count)


    return res_col, res_data


# 绘制空值柱状图
def zeroHistogram(data, cols):
    zero_cols, zero_data = compute_zero(data, cols)
    # 网上抄的代码,展示柱状图
    ddata = pd.Series(zero_data, index=zero_cols)
    fig = plt.figure(figsize=(7, 5),  dpi=90)  # 声明画布1
    ax = fig.add_subplot(1,1,1) #  声明绘图区
    x, y = ddata.index, ddata.values
    rects = plt.bar(x, y, color='dodgerblue', width=0.35, label='空值数')
    plt.grid(linestyle="-.", axis='y', alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()


# 绘制两变量相关散点图
def var_Scatter(x, y):
    plt.scatter(x, y, s=20, marker = 'o')
    
# 展示决策树结构
def disp_dt(clf, cols):
    dot_data = tree.export_graphviz(clf, out_file=None, 
                         feature_names=cols,  
                         filled=True, rounded=True, special_characters=True)  
    graph = pydotplus.graph_from_dot_data(dot_data)
    Image(graph.create_png())


if __name__ == "__main__":
    # cols, data285, data313 = prd.load_ori_xml(prd.ori_path)

    cols, data, tar, _, _ = fs.mergeData()
    tar = tar.reshape(-1, 1)
    data = np.array(data).T
    model = fs.randomTree(data, tar, cols)
    model.fit(data, tar)
    disp_dt(model, cols)

    # 绘制原始数据空值数量
    # zeroScatter(data285, cols)
    # zeroScatter(data313, cols)