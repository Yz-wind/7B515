"""
Author: 邹致远
Email: www.pisyongheng@foxmail.com
Date Created: 2023/11/3
Last Updated: 2023/11/3
Version: 1.0.0
"""
import numpy as np

class DecisionNode:
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, info_gain=None, value=None):
        #对于决策节点
        self.feature_index = feature_index#特征下标
        self.threshold = threshold#阈值
        self.left = left#左子树
        self.right = right#右子树
        self.info_gain = info_gain#信息增益

        #对于叶子节点
        self.value = value#值

class DescisionTreeClassfier:
    def __init__(self, min_samples_split=2, max_depth=2):
        #初始化根节点
        self.root = None

        #停止条件
        self.min_samples_split = min_samples_split#最小样本区分
        self.max_depth = max_depth#最大深度

    def build_tree(self, dataset, curr_depth=0):
        X, Y = dataset[:, :-1], dataset[:, -1]#X为0-倒数第2列，Y为最后一列
        num_samples, num_features = np.shape(X)#样本数量为行，特征数量为列

        #分裂直至满足条件
        if num_samples >= self.min_samples_split and curr_depth <= self.max_depth:#判断推出条件
            best_split = self.get_best_split(dataset, num_samples, num_features)#最好的一个分裂规则
            if best_split["info_gain"]>0:#如果最好地分裂规则的信息增益>0
                left_subtree = self.build_tree(best_split["dataset_left"], curr_depth+1)#构建左子树
                right_subtree = self.build_tree(best_split["dataset_right"], curr_depth+1)#构建右子树
                return DecisionNode(best_split["feature_index"], best_split["threshold"], left_subtree, right_subtree, best_split["info_gain"])#返回当前节点

        leaf_value = self.calculate_leaf_value(Y)#计算叶子节点的值
        return DecisionNode(value= leaf_value)#返回叶子节点

    def get_best_split(self, dataset, num_samples, num_features):
        best_split = {}#存储最好的分裂策略
        max_info_gain = -float("inf")#最大的信息增益初始化为负无穷

        for feature_index in range(num_features):#对特征进行遍历
            feature_values = dataset[:, feature_index]#得到当前特征列
            possible_thresholds = np.unique(feature_values)#找出该特征列中的所有唯一值作为可能的分隔阈值
            for threshold in possible_thresholds:#遍历这些可能的阈值
                dataset_left, dataset_right = self.split(dataset, feature_index, threshold)#分隔
                if len(dataset_left) > 0 and len(dataset_right) > 0:#检查分割后的左右子集是否都不为空
                    y, left_y, right_y = dataset[:, -1], dataset_left[:, -1], dataset_right[:, -1]#提取出原始数据集的目标变量列，以及分割后左右子集的目标变量列
                    curr_info_gain = self.information_gain(y, left_y, right_y)#计算当前分隔策略下的信息增益
                    if curr_info_gain > max_info_gain:#如果当前分割的信息增益大于目前为止记录的最大信息增益
                        best_split["feature_index"] = feature_index#更新 best_split 字典，记录下当前的最优分割策略：最优特征索引，最优阈值，左右子集以及信息增益值
                        best_split["threshold"] = threshold
                        best_split["dataset_left"] = dataset_left
                        best_split["dataset_right"] = dataset_right
                        best_split["info_gain"] = curr_info_gain
                        max_info_gain = curr_info_gain
        return best_split#返回最优分配的字典

    def split(self, dataset, feature_index, threshold):
        dataset_left = np.array([row for row in dataset if row[feature_index] <= threshold])#按照阈值分隔数据集
        dataset_right = np.array([row for row in dataset if row[feature_index] > threshold])
        return dataset_left, dataset_right#范围左子树数据集和右子树数据集

    def information_gain(self, parent, l_child, r_child):
        weight_l = len(l_child) / len(parent)#计算左子树比例
        weight_r = len(r_child) / len(parent)#计算右子树比例
        gain = self.entropy(parent) - (weight_l * self.entropy(l_child) + weight_r * self.entropy(r_child))#计算信息增益
        return gain

    def entropy(self, y):#计算熵值
        class_labels = np.unique(y)#取得所有y的取值
        entropy = 0#初始化熵值
        for cls in class_labels:#遍历
            p_cls = len(y[y == cls]) / len(y)#求pi
            entropy += -p_cls * np.log2(p_cls)#计算熵值-pilogpi
        return entropy

    def calculate_leaf_value(self, Y):#计算叶子值
        Y = list(Y)
        return max(Y, key=Y.count)#返回出现数量最多的Y

    def fit(self, X, Y):#训练
        dataset = np.concatenate((X, Y.reshape(-1, 1)), axis=1)
        self.root = self.build_tree(dataset)

    def predict(self, X):#预测
        preditions = [self.make_prediction(x, self.root) for x in X]
        return preditions

    def make_prediction(self, x, tree):#预测函数
        if tree.value != None: return tree.value#如果数非空返回数的value属性
        feature_val = x[tree.feature_index]
        if feature_val <= tree.threshold:#如果特征值小于阈值
            return self.make_prediction(x, tree.left)#走左子树
        else:
            return self.make_prediction(x, tree.right)#走右子树

if __name__ == '__main__':
    # 加载数据集
    # 这里为了演示，我们手动创建一个小型数据集，假设已经加载并准备好。
    # 在实际应用中，您可能需要从CSV文件或其他源加载数据。
    X = np.array([[1, 1],
                  [1, 0],
                  [0, 1],
                  [0, 0]])
    Y = np.array([1,
                  1,
                  0,
                  0])

    # 创建决策树分类器实例
    classifier = DescisionTreeClassfier(min_samples_split=1, max_depth=2)

    # 拟合模型
    classifier.fit(X, Y)

    # 制作预测
    X_test = np.array([[1, 1], [0, 0]])
    predictions = classifier.predict(X_test)

    print(predictions)