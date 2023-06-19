"""
DeepLabCut generate .csv and .h5
Authors: Dongsheng Xiao
"""
import glob
import os
import cv2
import pandas as pd
import skimage.io as io

coords_input = 'E://3Dmicedata//DLC_input//CollectedData_DongshengXiao.csv'
output_path = 'E://3Dmicedata//DLC_output'

coords = pd.read_csv(coords_input, header=[0, 1, 2], index_col=[0])

# Adapted from DeepLabCut (to facilitate conversion to DLC-compatible format):
# https://github.com/DeepLabCut/DeepLabCut/blob/master/deeplabcut/generate_training_dataset/labeling_toolbox.py
coords.to_csv(os.path.join(output_path, '{}.csv'.format(os.path.basename(coords_input).split('.')[0])))
coords.to_hdf(os.path.join(output_path, '{}.h5'.format(os.path.basename(coords_input).split('.')[0])),
                    'df_with_missing', format='table', mode='w')
