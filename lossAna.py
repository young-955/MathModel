import prepareData as prd
import featureSelect as fs
from keras import models, layers
import numpy as np
from keras.models import load_model


ron_model_path = r'C:\Users\wuziyang\Desktop\ron_model.h5'
s_model_path = r'C:\Users\wuziyang\Desktop\s_model.h5'


# https://www.marktechpost.com/2019/06/17/regression-with-keras-deep-learning-with-keras-part-3/
def dn_model(data, tar, test_data, test_tar):
    model = models.Sequential()
    model.add(layers.Dense(8, activation='relu', input_shape=[data.shape[1]]))
    model.add(layers.Dense(16, activation='relu'))
    model.add(layers.Dense(1))
    model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
    his = model.fit(data, tar, validation_split=0.15, epochs=3000)
    res = model.evaluate(test_data, test_tar)
    # print(np.array([data[0]]))
    print(model.predict(np.array([data[0]])))
    # The output values represent the loss (Mean Squarred Error) and the metrics (Mean Absolute Error).
    return model, res, his

def save_model(model, path):
    model.save(path)

def load_m(path):
    return load_model(path)


if __name__ == "__main__":
    opCol, opData, tarData, proCol, proData, s_col = fs.mergeData()
    proData = np.array(proData)
    opData = np.array(opData)

    t_data = []
    for i in range(len(opData[0])):
        a = opData[:, i]
        t_data.append(a)

    opData = np.array(t_data)
    # print(proData.shape)
    # print(opData.shape)
    input_data = np.hstack((proData, opData))
    train_data = input_data[: 300]
    test_data = input_data[300:]
    train_tar = tarData[:300]
    test_tar = tarData[300:]
    train_s = s_col[:300]
    test_s = s_col[300:]

    # ron_model = load_m(ron_model_path)
    # a = train_data[0]
    # a = [a]
    # a = np.array(a)
    # q = ron_model.predict(a)
    # print(q)

    ron_model, ron_test_res, his = dn_model(train_data, train_tar, test_data, test_tar)
    # s_model, s_test_res = dn_model(train_data, train_s, test_data, test_s)
    
    # print(his.history['loss'])
    # print(his.history['mean_absolute_error'])
    print(ron_test_res)

    # print(s_test_res)

    save_model(ron_model, ron_model_path)
    # save_model(s_model, s_model_path)
