import rospkg

import numpy as np
import cv2
import caffe

class neural_net(object):
    def __init__(self):
        self.prefix = ''
        self.dir_path = ''
        self.deploy_path = ''
        self.weights_path = ''

        self.prepare_paths()
        self.caffe_net = caffe.Net(self.deploy_path, self.weights_path, caffe.TEST)

        self.words_list = []
        self.parse_words_file()
        pass

    def prepare_paths(self):
        self.rospack = rospkg.RosPack()
        self.prefix = self.rospack.get_path('caffe_deep_cnn_test')
        self.dir_path = '/home/msdu/learning/caffe-master/models'

        self.deploy_path = self.dir_path + '/vgg16/deploy.prototxt'
        self.weights_path = self.dir_path + '/vgg16/weights.caffemodel'
        pass
    def parse_words_file(self):
        words_path = self.prefix + '/synset/synset_words.txt'
        words_file = open(words_path, 'r')
        wnids_to_words = {}
        i = 1
        for line in words_file.readlines():
            pairs = line.split(' ')
            pair = {pairs[0] : pairs[1:]}
            wnids_to_words[i] = pair
            i += 1
            pass
        self.words_list = wnids_to_words
        pass
    def forward_pass(self, image):
        self.set_gpu_mode(False)

        in_ = self.prepare_image(image)

        self.caffe_net.blobs['data'].reshape(1, *in_.shape)
        self.caffe_net.blobs['data'].data[...] = in_
        self.out = self.caffe_net.forward()
        pass

    def get_words(self):
        scores = self.out['prob']
        #print scores
        top5indicies = self.getTop5indicies(scores) + 0
        top5pairs = []
        print "Top 5 prediction:"
        for i in xrange(1):
            top5pairs.append(self.words_list[top5indicies[i]])
            if (i == 0):
		print "FIRST prediction: ", self.words_list[top5indicies[i]], "with score: ", scores[0, top5indicies[i]]
	    else:
		print self.words_list[top5indicies[i]], "with score: ", scores[0, top5indicies[i]]
            pass
        pass

    def getTop5indicies(self, array_in):
        array = np.copy(array_in)
        indicies = np.zeros(5, int)
        for i in xrange(5):
            idx = np.argmax(array)
            indicies[i] = idx
            array[0, idx] = 0
        return indicies

    def prepare_image(self, image):
        image = self.first_resize(image)
        image = self.crop(image)
        image = self.second_resize(image)

        # image = self.rotate_image(image)

        in_ = np.array(image, dtype=np.float32)
        in_ = self.substract_mean_pixel(in_)
        in_ = in_.transpose((2, 0, 1))
        return in_

    def first_resize(self, image):
        h, w, c = image.shape
        if h < w:
            image = cv2.resize(image, (256 * w / h, 256), interpolation=cv2.INTER_CUBIC)
            pass
        elif h >= w:
            image = cv2.resize(image, (256, 256 * h / w), interpolation=cv2.INTER_CUBIC)
            pass
        return image
        pass

    def crop(self, image):
        h, w, c = image.shape
        hs = (h - 224) / 2
        ws = (w - 224) / 2
        image = image[hs:hs + 224, ws:ws + 224, :]
        return image
        pass

    def second_resize(self, image):
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_CUBIC)
        return image
        pass

    def substract_mean_pixel(self, image):
        mean_pixel = [103.939, 116.779, 123.68]
        for c in range(3):
            image[:, :, c] = image[:, :, c] - mean_pixel[c]
            pass
        return image

    def set_gpu_mode(self, mode):
        if mode:
            caffe.set_device(0)
            caffe.set_mode_gpu()
        else:
            caffe.set_device(0)
            caffe.set_mode_cpu()
        pass
class vgg16(neural_net):
    def prepare_paths(self):
        self.rospack = rospkg.RosPack()
        self.prefix = self.rospack.get_path('caffe_deep_cnn_test')
        self.dir_path = '/home/msdu/learning/caffe-master/models'

        self.deploy_path = self.dir_path + '/vgg16/deploy.prototxt'
        self.weights_path = self.dir_path + '/vgg16/weights.caffemodel'
        pass

    pass
class googlenet(neural_net):
    def prepare_paths(self):
        self.rospack = rospkg.RosPack()
        self.prefix = self.rospack.get_path('caffe_deep_cnn_test')
        self.dir_path = '/home/msdu/learning/caffe-master/models'

        self.deploy_path = self.dir_path + '/googlenet/deploy.prototxt'
        self.weights_path = self.dir_path + '/googlenet/weights.caffemodel'
        pass
    pass
class caffenet(neural_net):
    def prepare_paths(self):
        self.rospack = rospkg.RosPack()
        self.prefix = self.rospack.get_path('caffe_deep_cnn_test')
        self.dir_path = '/home/msdu/learning/caffe-master/models'

        self.deploy_path = self.dir_path + '/caffenet/deploy.prototxt'
        self.weights_path = self.dir_path + '/caffenet/caffenet_train_iter_300.caffemodel'
        pass
    pass
    def parse_words_file(self):
        words_path = self.prefix + '/synset/words_list.txt'
        words_file = open(words_path, 'r')
        wnids_to_words = {}
        i = 1
        for line in words_file.readlines():
            pairs = line.split(' ')
            pair = {pairs[0] : pairs[1:]}
            wnids_to_words[i] = pair
            i += 1
            pass
        self.words_list = wnids_to_words
        pass
class fcn8s(neural_net):
    def prepare_paths(self):
        self.rospack = rospkg.RosPack()
        self.prefix = self.rospack.get_path('caffe_deep_cnn_test')
        self.dir_path = '/home/msdu/learning/caffe-master/models'

        self.deploy_path = self.dir_path + '/fcn8s/deploy.prototxt'
        self.weights_path = self.dir_path + '/fcn8s/weights.caffemodel'
        pass
    def first_resize(self, image):
        return image
    def crop(self, image):
        return image
    def second_resize(self, image):
        image = cv2.resize(image, (375, 500), interpolation=cv2.INTER_CUBIC)
        return image
    def substract_mean_pixel(self, image):
        mean_pixel = [104.007, 116.669, 122.68]
        for c in range(3):
            image[:, :, c] = image[:, :, c] - mean_pixel[c]
            pass
        return image
    pass

