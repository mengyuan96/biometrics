#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Tools to calculate distance between feature vectors, calculate ROC and CMC.

@author: Shiyu Luo
"""

import numpy as np
from sklearn.neighbors import NearestNeighbors

def distance(v1, v2):
    '''
    Calculates l2 distance (euclidean distance) between v1 and v2
    Parameters:
        - v1: feature vector, numpy array, shape(n_feature,)
        - v2: feature vector, numpy array, shape(n_features,)
        must be of same length.
    Return:
        - dist: euclidean distance betweenapr v1 and v2
    '''

    return np.linalg.norm((v1 - v2))
    

def match_against(p, gallery):
    '''
    Calculates the distance between p and each subject in gallery.
    Parameters:
        - p: feature vector of a probe, shape(n_features,)
        - gallery: feature vectors of gallery subjects, shape(n_subjects, n_features)
    Returns:
        - distances: distances between p and each row in gallery, numpy array, shape(n_subjects,)
    '''
    def distant_wrapper(g):
        return distance(p, g)
    return np.apply_along_axis(func1d=distant_wrapper, axis=1, arr=gallery)

def distances(gallery, probes):
    '''
    
    Returns:
        a n_subjects-by-n_subjects 2d numpy array, where the element at row i and column j is the
        distance between probe subject i and gallery subject j.
    '''
    def match_against_wrapper(p):
        return match_against(p, gallery)
    return np.apply_along_axis(func1d=match_against_wrapper, axis=1, arr=probes)
    

def compute_genuine_scores(distances):
    return np.diagonal(distances)

def compute_imposter_scores(distances):
    flat = np.ravel(distances)
    # get indices of diagonal elements
    n_subjects = distances.shape[0]
    ind = [(n_subjects + 1) * i for i in range(n_subjects)]
    # extract diagonal elements
    mask = np.ones(len(flat), dtype=bool)
    mask[ind] = False
    result = flat[mask]
    return result

def compute_genuine_and_imposter_scores(gallery, probes):
    '''
    Computes genuine scores and imposter scores.
    Parameters:
        - gallery: feature vectors of gallery subjects, numpy array, shape(n_subjects, n_features)
        - probes: feature vectors of probes, numpy array, shape(n_subjects, n_features)
    Returns:
        - genuine_scores: an array of genuine scores, numpy array, shape(n_subjects,)
        - imposter_scores: an array of imposter scores, numpy array, shape(n_subjects, )
    '''
    
    print 'computing distance matrix...'
    distance_mat = distances(gallery, probes)
    print 'done.'
    np.save('distance_matrix', distance_mat)

    print 'computing genuine scores...'
    genuine_scores = compute_genuine_scores(distance_mat)
    np.save('genuine_scores', genuine_scores)
    print 'done.'
    

    print 'computing imposter scores...'
    imposter_scores = compute_imposter_scores(distance_mat)
    np.save('imposter_scores', imposter_scores)
    print 'done.'
    
    return genuine_scores, imposter_scores


def rates(genuine_scores, imposter_scores, threshold):
    # false positive rates and false positive rates
   
    n_trueclaims = len(genuine_scores)
    n_falseclaims = len(imposter_scores)
    
    mask = np.zeros((n_trueclaims,))
    mask[np.where(genuine_scores < threshold)] = 1
    n_tp = np.sum(mask)
    
    mask = np.zeros((n_falseclaims,))
    mask[np.where(imposter_scores < threshold)] = 1
    n_fp = np.sum(mask)

    tpr = float(n_tp) / n_trueclaims
    fpr = float(n_fp) / n_falseclaims
    
    return fpr, tpr

def roc(genuine_scores, imposter_scores, n_thresholds, min_threshold, max_threshold):
    '''
    Calculates true positive rates and false positive rates.
    Parameters:
        - genuine_scores: genuine scores, numpy array, shape(n_subjects, )
        - imposter_scores: imposter scores, numpy array, shape(n_subjects,)
        - n_thresholds: number of intervals between <min_threshold> and <max_threshold>, int
        - min_threshold: lowerbound of thresholds, int
        - max_threshold: upperbound of thresholds, int
    Returns:
        - fprs: false positive rates, numpy array, shape(n_thresholds,)
        - tprs: true positive rates, numpy array, shape(n_thresholds,)
    '''

    thresholds = np.linspace(min_threshold, max_threshold, n_thresholds)
    print thresholds
    tprs = []
    fprs = []
    for t in thresholds:
        fpr, tpr = rates(genuine_scores, imposter_scores, t)
        tprs.append(tpr)
        fprs.append(fpr)
        
    return fprs, tprs

    
def cmc(gallery, probes):
    '''
    Computes CMC match rates.
    Parameters:
        - gallery: feature vectors of gallery subjects, numpy array, shape(n_subjects, n_features)
        - probes: feature vectors of probes, numpy array, shape(n_subjects, n_features)
    Returns:
        - match_rates: numpy array, match_rates[n] = match rate of top (n+1) match
    '''
    
    # number of subjects in gallery
    print gallery.shape
    print probes.shape
    N = gallery.shape[0]
    P = probes.shape[0]
    
    match_rates = []
    for n in range(1, N+1):
        # how many matches
        num_matches = 0
        
        nrbs = NearestNeighbors(n_neighbors=n, algorithm='kd_tree', metric='euclidean')
        nrbs.fit(gallery)
        # returned_ids: shape(P, n)
        returned_ids = nrbs.kneighbors(probes, return_distance=False)
        
        for p in range(P):
            if p in returned_ids[p]:
                num_matches += 1
                
        match_rate = num_matches / float(P)
        match_rates.append(match_rate)
        
    np.save('cmc.npy', match_rates)
    return np.array(match_rates)


    


    