'''
Created on 20 Jun 2018

@author: mauicv
'''

import math
import random
import matplotlib.pyplot as plt
import json


class Collection(object):
    
    def __init__(self,**kargs):
             
        self.count=0
        self.samples=[]
        
        self.file_name=kargs.get('file_name',None)
        if self.file_name==None:
            self.file_name="data"
        self.load()

    def addSample(self,sample):
        self.samples.append(sample)
        self.count+=1
        self.save()
        
    def rewind(self,n):
        if n>0:
            self.samples.pop()
            self.count-=1
            self.save()
            return self.rewind(n-1)
        else:    
            return self.samples[self.count-1]
        
    def getLast(self):
        if len(self.samples)>0:
            return self.samples[self.count-1]
        else:
            return None
    
    def save(self):
        try:
            with open(self.file_name+'.txt', 'w') as outfile:
                json.dump(self.samples, outfile)
        except:
            print("file save error")
        
    def load(self):
        try:
            with open(self.file_name+'.txt') as outfile:
                self.samples=json.load(outfile)
                self.count=len(self.samples)
                print('data.txt file loaded with number of samples:', self.count)
        except:
            print('data.txt file not loaded')
            return False
    
    def printSample(self,sample):
        print("*******************")
        print('screen_name:', sample['screen_name'])
        try:
            print('location:', sample['location'])
            print('followers_count:', sample['followers_count'])
            print("*******************")
            
        except:
            print("failure to print details for sample")
        pass
    
    def printCurrent(self):
        self.printSample(self.samples[self.count-1])
    
    def printAll(self):
        for sample in self.samples:
            self.printSample(sample)
            
        print("-----------")
        print("number of samples:",self.count)
            
    def printWithoutDuplicates(self):
        newList=[self.samples[0]]
        count=0
        for thisSample in self.samples:
            unique=True
            for thatSample in newList:
                if thisSample['id'] == thatSample['id']:
                    unique=False
            if unique:
                newList.append(thisSample)
                count+=1
        
        for sample in newList:
            self.printSample(sample)
        
        print("-----------")
        print("number of samples:",self.count)
        print("number of unique samples:",count)
                
        pass
            