import tensorflow as tf

class Network:
    def __int__(self):
        self.learning_rate = 0.001

        self.x = tf.placeholder(tf.float32, [None, 784])

        self.label = tf.placeholder(tf.float32, [None, 10])

        self.w = tf.Variable(tf.zeros([784,10]))

        self.b = tf.Variable(tf.zeros[10])

        self.y = tf.nn.softmax(tf.matmul(self.x, self.w) + self.b)

        self.loss = -tf.reduce_sum(self.label * tf.log(self.y + 1e-10))

        self.train = tf.train.GradientDescentOptimizer(self.learning_rate).minimize(self.loss)

        # 以下代码验证正确率时使用
        # argmax 返回最大值的下标，最大值的下标即答案
        # 例如 [0,0,0,0.9,0,0.1,0,0,0,0] 代表数字3
        predict = tf.equal(tf.argmax(self.label, 1), tf.argmax(self.y, 1))

        # predict -> [true, true, true, false, false, true]
        # reduce_mean即求predict的平均数 即 正确个数 / 总数，即正确率
        self.accuracy = tf.reduce_mean(tf.cast(predict, "float"))