#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Generates gallery and probes.

@author: Shiyu Luo
"""
import numpy as np
import eigenface

def gallery_and_probes(gallery_images, probe_images, get_rep, mean_face, eigenvects, n_eigenvects):
    '''
    Generates a gallery.
    Parameters:
        - gallery_images: a dictionary, keys = subject id, vals = path of image to use.
        - get_rep: function to get feature vector of an image
        - eigenvects: eigenvectors of training images
        - mean_face: mean face of training images
        - n_eigenvects: number of eigenvectors to represent the image space
    Returns:
        - gallery: feature vectors of gallery subjects, numpy array, shape(n_subjects, n_features)
        - probes: feature vectors of probe subjects, numpy array, shape(n_subjects, n_features)
    '''
    def get_feature_vector(img_path):
        # a wrapper of get_rep
        return get_rep(img_path, mean_face, eigenvects)
    
    gallery = np.zeros((1, n_eigenvects))
    probes = np.zeros((1, n_eigenvects))
    for subject in gallery_images.keys():
        feature_vector = get_feature_vector(gallery_images[subject])
        gallery = np.concatenate((gallery, feature_vector), axis=0)
        
    gallery = gallery[1:, :]
    np.save('gallery', gallery)
    
    for subject in probe_images.keys():
        feature_vector = get_feature_vector(probe_images[subject])
        probes = np.concatenate((probes, feature_vector), axis=0)

    probes = probes[1:, :]
    np.save('probes', probes)
    
    return gallery, probes



        
    
    