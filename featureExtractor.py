import cv2

FETURE_EXTRACTORS = ['SIFT']


class FeatureExtractor:

    def __init__(self, src, algorithm, mask=None):

        self._extractor = self._select_algorithm(algorithm)
        self._src_image = src

    def _select_algorithm(self, algorithm):
        assert(algorithm in FETURE_EXTRACTORS)

        if(algorithm == 'SIFT'):
            return cv2.xfeatures2d.SIFT_create()
            # return cv2.xfeatures2d.SIFT_create(edgeThreshold=0)

    def compute(self, mask=None):
        self.features, self.descriptors = self._extractor.detectAndCompute(
            self._src_image, mask)

    def get_features_and_descriptors(self):
        return self.features, self.descriptors
