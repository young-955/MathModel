import lossAna as la
import prepareData as prd
import featureSelect as fs
import numpy as np
import pandas as pd


# 魔改版三分法
# 多输入，每次单变量变化
# 有限制条件s <= 5
def Solve(v_range, ron_model, s_model, pro_data, tar_data):
    v = v_range.values()
    v_range = np.array(list(v))
    left = v_range[:, 0].copy()
    right = v_range[:, 1].copy()
    input_data = np.hstack((pro_data, v_range[:, 0]))
    init_data = input_data
    mid = 0
    midmid = 0
    for i in range(len(pro_data)):
        lim = (v_range[i][1] - v_range[i][0]) / 990000
        temp_data = list(input_data)
        while left[i] < right[i] and (right[i] - left[i]) >= lim:
            # print(i)
            mid = (left[i] + right[i]) / 2
            midmid = (mid + right[i]) / 2
            temp_data[i + len(pro_data)] = mid
            mid_data = np.array([temp_data])
            temp_data[i + len(pro_data)] = midmid
            midmid_data = np.array([temp_data])
            temp_data[i + len(pro_data)] = left[i]
            left_data = np.array([temp_data])
            temp_data[i + len(pro_data)] = right[i]
            right_data = np.array([temp_data])
            mid_area = ron_model.predict(mid_data)
            midmid_area = ron_model.predict(midmid_data)
            left_area = ron_model.predict(left_data)
            right_area = ron_model.predict(right_data)
            # 求s的结果,小于5可以继续优化
            s_mid_value = s_model.predict(mid_data)
            s_midmid_value = s_model.predict(midmid_data)
            if s_mid_value > 5 and s_midmid_value > 5:
                if left_area > right_area:
                    left[i] = midmid
                else:
                    right[i] = mid
            elif s_mid_value > 5 and s_midmid_value <= 5:
                left[i] = midmid
            elif s_mid_value <= 5 and s_midmid_value > 5:
                right[i] = mid
            else:
                # ron求最小极值
                if mid_area <= midmid_area:
                    right[i] = midmid
                else:
                    left[i] = mid
        # 更新操作变量
        input_data[i + len(pro_data)] = left[i]
    
    res = ron_model.predict(np.array([list(input_data)]))
    if res > tar_data:
        print("failed " + str(tar_data))
        res = tar_data
        input_data = init_data

    return input_data, res


# 优化操作变量
def optimize():
    # 加载模型
    ron_model = la.load_m(la.ron_model_path)
    s_model = la.load_m(la.s_model_path)
    # 加载操作变量范围
    v_range = prd.get_range(prd.del_path)
    # 加载数据
    tar_data, pro_cols, pro_data, s_col = fs.get_pro_data()
    
    # 三分法确定操作变量
    res = []
    opt_res = []
    for p,t in zip(pro_data, tar_data):
        ar, ron = Solve(v_range, ron_model, s_model, p, t)
        res.append(ar)
        opt_res.append(ron)

    return res, opt_res



if __name__ == "__main__":
    res, opt_res = optimize()
    # print(res)
    # print(opt_res)
    with open(r'C:\Users\wuziyang\Desktop\1.txt', 'w') as f:
        for i in res:
            f.write(str(i))
            f.write('\n')
        f.close()
    with open(r'C:\Users\wuziyang\Desktop\2.txt', 'w') as f:
        for i in opt_res:
            f.write(str(i))
            f.write('\n')
        f.close()

    # pd.DataFrame(res).to_csv(r'C:\Users\wuziyang\Desktop\1.csv')
    # pd.DataFrame(opt_res).to_csv(r'C:\Users\wuziyang\Desktop\2.csv')