# %%
import numpy as np
import openpyxl as oxl
import math
import xlwt as xt
import pandas as pd

# 目标数据列
tar_cols = []

# 获取目标数据
def load_tar_xml(path):
    # 操作变量列
    op_cols = []
    op_data = []
    # 性质列
    pro_cols = []
    pro_data = []
    # 数据
    data = []

    wb = oxl.load_workbook(path)
    tar_sheet = wb.get_sheet_by_name("Sheet1")

    # 获取性质列
    for i in range(3, 17):
        pro_cols.append(tar_sheet.cell(row=3, column=i).value)
    
    # 获取操作变量列
    row = tar_sheet.max_row
    col = tar_sheet.max_column
    for i in range(4, row + 1):
        row_data = []
        for j in range(1, col + 1):
            row_data.append(tar_sheet.cell(row=i, column=j).value)
        
        data.append(row_data)
    
    return data


# 获取原始数据
def load_ori_xml(path):
    # 操作变量列
    op_cols = []
    op_data285 = []
    op_data313 = []
    # # 性质列
    # pro_cols = []
    # pro_data285 = []
    # pro_data313 = []
    # 样本行
    row285 = range(4, 44)
    row313 = range(45, 85)

    wb = oxl.load_workbook(path)
    # names = wb.get_sheet_names()
    # 操作变量sheet
    op_sheet = wb.get_sheet_by_name("操作变量")
    # # 原料sheet
    # pro_sheet1 = wb.get_sheet_by_name("原料")
    # # 产品sheet
    # pro_sheet2 = wb.get_sheet_by_name("产品")
    # # 待生吸附剂sheet
    # pro_sheet3 = wb.get_sheet_by_name("待生吸附剂")
    # # 再生吸附剂sheet
    # pro_sheet4 = wb.get_sheet_by_name("再生吸附剂")

    # 处理操作变量sheet
    row = op_sheet.max_row
    col = op_sheet.max_column
    # 读取操作变量列(英文,中文就不处理了)
    for i in range(1, col + 1):
        op_cols.append(op_sheet.cell(row=2, column=i).value)
    # 读取数据
    for i in row285:
        temp_row = []
        for j in range(1, col + 1):
            temp_row.append(op_sheet.cell(row=i, column=j).value)
        op_data285.append(temp_row)
    for i in row313:
        temp_row = []
        for j in range(1, col + 1):
            temp_row.append(op_sheet.cell(row=i, column=j).value)
        op_data313.append(temp_row)

    # # 处理性质sheet
    # t1 = []
    # t2 = []
    # # 原料sheet
    # for i in row285:
    #     pro_cols.append(pro_sheet1.cell(row=1, column=i).value)
    #     t1.append(pro_sheet1.cell(row=2, column=i).value)
    #     t2.append(pro_sheet1.cell(row=3, column=i).value)
    # # 产品sheet
    # for i in row285:
    #     pro_cols.append(pro_sheet2.cell(row=2, column=i).value)
    #     t1.append(pro_sheet2.cell(row=3, column=i).value)
    #     t2.append(pro_sheet2.cell(row=4, column=i).value)
    # # 待生吸附剂sheet
    # for i in row285:
    #     pro_cols.append(pro_sheet3.cell(row=2, column=i).value)
    #     t1.append(pro_sheet3.cell(row=3, column=i).value)
    #     t2.append(pro_sheet3.cell(row=4, column=i).value)
    # # 再生吸附剂sheet
    # for i in row285:
    #     pro_cols.append(pro_sheet4.cell(row=2, column=i).value)
    #     t1.append(pro_sheet4.cell(row=3, column=i).value)
    #     t2.append(pro_sheet4.cell(row=4, column=i).value)
    # pro_data285.append(t1)
    # pro_data285.append(t2)

    return op_cols, op_data285, op_data313


# 预处理285,313数据
def preProcess(data, cols):
    resData = []
    # 数据整定
    data = np.array(data)
    # 跳过时间列
    for i in range(1, len(data[0])):
        # 1.删除全部为空的位点
        if len(np.nonzero(data[:, i])[0]) > 0:
            # 2.处理部分数据为空值的位点
            col_av = np.average(data[:, i].astype(np.float))
            for j in range(len(data[:, i])):
                if j == 0:
                    data[j, i] = col_av
            # 3.根据拉益达准则去除异常值
            pdata = data[:, i].astype(np.float)
            res = []
            p_av_mat = np.full_like(pdata, np.average(pdata))
            p_av = np.average(pdata)
            theta = math.sqrt(np.linalg.norm((p_av_mat - pdata), 2) / (len(pdata) - 1))
            for k in range(len(pdata)):
                if abs(pdata[k] - p_av) <= 3 * theta:
                    res.append(pdata[k])
            resData.append({cols[i]: np.average(np.array(res))})
        else:
            continue
    
    return resData

# 写出数据,xlwt库不支持多余256列的写入，因此使用csv格式导出
def output_data(data, path):
    keys = []
    values = []
    for d in data:
        keys.append(list(d.keys())[0])
        values.append(list(d.values())[0])
    
    # 输出csv
    pd.DataFrame(dict(zip(keys, values)), index=[0]).to_csv(path, index=False)
    


# %%
if __name__ == "__main__":
    # cols, data285, data313 = load_ori_xml(r'E:\数模题\附件三：285号和313号样本原始数据.xlsx')
    # res285 = preProcess(data285, cols)
    # res313 = preProcess(data313, cols)
    # output_data(res285, r'C:\Users\Administrator\Desktop\285.csv')
    # output_data(res313, r'C:\Users\Administrator\Desktop\313.csv')
    s = load_tar_xml(r'E:\数模题\附件一：325个样本数据.xlsx')


# %%

