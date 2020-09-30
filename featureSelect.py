# %%
#-*- coding:utf-8 –*-
from sklearn.ensemble import  GradientBoostingClassifier
from sklearn.feature_selection import SelectFromModel
import prepareData as prd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from  matplotlib import pyplot as plt
import pandas as pd
# import tools


# 随机森林算法
def randomTree(data, tar, col):
    res = []
    # 获取中英文列名dict
    op_dict = prd.get_op_dict()

    rf = RandomForestRegressor(n_estimators=300, max_features=20)
    rf.fit(data, tar)
    print("Features sorted by their score:")
    st_res = sorted(zip(map(lambda x: "%.4f"%x, rf.feature_importances_), col), reverse=True)
    for i in st_res:
        print([i[0], i[1], op_dict[i[1]]])
    
    return rf


# 处理性质数据
# 第十二列是目标数据
def get_pro_data():
    pro_data, pro_cols, _, _ = prd.load_tar_xml(prd.del_path)
    # pro_data = np.array(pro_data)[:, 1:].astype(np.float)
    # prd.processProperty(pro_data, pro_cols)
    # tar_data = pro_data[:, 11]
    # p_cols = pro_cols[:11] + pro_cols[12:]
    # p_data = pro_data[:, :11] + pro_data[:, 12:]
    pro_data = np.array(pro_data)
    # s产量
    s_col = pro_data[:, 7]
    # RON值
    tar_data = pro_data[:, 1].astype(np.float) - pro_data[:, 8].astype(np.float)
    pro_data = np.hstack((pro_data[:, :7].astype(np.float), pro_data[:, 10:].astype(np.float)))
    pro_cols = np.array(pro_cols)
    pro_cols = list(pro_cols[:9]) + list(pro_cols[10:])

    return tar_data, pro_cols, pro_data, s_col


# 处理操作变量数据，提取操作变量和目标数据
def get_op_data():
    # 获取样本数据
    _, _, op_data, op_cols = prd.load_tar_xml(prd.del_path)
    p_op_col, p_op_data = prd.processOridata(op_data, op_cols)

    return p_op_col, p_op_data


# 汇总整合数据和目标
def mergeData():
    opCol, opData = get_op_data()
    tarData, proCol, proData, s_col = get_pro_data()

    return opCol, opData, tarData, proCol, proData, s_col


# 计算列相关性
def cal_corr():
    op_Dict = prd.get_op_dict()
    opCol, opData, tarData, proCol, proData, s_col = mergeData()
    # opData = np.array(opData).reshape(325, 335)
    opData = np.array(opData)
    proData = np.array(proData)
    # 整理列名
    pCols = []
    for i in opCol + proCol:
        if i in op_Dict:
            pCols.append(str(i) + str(op_Dict[i]))
        else:
            pCols.append(i)
    pCols = np.array(pCols)
    opData = opData.reshape(325, -1)
    # print(opData.shape)
    # print(proData.shape)
    # print(pCols.shape)
    a = np.hstack((np.array(opData), np.array(proData)))
    corr = pd.DataFrame(dict(zip((pCols), a.reshape(325, -1)))).corr()
    return corr

# %%
if __name__ == "__main__":
    # cols, data, tar, _, _, s_col = mergeData()
    # tar = tar.reshape(-1, 1)
    # data = np.array(data).T
    # model = randomTree(data, tar, cols)


    corr = cal_corr()
    corr = corr[abs(corr) > 0.99]
    s = corr.count()
    # ac = 0
    # print(corr.columns[0])
    # for i in range(len(s)):
    #     if s[i] > 1 and s[i] <= 5:
    #         print(corr.columns[i])
    #     ac += s[i]
    # print(ac)
    corr.to_csv(r'C:\Users\Administrator\Desktop\ori_corrs.csv', encoding='utf-8-sig')

# %%
