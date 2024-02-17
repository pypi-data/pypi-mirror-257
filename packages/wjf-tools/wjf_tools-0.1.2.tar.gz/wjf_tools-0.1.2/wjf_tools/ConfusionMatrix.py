import sys

import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import brier_score_loss

class Metric(object):
    '''
        def Train_model(model, train_x, train_y, validate_x, validate_y, test_x, test_y):
            true, pred = validate_y, model.predict(validate_x)
    的返回值就是构造函数的参数
        true = np.array([[0, 0, 1, 0],
                     [0, 0, 0, 1]])import osimport os
        y_true=true.argmax(axis=1)

        pred=  np.array( [
                    [9.15028811e-01, 8.05485323e-02, 8.47977935e-04, 3.57471826e-03],
                    [8.80581319e-01, 1.12179980e-01, 1.34876964e-03, 5.88990562e-03],
                ])
        y_pred = pre.argmax(axis=1))
    '''

    def __init__(self, y_true, y_pred):
        self.y_true = np.array(y_true)
        self.y_pred = np.array(y_pred)

        self.__matrix = confusion_matrix(y_true, y_pred)

    def to_matrix(self, matrix=None):
        self.__matrix = np.asarray(matrix)
        return self

    def Matrix(self):
        return self.__matrix

    def TP(self):
        tp = np.diag(self.__matrix)
        return tp.astype(float)

    def TN(self):
        tn = self.__matrix.sum() - (self.FP() + self.FN() + self.TP())
        return tn.astype(float)

    def FP(self):
        fp = self.__matrix.sum(axis=0) - np.diag(self.__matrix)
        return fp.astype(float)

    def FN(self):
        fn = self.__matrix.sum(axis=1) - np.diag(self.__matrix)
        return fn.astype(float)

    def TPRate(self):
        return self.TP() / (self.TP() + self.FN() + sys.float_info.epsilon)

    def TNRate(self):
        return self.TN() / (self.TN() + self.FP() + sys.float_info.epsilon)

    def FPRate(self):
        return 1 - self.TNRate()

    def FNRate(self):
        return 1 - self.TPRate()

    def Accuracy(self):
        ALL = self.TP() + self.FP() + self.TN() + self.FN()
        RIGHT = self.TP() + self.TN()
        return RIGHT / (ALL + sys.float_info.epsilon)

    def Recall(self):
        return self.TP() / (self.TP() + self.FN() + sys.float_info.epsilon)

    def Precision(self):
        return self.TP() / (self.TP() + self.FP() + sys.float_info.epsilon)

    def TSS(self):
        return self.TPRate() - self.FPRate()

    @staticmethod
    def Get_BS_BSS(y_true, y_pred,numlist):
        if len(numlist)==2:
            """
                :param y_true: y_true = y_test.argmax(axis=1) 拿到属于正类的下标1
                :param y_pred: model.predict(x_test_time_step)
                :return: BS和BSS的值
                
                y_prob2 = model.predict(x_test_time_step)[:, 1]拿到正类的概率
                """
            y_prob2=y_pred[:, 1]
            # BSS开始计算
            BS = brier_score_loss(y_true, y_prob2)
            y_mean = y_prob2.mean()
            # print(y_true)
            # print(y_mean)
            temp = y_true - y_mean
            # print(temp)
            temp = np.square(temp)
            # print(temp)
            temp = np.sum(temp) / float(len(y_true))
            BSS = 1 - BS / temp
            return [BS, BSS]
        elif len(numlist)!=2:
            def Cal_Bss(y_true, y_pred):
                BS = np.mean(np.square(y_true - y_pred), axis=0)
                y_ave = np.mean(y_true, axis=0)
                BSS = 1 - BS / np.mean(np.square(y_true - y_ave), axis=0)
                BSS = [BSS, BSS]
                return BSS
            '''
            y_true=y_true.argmax(axis=1) 多分类拿出的热编码下标一维数组
            y_pred = model.predict(test_x) （sample，numclasses）
            '''
            ####  [0 , 1 , 2 , 3 ] : 对应[ N , C , M , X]
            y_t = [[] for _ in range(len(numlist))]
            y_p = [[] for _ in range(len(numlist))]

            # 遍历每个指定的类别索引
            for idx, num in enumerate(numlist):
                for t, p in zip(y_true, y_pred):
                    # 将y_true中指定类别的标签置为1，其余置为0
                    y_t[idx].append(int(t == num))
                    # 提取每个样本属于指定类别的预测概率
                    y_p[idx].append(p[num])

            Bss = []
            for t, p in zip(y_t, y_p):
                # 计算每个指定类别的BSS
                Bss.append(Cal_Bss(np.array(t), np.array(p)))

            return Bss

    @staticmethod
    def Get_BS_BSS_Group(predict_yprob, test_y,grouplabelleft,grouplabelright):
        """
        计算并返回给定预测概率和真实标签的Brier分数（BS）和Brier技能分数（BSS）。

        Args:
            predict_yprob (np.array): 模型预测的概率分布，形状为(samples, num_classes)。
                                      每行代表一个样本，每列代表对应类别的预测概率。
            test_y (np.array): 真实的标签数据，(samples, num_classes)。
                               对于多分类问题，是one-hot编码的二维数组。
            grouplabel:哪几组作为一类【例如123】，label编号从0开始
        Returns:
            list: 包含计算得到的Brier分数（BS）和Brier技能分数（BSS）的列表。
        """
        predict_yprob_binary = []  ##以下代码块实现功能：由4类变2类！
        test_y_binary = []
        for i in range(len(predict_yprob)):
            predict_group_left_sum = sum(predict_yprob[i][label] for label in grouplabelleft) / 1.001
            predict_group_right_sum = sum(predict_yprob[i][label] for label in grouplabelright) / 1.001
            # 对于test_y，如果它是概率则进行相同处理，如果是标签则根据实际需要处理
            test_group_left_sum = sum(test_y[i][label] for label in grouplabelleft)
            test_group_right_sum = sum(test_y[i][label] for label in grouplabelright)
            # 将处理后的结果追加到相应的列表中
            predict_yprob_binary.append([predict_group_left_sum, predict_group_right_sum])
            test_y_binary.append([test_group_left_sum, test_group_right_sum])

        predict_yprob_binary=np.array(predict_yprob_binary)
        test_y_binary=np.array(test_y_binary)
        # print("predict_yprob_binary[:4]:", predict_yprob_binary[:4]) #N类和大于等于C类的和
        # print("test_y_binary[:4]:", test_y_binary[:4]) #属于N还是大于等于C
        new_predict_yprob_binary=[]            ##以下代码块实现功能：从2类数据中提取1维数据！
        new_test_y_binary=[]
        for i in range(len(predict_yprob_binary)):
            new_predict_yprob_binary.append(predict_yprob_binary[i][1]) #拿到大于等于C的组合概率                      ##通过修改这一行与下一行，可实现>=C和4分类中N类对应的BSS等切换！！！
            new_test_y_binary.append(test_y_binary[i][1])   #拿到大于等于C的是否是0/1
        new_predict_yprob_binary=np.array(new_predict_yprob_binary)
        new_test_y_binary=np.array(new_test_y_binary)
        # print("new_predict_yprob_binary[:4]:", new_predict_yprob_binary[:4])
        # print("new_test_y_binary[:4]:", new_test_y_binary[:4])


        BS=brier_score_loss(new_test_y_binary,new_predict_yprob_binary,pos_label=1)     ##以下代码块是计算BS得分和BSS得分！
        print("BS:",BS)
        y_mean=new_test_y_binary.mean()
        temp=0
        for i in range(len(new_test_y_binary)):
            temp+=((new_test_y_binary[i]-y_mean)*(new_test_y_binary[i]-y_mean))/len(new_test_y_binary)
        BSS=1-BS/temp
        print("BSS:",BSS)

        return  BS,BSS
    def HSS(self):
        P = self.TP() + self.FN()
        N = self.TN() + self.FP()
        up = 2 * (self.TP() * self.TN() - self.FN() * self.FP())
        below = P * (self.FN() + self.TN()) + N * (self.TP() + self.FP())
        return up / (below + sys.float_info.epsilon)

    def FAR(self):  ###12/11新加
        return self.FP() / (self.FP() + self.TP() + sys.float_info.epsilon)
