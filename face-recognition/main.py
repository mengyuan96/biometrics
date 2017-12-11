#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 10:16:53 2017

@author: Shiyu Luo
"""

import data_preparation
import eigenface
import generate
import face_utils
import numpy as np
import os.path
import shutil
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import Series, DataFrame
import pandas as pd

def main():
    n_eigenvects = 100
    csv_path = 'neutral.csv'
    training_dir = 'training_data'
    testing_dir = 'testing_data'
    
    # prepare data
    #data_preparation.batch_nef2jpg(nef_dir, csv_path, training_dir, testing_dir)
    
    # iterate over training_data to create gallery_images
    cnt = 0
    subjects = os.listdir(training_dir)
    gallery_images = dict()
    for subject in subjects:
        if subject.startswith('9'):
            subject_folder_path = os.path.join(training_dir, subject)
            imgs = os.listdir(subject_folder_path)
            for img in imgs:
                if img.startswith('9'):
                    if cnt < 50:
                        img_path = os.path.join(subject_folder_path, img)
                        gallery_images[subject] = img_path
                        cnt += 1
    
    # iterate over testing_data to create probe_images
    cnt = 0
    subjects = os.listdir(testing_dir)
    probe_images = dict()
    for subject in subjects:
        if subject.startswith('9'):
            subject_folder_path = os.path.join(testing_dir, subject)
            imgs = os.listdir(subject_folder_path)
            for img in imgs:
                if img.startswith('9'):
                    if cnt < 50:
                        img_path = os.path.join(subject_folder_path, img)
                        probe_images[subject] = img_path
                        cnt += 1
            
    #train eigenface model
    mean_face, eigenvects = eigenface.RecognitionVector(gallery_images, k=n_eigenvects)

    # create gallery and probes
    gallery, probes = generate.gallery_and_probes(gallery_images, probe_images, eigenface.featureVect, mean_face, eigenvects, n_eigenvects=n_eigenvects)
    
    # genuine and imposter distribution
    genuine_scores, imposter_scores = face_utils.compute_genuine_and_imposter_scores(gallery, probes)
    
    # plot distribution
    Distribution_Plot(genuine_scores, imposter_scores)

    # plot ROC
    ROC_plot(genuine_scores, imposter_scores)
    
    # calculate cmc match rates
    cmc = face_utils.cmc(gallery, probes)

    # plot CMC
    rank = np.linspace(1,len(cmc), 50)
    CMC = CMC_plot(cmc, rank)

def Distribution_Plot(gen, imp):
    fig = plt.figure()

    # set up for distribution plot
    plt.ylabel("Density", fontsize=14)
    plt.title("Genuine and Imposter Distribution ", fontsize=14)


    # add Distribution
    sns.distplot(gen)
    sns.distplot(imp)
    
    # save distribution
    plt.tight_layout()
    plt.xlim(0, 7000)
    plt.ylim(0, 0.0006)
    plt.legend(fontsize=10, loc='best')
    plt.savefig('Distribution.jpg')
 

def CMC_plot(cmc, rank):
    
    # set up for CMC plot
    fig = plt.figure()
    plt.xlabel("Rank Counted as Recognition", fontsize=14)
    plt.ylabel("Recognition Rate", fontsize=14)
    plt.title("CMC Curve", fontsize=14)
    
    # add CMC curve  
    plt.plot(rank, cmc,  color='r', label='CMC')
    
    #save CMC curve plot
    plt.xlim(0.0, max(rank))
    plt.ylim(0.0, 1.0)
    plt.legend(fontsize=10, loc='best')
    plt.tight_layout()
    plt.savefig('CMC.jpg')

def ROC_plot(gen, imp):
    
    fig = plt.figure()
    # set up for ROC plot
    plt.xlabel("FPR", fontsize=14)
    plt.ylabel("TPR", fontsize=14)
    plt.title("ROC Curve", fontsize=14)
    
    # add ROC curve
    tpr, fpr = GetRates(gen, imp)
    plt.plot(fpr, tpr, color='k', linewidth=2, label='ROC')
    
    # add a random line    
    x = [0.0, 1.0]
    plt.plot(x, x, linestyle='dashed', color='red', linewidth=2, label='random')

    #save ROC curve plot
    plt.xlim(0.0, 1.0)
    plt.ylim(0.0, 1.0)
    plt.legend(fontsize=10, loc='best')
    plt.tight_layout()
    plt.savefig('roc.jpg')
    

def GetRates(gen, imp):

    tpr = [0.0]  # true positive rate
    fpr = [0.0]  # false positive rate
        
    T = Threshold()
    
    for t in T:       
        true_claim = 0.0
        false_claim = 0.0
        for s in gen:
            if s < t:
                true_claim += 1.0
                
        for s in imp:
            if s < t:
                false_claim += 1.0

        tpr.append(true_claim / float(len(gen)))
        fpr.append(false_claim / float(len(imp)))

    return tpr, fpr

def Threshold():
    return np.linspace(0,6000,100)
    
main()