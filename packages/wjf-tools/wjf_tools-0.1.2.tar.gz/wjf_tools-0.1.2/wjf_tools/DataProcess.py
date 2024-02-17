import numpy as np
import pandas as pd
from tensorflow.python.keras.utils.np_utils import to_categorical

class DataLoader(object):
    @staticmethod
    def get_labels_weight(every_class_num_list: list):
        """
        根据每个类样本数获取每个类的权重
        :param every_class_num_list:每个元素在类中的个数
        :return:返回的对应元素的权重列表（和传入列表顺序一致）
        """
        all_samples = 0
        num_classes = len(every_class_num_list)
        for i in every_class_num_list:
            all_samples += i
        weight_dir = {}
        index = 0
        for i in every_class_num_list:
            weight_dir[index] = all_samples / (i * num_classes)
            index += 1
        return weight_dir
    @staticmethod
    def rectify(y, timestep, label_num):
        """
        从标签数组中每隔特定时间步抽取一个样本，并调整形状以匹配标签数。

        Args:
            y (np.array): 原始标签数组。
            timestep (int): 抽取样本的时间步长。
            label_num (int): 标签的数量，用于重塑数组。

        Returns:
            np.array: 调整形状并抽取样本后的标签数组。
        """
        # 重塑y数组以适应期望的标签数量
        y_reshaped = y.reshape(-1, label_num)

        temp_y = []  # 用于存储抽取的样本
        # 使用循环每隔timestep抽取一个样本
        for i in range(0, y_reshaped.shape[0], timestep):
            temp_y.append(y_reshaped[i])

        # 将抽取的样本列表转换回np.array
        y_sampled = np.array(temp_y)

        return y_sampled

    @staticmethod
    def load_data(train_csv_path, validate_csv_path, test_csv_path, start_col, end_col, label_list):
        """
        Args:
            train_csv_path  validate_csv_path   test_csv_path:三个路径
            若干列字段	CLASS
            若干列数值      N
            startCol    endCol:选择那两列之间的数据，字符串代表字段名字
        Description:
            把输入进来的若干行，若干列标签进行提取，最后一列的文本类别进行独热编码
            同时进行计算每一个类别数量，调用GetClass为全局变量进行权重填充方便后续训练分配权重（类别数量不平衡）
            同时把NCMX每一类下标到哪位置填充到global c_index_end_list
        Returns:
            以train为例子：
            List[0] : [ [csv中第一行若干个数据],[...]，[csv中最后一行若干个数据] ]
            List[1] : [ [csv中第一标签编码],[...]，[csv中最后一行标签编码] ]
            ....
            class_counts 每一类的数目列表
        """

        pd.set_option('display.max_columns', None)
        data_list = []  # 用于存储x_train, y_train, x_validate, y_validate, x_test, y_test
        class_counts = [0] * len(label_list)  # 初始化每个类的计数

        for path in [train_csv_path, validate_csv_path, test_csv_path]:
            csv_data = pd.read_csv(path)
            # 计算开始和结束列的索引
            columns = csv_data.columns.values
            start_index = list(columns).index(start_col)
            end_index = list(columns).index(end_col) + 1  # 包含end_col

            # 选择指定列之间的数据
            selected_features = csv_data.iloc[:, start_index:end_index].values
            data_list.append(selected_features)

            # 处理标签列，进行独热编码
            labels = csv_data["CLASS"].copy()  # 假设标签列名为"CLASS"
            class_list = []  # 存储每个实例的类别编号

            for label in labels:
                for i, class_label in enumerate(label_list):
                    if label == class_label:
                        class_counts[i] += 1
                        class_list.append(i)
                        break

            # 转换类别编号为one-hot编码
            labels_one_hot = to_categorical(class_list, num_classes=len(label_list))
            data_list.append(labels_one_hot)

        # 解包列表以匹配返回值
        train_x, train_y, validate_x, validate_y, test_x, test_y = data_list

        return train_x, train_y, validate_x, validate_y, test_x, test_y, class_counts
        ##分别对应 train_x,train_y,validate_x,validate_y,test_x,test_y

    @staticmethod
    def GetTimeSeries(train_x, train_y, validate_x, validate_y, test_x, test_y, inputdim, timestep):
        """

        Args:
            train_x train_y validate_x validate_y test_x test_y:
            inputdim:输入维度
            timestep:时间步长
        Description:
            把csv读取的二维矩阵特征和二维矩阵热编码进行 时间窗口的划分
        Returns:

        """

        # train_x.shape : (62520, 10)
        train_x = train_x.reshape(-1, timestep, inputdim)
        # train_x.shape: (521, 120, 10)
        validate_x = validate_x.reshape(-1, timestep, inputdim)
        test_x = test_x.reshape(-1, timestep, inputdim)

        num_classes = train_y.shape[1]
        # (train_y.shape)(62520, 4)
        train_y = DataLoader.rectify(train_y, timestep, num_classes)
        # train_y.shape: (521, 4)
        validate_y = DataLoader.rectify(validate_y, timestep,num_classes)
        test_y = DataLoader.rectify(test_y, timestep,num_classes)


        return train_x, train_y, validate_x, validate_y, test_x, test_y