'''
Created on 1 Jul 2018

@author: mauicv
'''

import random 
from MHRW_Algo.Collection import Collection
import tweepy 


class MHRW(object):
    '''
    classdocs
    '''

    def __init__(self, **kargs):
        '''
        Constructor
        '''
    
        #get api
        self.api=kargs.get('api',None)
        if self.api==None:
            print("no api!")
        
        #get data file
        self.data_file=kargs.get('data_file',None)
        self.collection = Collection(file_name=self.data_file)
        
        #get seed
        self.seed=kargs.get('seed',None)
        if self.seed == None:
            try:
                self.seed=self.api.get_user(id=self.collection.getLast()['id'])
            except:
                print("no seed!")
        else:
            if self.collection.getLast() != self.seed:
                print("adding seed to collection")
                self.collection.addSample(self.seed._json)
                    
        #state variables
        self.currentUser=self.seed
        self.currentStepFinished=False
        self.p=0
        self.cu_p=0
        self.midPoint=0
        self.cursor=[]
        self.followers=[]
        self.following=[]
        self.record=False
        self.fof=None
        
        #number of steps
        self.N=0
        self.count=0
    
    def run(self,numOfSteps):
        if self.api == None:
            print('no api!')
            return False
        if self.seed == None:
            print('no seed!')
            return False
        else:
            self.N=numOfSteps
            print("---------------------")
            print("initiating with seed:",self.seed.screen_name)
            print("---------------------")

            while self.count<self.N:
                self.currentStepFinished=False
                while not self.currentStepFinished:
                    ##
                    self.p=0
                    self.cu_p=0
                    self.record=False
                    ##
                    if self.stepSetUp():
                        if self.selectNeighbor(self.fof, self.cursor):
                            self.count+=1
                            print('sample number: ',self.count)
                            self.collection.addSample(self.currentUser._json)
                            self.collection.save()
                            self.collection.printCurrent()
                            self.clean()
                            self.currentStepFinished=True
                        pass #start step loop
                    else:
                        #assume privacy is stopping progress and go back to last sample
                        self.count-=1
                        self.currentUser=self.api.get_user(id=self.collection.rewind(1)['id'])
                        self.clean()
                        self.currentStepFinished=True
                
    def stepSetUp(self):
        #check what information we have and configure the step process to make the least api calls...
        numOfEdges=self.currentUser.followers_count+self.currentUser.friends_count
        self.p=random.random()
        self.midPoint=self.currentUser.followers_count/(numOfEdges)
        
        if self.currentUser.protected:
            return False    #If user has privacy settings protecting follower and following details
        
        if self.p<self.midPoint:
            if len(self.followers)>0:
                pass #don't need any more api calls
                self.record=False
                self.cursor=self.followers
            else:
                try:
                    self.record=True
                    self.fof='followers'
                    self.cursor=tweepy.Cursor(self.api.followers, id=self.currentUser.id,count=200).pages()
                    pass
                except:
                    return False #indicates tweepy access issue in which case we will rewind and take a step back...
        else:
            self.cu_p=self.midPoint
            if len(self.following)>0:
                self.record=False
                pass #don't need any more api calls
                self.cursor=self.following
            else:
                try:
                    self.record=True
                    self.fof='following'
                    self.cursor=tweepy.Cursor(self.api.friends, id=self.currentUser.id,count=200).pages()
                    pass
                except:
                    return False #indicates tweepy access issue in which case we will rewind and take a step back...
        pass
        return True
            
    def selectNeighbor(self,FoF,element):
        try:
            for item in element:
                if self.selectNeighbor(FoF, item):
                    return True
            return False
        except:
            if self.record:
                getattr(self,FoF).append(element)
            eSum=self.getEdgeSum(self.currentUser)
            uSum=self.getEdgeSum(element)
            if not uSum:
                self.cu_p+self.cu_p+(1/eSum)
                return False
            else:
                self.cu_p=self.cu_p+(1/eSum)*min([1,eSum/uSum])
            if self.p<self.cu_p:
                self.currentUser= element
                return True
            else:
                return False
            
    def getEdgeSum(self,user):
        try:
            return user.followers_count+user.friends_count
        except:
            return False
            
    def clean(self):
        
        self.currentStepFinished=False
        
        self.p=0
        self.cu_p=0
        self.midPoint=0

        self.cursor=[]

        self.followers=[]
        self.following=[]
        self.fof=None
        self.record=False
        
    def printAllProg(self):
        self.collection.load()
        self.collection.printAll()
        
        
        