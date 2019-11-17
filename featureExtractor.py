import cv2
import numpy as np

FETURE_EXTRACTORS = ['SIFT']


class FeatureExtractor:

    def __init__(self, src, algorithm, args):
        self.common_args = {
            'SIFT_nfeatures': args.SIFT_nfeatures,
            'SIFT_nOctaveLayers': args.SIFT_nOctaveLayers,
            'SIFT_contrastThreshold': args.SIFT_contrastThreshold,
            'SIFT_edgeThreshold': args.SIFT_edgeThreshold,
            'SIFT_sigma': args.SIFT_sigma
        }
        self._extractor = self._select_algorithm(algorithm)
        self._src_image = src

    def _select_algorithm(self, algorithm):
        assert(algorithm in FETURE_EXTRACTORS)

        if(algorithm == 'SIFT'):
            return cv2.xfeatures2d.SIFT_create(
                nfeatures=self.common_args['SIFT_nfeatures'],
                nOctaveLayers=self.common_args['SIFT_nOctaveLayers'],
                contrastThreshold=self.common_args['SIFT_contrastThreshold'],
                edgeThreshold=self.common_args['SIFT_edgeThreshold'],
                sigma=self.common_args['SIFT_sigma']
            )

    def compute(self, mask=None):
        print(mask.shape)
        print(np.max(mask))
        self.features, self.descriptors = self._extractor.detectAndCompute(
            self._src_image, mask)

    def get_features_and_descriptors(self):
        return self.features, self.descriptors
