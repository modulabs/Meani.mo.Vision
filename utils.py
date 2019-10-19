import os, sys
import cv2
import numpy as np

def makedirs(path):
    # Intended behavior: try to create the directory,
    # pass if the directory exists already, fails otherwise.
    # Meant for Python 2.7/3.n compatibility.
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

class ResultWriter:
    
    # 초기자(initializer)
    def __init__(self, args):

        self.common_args = {
        'experiment_num': args.experiment_num,
        'drone_folder_path': args.drone_folder_path,

        'save_csv': args.save_csv,
        'save_video': args.save_video,

        'save_masked_pcl': args.save_masked_pcl,
        'save_masked_drone': args.save_masked_drone,
        'save_matching': args.save_matching,
        'save_keypoints': args.save_keypoints
        }
    
        dataSetStr = os.path.basename(os.path.normpath(self.common_args['drone_folder_path']))
        self.dst_path = os.path.join('./', 'experiment' + str(self.common_args['experiment_num']) + '_' + dataSetStr)
        makedirs(self.dst_path)

        if self.common_args['save_csv'] is True:
            self.f = open(os.path.join(self.dst_path, 'result.csv'),'w')

        if self.common_args['save_video'] is True:
            video_size = (3000, 3000)
            fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            video_dst = os.path.join(self.dst_path, 'output.avi')
            self.vid = cv2.VideoWriter(video_dst, fourcc, 1, video_size, True, )

    def __del__(self):    
        if self.common_args['save_csv'] is True:
            self.f.close()

        if self.common_args['save_video'] is True:
            self.vid.release()

    # 메서드
    def saveResults(self, result, idx):
        cv2.imwrite(os.path.join(self.dst_path, 'result_' + str(idx) + '.jpg'), result['image'])

        if self.common_args['save_csv'] is True:
            print("save_csv")
            data = "Num, %d\n" % idx
            self.f.write(data)

            np.savetxt(self.f, result['homography'], delimiter=",")

            det = np.linalg.det(result['homography'])
            data = "Det, %f\n" % det
            self.f.write(data)

            x = result['homography'][0][0]
            y = result['homography'][1][1]
            ratio = x/y
            data = "ratio, %f\n\n" % ratio
            self.f.write(data)

            drone_total_keypoints = result['drone_total_keypoints']
            data = "drone_total_keypoints, %d\n" % drone_total_keypoints
            self.f.write(data)

            pcl_total_keypoints = result['pcl_total_keypoints']
            data = "pcl_total_keypoints, %d\n" % pcl_total_keypoints
            self.f.write(data)

            num_inliers = result['num_inliers']
            data = "num_inliers, %d\n" % num_inliers
            self.f.write(data)

            num_raw_matches = result['num_raw_matches']
            data = "num_raw_matches, %d\n" % num_raw_matches
            self.f.write(data)

            num_good_matches = result['num_good_matches']
            data = "num_good_matches, %d\n" % num_good_matches
            self.f.write(data)

           
        if self.common_args['save_video'] is True:
            print("save_video")
            self.vid.write(cv2.resize(result['image'], (3000, 3000)))

        if self.common_args['save_masked_pcl'] is True:
            print("save_masked_pcl")
            cv2.imwrite(os.path.join(self.dst_path, 'masked_pcl.jpg'), result['masked_pcl'])
            
    
        if self.common_args['save_masked_drone'] is True:
            print("save_masked_drone")
            cv2.imwrite(os.path.join(self.dst_path, 'masked_drone_' + str(idx) + '.jpg'), result['masked_drone'])
            
        
        if self.common_args['save_matching'] is True:
            print("save_matching")
            cv2.imwrite(os.path.join(self.dst_path, 'matching1_' + str(idx) + '.jpg'), result['matching1'])
            cv2.imwrite(os.path.join(self.dst_path, 'matching2_' + str(idx) + '.jpg'), result['matching2'])
            cv2.imwrite(os.path.join(self.dst_path, 'matching3_' + str(idx) + '.jpg'), result['matching3'])
            

        if self.common_args['save_keypoints'] is True:
            print("save_keypoints")
            cv2.imwrite(os.path.join(self.dst_path, 'keypoints_lidar.jpg'), result['keypoints_lidar_image'])
            cv2.imwrite(os.path.join(self.dst_path, 'keypoints_drone_' + str(idx) + '.jpg'), result['keypoints_drone_image'])
            
        return print("save done")
