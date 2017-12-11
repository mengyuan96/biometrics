#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Data Preparation Module.

@author: Shiyu Luo
"""
import csv
import rawpy
from PIL import Image
import os.path
from random import sample
import shutil
import numpy as np
import sys

def nef2jpg(nef_file, jpg_dir):
    '''
    Converts <nef_file> to a .jpg file.
    Parameters:
        - nef_file: path to the .nef file
        - jpg_dir: directory under which the converted .jpg file to be placed
    Returns:
        path to the converted .jpg image
    '''
    if os.path.exists(nef_file) and os.path.isdir(jpg_dir):
        print 'nef2jpg:***processing {}***'.format(nef_file)
        raw = rawpy.imread(nef_file)
        rgb = raw.postprocess()
        print 'original size {}'.format(rgb.shape[:-1])
        rgb_img = Image.fromarray(rgb)
        maxsize = (50, 70)
        rgb_img.thumbnail(maxsize, Image.ANTIALIAS)
        print 'resize to {}'.format(rgb_img.size)
        jpg_path = os.path.join(jpg_dir, os.path.splitext(os.path.basename(nef_file))[0]) + '.jpg'
        rgb_img.save(jpg_path)
        #return jpg_path
    elif not os.path.exists(nef_file):
        raise Exception('{} does not exist'.format(nef_file))
    else:
        raise Exception('{} does not exist'.format(jpg_dir))


def batch_nef2jpg(nef_dir, csv_path, training_dir, testing_dir):
    '''
    Converts the .nef images specified by <csv_path> and place the converted
    images under <tiff_dir>.
    Parameters:
        - nef_dir: path of directory that contains .nef images
        - csv_path: path of .csv file that contains paths of images to convert
        - training_dir: path of directory that contains training data
        - testing_dir: path of directory that contains testing data
    Throw exception: if <nef_dir> does not exist, or <csv_path> does not
        exist, or <training_dir> or <testing_data> is not correctly created
    Return
        - subject_images: mapping subject
    '''
   
    # make training and testing directory
    if not os.path.isdir(training_dir):
        os.mkdir(training_dir)
    if not os.path.isdir(testing_dir):
        os.mkdir(testing_dir)
    
    if os.path.isdir(training_dir) and os.path.isdir(testing_dir):
        print 'created {} and {}.'.format(training_dir, testing_dir)
        
        # iterate over rows in <csv_path> to save image paths in dictionary subject_imgs
        subject_imgs = dict()
        with open(csv_path, 'r') as f:
            for line in f:
                # extract .nef path, e.g. 'face_data/90003/90003d1.nef'
                nef_img_path = (nef_dir + '/' + line.splitlines()[0]).split(',')[0]
                # extract subject id, e.g. '90003'
                img_subjectid = nef_img_path.split('/')[1]
                if img_subjectid not in subject_imgs:
                    subject_imgs[img_subjectid] = []
                subject_imgs[img_subjectid].append(nef_img_path)
        for key in subject_imgs.keys():
            print 'subject id: {}, images: {}\n'.format(key, subject_imgs[key])
            
        gallery_images = dict()
        probe_images = []
        probe_ids = []
        
        for key in subject_imgs.keys():
            nef_paths = subject_imgs[key]
            n_imgs = len(nef_paths)
            if n_imgs >= 2: # skip subjects with less than 2 images

                # randomly samples 2 images to serve as training and testing data
                rand_ind = sample(range(0, n_imgs), 2)
                training = nef_paths[rand_ind[0]]
                testing = nef_paths[rand_ind[1]]

                # create subfolder for each subject if subfolder does not exist
                training_subfolder = training_dir + '/' + key
                testing_subfolder = testing_dir + '/' + key
                if not os.path.isdir(training_subfolder):
                    os.mkdir(training_subfolder)
                if not os.path.isdir(testing_subfolder):
                    os.mkdir(testing_subfolder)

                print 'preparing data for subject {}...'.format(key)
                print 'converting {}...'.format(training)
                nef2jpg(training, training_subfolder)
                print 'done. save to {}.'.format(training_subfolder)
                print 'converting {}...'.format(testing)
                nef2jpg(testing, testing_subfolder)
                print 'done. save to {}.\n'.format(testing_subfolder)

        print '\nfinished preparing data.'
                
    else:
        raise Exception('Unable to create directory {} and {}.'.format(training_dir, testing_dir))
