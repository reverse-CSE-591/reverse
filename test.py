from __future__ import division
import nltk
import time
from random import randint


def getEdidDistanceScore(word1, word2):        
    distance = nltk.metrics.distance.edit_distance(word1, word2, transpositions=False)    
    avgLength = (len(word1) + len(word2))/2
    score = distance/avgLength
    return score

def getLabel(orglabel):
    userset = ['user','username','user_name']
    maxscore =0
    newlabel =''
    for field in userset:
        score = getEdidDistanceScore(orglabel, field)
        if(score > maxscore):
	    maxscore = score
            newlabel = 'username'
    print 'Max score' + str(maxscore), 'Label' + newlabel
    if(maxscore<0.5):
        newlabel = orglabel
    return newlabel             
    
def generateValue(label, labeltype):
    if labeltype == 'text':
        newlabel = getLabel(label)
        if newlabel == 'username':	
            return 'reverse'+ str(time.time())
        else:
            return 'reverserandom'+ str(time.time())
    elif labeltype == 'password':
        return 'reversePass'+ str(time.time())
    elif labeltype == 'email':
        return 'reverse'+str(time.time())+'@reverse.com'
    elif labeltype == 'number':
         return randint(0,10000)    
 
if __name__ == '__main__':
    dict = {'usersname' : {'label': 'user', 'type':'text'} , 'age':{'label':'age','type': 'number'}, 'password': {'label':'password', 'type':'password'}}
    forminput = {}
    for key in dict:
        value = dict[key] 
        forminput[key] = generateValue(value['label'], value['type'])
    print forminput 
           
 

