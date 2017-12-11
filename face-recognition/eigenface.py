#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 21:32:11 2017

@author: xindahuang
"""
from numpy import *
from numpy import linalg as la  
import cv2  
import os
from scipy.linalg import eigh as largest_eigh
from scipy.sparse.linalg.eigen.arpack import eigsh as largest_eigsh

  
def loadImageSet(dictionary):  
    FaceMat = mat(zeros((len(dictionary),46*70)))  
    j =0  
    for i in dictionary:
        #dictionary is the gallery,key is subject,value is the path of image
        try:  
            img = cv2.imread(dictionary[i],0)  
        except:  
            print 'load %s failed'%i  
        FaceMat[j,:] = mat(img).flatten()  
        j += 1  
    return FaceMat  
  
def RecognitionVector(dictionary, k=50):
    # step1: load the face image data ,get the matrix consists of all image
    print 'loading training image data...'
    FaceMat = loadImageSet(dictionary) 
    print 'done.\n'
    
    # step2: average the FaceMat 
    print 'computing eigenvectors and eigenvalues...'
    meanface = mean(FaceMat,0) 
    normalizedface = FaceMat-meanface 
    covMat=cov(normalizedface,rowvar=0) 
    eigVals,eigVects=linalg.eig(mat(covMat))
    eigValIndice=argsort(eigVals)
    n_eigValIndice=eigValIndice[-1:-(k+1):-1]
    n_eigVect=eigVects[:,n_eigValIndice]
    print 'get eigvals'
    print 'done.'
    save('meanface-eig{}.npy'.format(k), meanface)
    save('eigenvectors-eig{}.npy'.format(k), eigVects)
    save('eigenvalues-eig{}.npy'.format(k), eigVals)
    print 'saved to file.\n'
    
    return meanface,n_eigVect

def featureVect(imgpath, meanface, eigVects):
    print 'read image {}...'.format(imgpath)
    img = cv2.imread(imgpath,0)
    print 'done.'
    print 'computing feature vector for {}...'.format(imgpath)
    Face = mat(img).flatten()
    normalizedface = Face-meanface 
    featureVect = normalizedface* eigVects
    print 'feature vector shape {}, finished'.format(featureVect.shape)
    return featureVect