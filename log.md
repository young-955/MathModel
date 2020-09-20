# 竞赛题目做法与思路

## 第一问
按题目要求，只用附件二操作附件三，其他不管。
Note:
第一版：285.csv 313.csv
使用附件二中的（1）（3）（5）步骤对原始数据进行处理。

第二版：285(1).csv 313(1).csv
按“专家”要求使用附件中的（1）（3）（4）步骤对原始数据进行处理。

## 第二问
按题目要求，先对样本数据进行必要的清洗，性质数据不做清洗.

清洗方法：
按附件二中（1）（3）步骤对样本数据清洗，同时人工筛选大部分为空值的位点。
人工筛选性质。
使用相关性计算，相关性高的列，选取其中一个保留。由于各操作变量的变化幅度都很小，因此计算的相似度都很高，所以选择0.99的选择阈值。此阶段目标是筛选变量到200个以下。

使用多种分析方法，提取关键变量，提取过程具有随机性。
### 随机森林：
https://www.cnblogs.com/stevenlk/p/6543646.html#2-%E5%9F%BA%E4%BA%8E%E6%A0%91%E6%A8%A1%E5%9E%8B%E7%9A%84%E7%89%B9%E5%BE%81%E9%80%89%E6%8B%A9embedded%E6%96%B9%E5%BC%8F
这种方法存在偏向 ，对具有更多类别的变量会更有利；
对于存在_关联的多个特征_，其中任意一个都可以作为指示器（优秀的特征），并且_一旦某个特征被选择之后，其他特征的重要度就会急剧下降_(因为不纯度已经被选中的那个特征降下来了，其他的特征就很难再降低那么多不纯度了，这样一来，只有先被选中的那个特征重要度很高，其他的关联特征重要度往往较低)。在理解数据时，这就会造成误解，导致错误的认为先被选中的特征是很重要的，而其余的特征是不重要的，但实际上这些特征对响应变量的作用确实非常接近的（这跟Lasso是很像的）。

## 第三问
使用
https://www.marktechpost.com/2019/06/17/regression-with-keras-deep-learning-with-keras-part-3/
中的深度学习回归。

模型结构：
    model.add(layers.Dense(8, activation='relu', input_shape=[data.shape[1]]))
    model.add(layers.Dense(16, activation='relu'))
    model.add(layers.Dense(1))

模型参数选择：
validation_split=0.2, epochs=3000

验证方法：
将输入数据划分为300:25的两个数据集，前300条数据用于模型训练，后25条数据用于模型效果验证。
结果格式如下：
The output values represent the loss (Mean Squarred Error) and the metrics (Mean Absolute Error).
RON验证结果：
Mean Squarred Error， Mean Absolute Error
[0.023724902421236038, 0.1253451108932495]


## 第四问
需要两个模型，一个是第三问中预测RON的，一个是这个环节预测输出S的。
已知样本每个变量的输入范围，使用三分法，逐步降低RON，并确保S小于5。
三分法：
https://www.cnblogs.com/newpanderking/archive/2011/08/25/2153777.html

伪代码：
FOR D IN 输入数据：
    FOR V IN 可操作变量：
        使用三分法调整当前变量，得到当前变量调整后的数据D1
        RON = RON_Model.predict(D1)
        // 题目限制条件
        IF S_Model.predict(D1) < 5:
            记录min(RON)与对应的D1



## 第五问
做，很好做
绘图思路：
以时间为x轴，S和RON为Y轴绘图
下方列出表格，展示各变量变化过程（是不是也有点长。。）
