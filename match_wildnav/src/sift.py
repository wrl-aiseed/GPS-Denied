import cv2 
from matplotlib import pyplot as plt
import numpy as np
import os 
import math
import time
import csv

sift = cv2.xfeatures2d.SIFT_create()
input_folder = '../dataset/query/'
input_name = 'input.png'
sat_folder = '../dataset/georeference/'
sat_name = 'sat_patch_0001.png'

# image_folder = '../dataset/georeference/'
# for i in range(0, 35):
#     num = ""
#     if i<10:
#         num += '0' + str(i)
#     else:
#         num += str(i)
#     image_name = f'sat_patch_00{num}.png'

#     image = cv2.imread(image_folder + image_name, cv2.IMREAD_GRAYSCALE)

#     sift = cv2.SIFT_create()
#     kp, dc = sift.detectAndCompute(image, None)
#     output_image = cv2.drawKeypoints(image, kp, None)

#     cv2.imshow('SIFT Keypoints, ', output_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

def getMatchNum(matches,ratio):
    '''返回特徵點匹配數量和matchesMask'''
    matchesMask=[[0,0] for i in range(len(matches))]
    matchNum=0
    for i,(m,n) in enumerate(matches):
        if m.distance<ratio*n.distance:
            matchesMask[i]=[1,0]
            matchNum+=1
    return (matchNum,matchesMask)

comparisonImageList = []
time_match_ratio = [['Execution Time', 'Match Ratio']]
#建立FLANN匹配對象
FLANN_INDEX_KDTREE=0
indexParams=dict(algorithm=FLANN_INDEX_KDTREE,trees=5)
searchParams=dict(checks=50)
flann=cv2.FlannBasedMatcher(indexParams,searchParams)

for i in range(0, 38): 
    start_time = time.perf_counter()
    num = str(i)
    if i < 10:
        num = '0' + num
    sat_name = f'sat_patch_00{num}.png'
    sat_image = sat_folder + sat_name
    sampleImage=cv2.imread(sat_image,0)
    kp1, des1 = sift.detectAndCompute(sampleImage, None)

    queryImage=cv2.imread(input_folder + input_name,0)
    kp2, des2 = sift.detectAndCompute(queryImage, None)

    matches=flann.knnMatch(des1,des2,k=2) 
    (matchNum,matchesMask)=getMatchNum(matches,0.9)
    matchRatio=matchNum*100/len(matches)
    drawParams=dict(matchColor=(0,255,0),
                    singlePointColor=(255,0,0),
                    matchesMask=matchesMask,
                    flags=0)

    comparisonImage=cv2.drawMatchesKnn(sampleImage,kp1,queryImage,kp2,matches,None,**drawParams)
    comparisonImageList.append((comparisonImage,matchRatio)) 
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"At {sat_name}, execution time (high precision): {execution_time:.6f} seconds, match ratio: {round(matchRatio, 2)}%")
    time_match_ratio.append([execution_time, matchRatio])
# print(sat_name)
# figure,ax=plt.subplots()
# for index,(image,ratio) in enumerate(comparisonImageList):
    # ax.set_title('Similiarity %.2f%%' % ratio)
    # print(ratio, '%')
    # ax.imshow(image)
    # print(ratio)
    # lines = ratio.split('\n')
    # print(lines[-1], '%')
# plt.tight_layout()  # Adjust layout
# plt.show()

# Write to a CSV file with quotes around strings
with open("time_match_ratio_data.csv", mode="w", newline="") as file:
    writer = csv.writer(file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerows(time_match_ratio)

print("CSV file with quoted strings has been written successfully.")