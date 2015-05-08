#!/usr/bin/python -tt
#####################################################################################################################
# CSE 591: Security and Vulnerability Analysis
# 
# Team 5:
#
# Kartheek Nallepalli
# Bhargavi Rajagopalan
# Priya Pipada
# Ayush Maheshwari
# Nikhil Aourpally
#
#
# This is the driver program. Run the main function here to find potential vulnerabilities in the website
#####################################################################################################################

# Python Imports

from __future__ import division
from bs4 import BeautifulSoup
from lxml import html
from os import system, path
from random import randint
from urlparse import urlparse
import ast
import json
import math
import nltk
import re
import requests
#requests.packages.urllib3.disable_warnings()
import sys
import time
import urllib
import urllib2

# This is a global set that contains all the URL's crawled from the website.
urls = set()
stopWords = []
            

#####################################################################################################################
# This method takes in a form to be filled and the url and tries to guess valid inputs that would result in a
# successful response from the server
# Inputs:
#       params[] (List[String]): list of parameters along with the types in the following format. 
#                               ex: ["username::text", "password::password"]
#       action (String): The action the form should take when submitted 
#       url (String): The page URL for getting the HTML data and figuring out what to fill
# Output:
#       validResponse (String): returns the HTML string of the valid response
#####################################################################################################################

def getValidResponse(params, action, url, cookies):
    formInput={} 
    for key in params:	  
        value = params[key]
	formInput[key] = generateValue(value['label'],value['type'])
    print cookies, type(cookies)
    validResponse = constructPostRequest(formInput, cookies, action)
    return validResponse

#####################################################################################################################
# This method constructs a HTTP Post Request to submit the form to it
#####################################################################################################################

def constructPostRequest(formInput, input_cookies, action):
	#cookies = dict(cse591='kP047iYtubEZ6ZnMKmxO')
	r = requests.post(action, data=formInput, verify=False, cookies=input_cookies)	
	#print r.headers
	#print r.status_code
	#print r.text
	return r.text

#####################################################################################################################
# This method takes in a form to be filled and the url and inserts <scripts> into the fields.
# Inputs:
#       params[] (List[String]): list of parameters along with the types in the following format. 
#                               ex: ["username::text", "password::password"]
#       action (String): The action the form should take when submitted 
# Output:
#       xssResponse (String): returns the HTML response
#####################################################################################################################

def getXssResponse(params, action, url, cookies):
    formInput={} 
    for key in params:	  
        value = params[key]
	formInput[key]="<sCript>xssAttack</sCript>"
    xssInjResponse = constructPostRequest(formInput,cookies,action)
    return xssInjResponse
    
def getXssScore(xssResponse, input_cookies): 
    urls = open("crawledURLs.txt")
    for url in urls:        
        response = requests.get(re.sub("\n","",url), verify=False, cookies=input_cookies).text
        if bool(re.search('<sCript>xssAttack</sCript>', response)):            
            return 1
    return 0                                       

#####################################################################################################################
# This method takes in a form to be filled and the url and tries SQL injection in the fields
# Inputs:
#       params[] (List[String]): list of parameters along with the types in the following format. 
#                               ex: ["username::text", "password::password"]
#       action (String): The action the form should take when submitted 
# Output:
#       xssResponse (String): returns the HTML response
#####################################################################################################################

def getSqlInjResponse(params, action, url, cookies):        
    formInput={} 
    #if(action == ""):
    #    action = url
    #parsedURL = urlparse(url);
    #dirPath = path.split(parsedURL.path)
    #fullPath=parsedURL.scheme+"://"+parsedURL.netloc+dirPath[0]+"/"
    #if(parsedURL.netloc not in action):
    #    action = parsedURL.scheme+"://"+parsedURL.netloc+action
    #print action
    for key in params:	  
        value = params[key]
	formInput[key] ="' or 1=1 --'"
    sqlInjResponse = constructPostRequest(formInput,cookies,action)
    return sqlInjResponse

#####################################################################################################################
# This method takes in two HTML strings, compares them and assigns a similarity score. The idea is to use this 
# score to see how similar pages with valid and invalid outputs are.
# Inputs:
#       html_1 (String): The first HTML page
#       html_2 (String): The second HTML page
# Output:
#       score (double): similarity between pages 
#####################################################################################################################

def getSimilarityScore(html_1, html_2):
    cleanResponse1 = BeautifulSoup(html_1).get_text()
    cleanResponse2 = BeautifulSoup(html_2).get_text()
    return calculateCosineSimilarity(formatVector(cleanResponse1), formatVector(cleanResponse2))

def calculateCosineSimilarity(group1, group2):
    doc1sq = doc2sq = frequency = 0
    for i in group1:
        if i in group2:
            frequency += group1[i] * group2[i]
    for j in group1:
        doc1sq += math.pow(group1[j], 2)
    for k in group2:
        doc2sq += math.pow(group2[k], 2)
        
    score = float(frequency) / (math.sqrt(doc1sq) * math.sqrt(doc2sq))
    return score
   
def formatVector(response):
    global stopWords
    cleanResponse = map(lambda x:re.split(" ", x), re.split("\n", response))
    vectorList = []
    vectorDict = {}
    for i in cleanResponse:
            vectorList.extend(i)    
    vector = []
    for i in vectorList:
        if str(i) != '' or str(i) not in stopWords:
            vector.append(i.lower())
    for j in vector:
        if j in vectorDict:
            vectorDict[j] += 1
        else:
            vectorDict[j] = 1
    return vectorDict


#####################################################################################################################
# This method takes in the original label extracted, gets the similarity score and predicts the valid form entries
# by understanding meaning of the labes and mapping them to known labels using dictionary similarity and edit-
# distance score.
#
# TODO : Faced problems with wu-palmer similarity over wordNet (flase positives and not all terms present)
#        Currently using just the edit distance
#
# Inputs:
#       label (String): Label generated from the scarppy code extended
# Output:
#       generated value (String): Valid generated form input value
#####################################################################################################################

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

         
#####################################################################################################################
# Helper methods
#####################################################################################################################     

# Get the specific form parameters
def getFormParams(link):
    params = {}
    # Get Labels from the form
    labels = []
    source = link['source'].replace("\n","")
    for i in range(0, len(source)):
    	label = ''
    	if source[i] == '>':
        	while source[i] != '<':
                    label += source[i]
                    i = i + 1
                    if i >= len(source) - 1:
                        break;
                if label[1:] and not label[1:].isspace():
                    labels.append(label[1:])
    i = 0
    for j in link['form']:
	params[j['name']] = {}
	params[j['name']]['type'] = j['type']
	params[j['name']]['label'] = labels[0]
	i = i + 1
#        params.append(j['name'])
    
    return (link['target'], params)
        

# This method gets the list of stopwords
def getStopWords():
    global stopWords
    f = open("stopwords.en")
    for i in f:
        stopWords.append(re.sub("\n","",i))
        
# Get the edit-distance score between  two words
def getEdidDistanceScore(word1, word2):        
    distance = nltk.metrics.distance.edit_distance(word1, word2, transpositions=False)    
    avgLength = (len(word1) + len(word2))/2
    score = distance/avgLength
    return score

#Get cookies from user
def getCookies():
    flag = 0
    cookies = {}
    print "Enter cookies(Press X to exit): "
    while True:
        if not flag:
            key = raw_input("Enter Key: ")
            flag = 1
            if key == 'X':
                break;
        else:
            value = raw_input("Enter value: ")
            flag = 0
            if value == 'X':
                break;
            cookies[key] = value
    return cookies

#####################################################################################################################
# This is the main method that gets called and submits the report on possible vulnerabilities
#####################################################################################################################

def main():   
    
    # Init Global variables
    getStopWords()
   
    # Add the required headers, most likely its just the login cookie for the page.
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'cse591=kP047iYtubEZ6ZnMKmxO'))
    domain = "129.219.253.30:80" 
    url = raw_input("Enter the web address: ")
    cookies = getCookies()
    
    # Remove any residual files
    system("rm items.json")
    system("rm crawledURLs.txt")
    system("rm reverse_report")
    system("rm reverse_response")
    
    
    # Use Scrappy to get recursively get all URLs, Stores the 
    system("scrapy crawl ReverseCrawler -a domain="+domain+" -a start_urls="+url+" -a cookies=\""+str(cookies)+"\" -o items.json")
    #cookies = ast.literal_eval(cookies)
    
    # Iterate over all the URL's and their forms
    UrlForms = json.load(open("items.json"))
    
    print "\n\n\n"
    
    
    # Open report, response file
    reportFile = open('reverse_report','w')
    responseFile = open('reverse_response','w')
    
    # Iterate through all possible forms 
    for urlForm in UrlForms:                
        (action, params) = getFormParams(urlForm) 
        print "[INFO] action: ", action
        
        # Get the valid response
        validResponse = getValidResponse(params, action, url, cookies)        
        
	# Append the resposes to response file
        responseFile.write("%%%%%%%%%%%%%%%%%%%%%%%%%% Start Valid Response %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
        responseFile.write(action + "\n")
        responseFile.write(str(params) + "\n")
        responseFile.write(BeautifulSoup(validResponse).get_text() + "\n")
        responseFile.write("############################ Start SQL Injection response ###########################\n")
	      
	      
	# Attempt SQL Injection and Get the score
        sqlInjResponse = getSqlInjResponse(params, action, url, cookies)        
        responseFile.write(BeautifulSoup(sqlInjResponse).get_text() + "\n")
        responseFile.write("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Start XSS response @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")        
        sqlInjectionScore = float(1) - getSimilarityScore(validResponse, sqlInjResponse)
        print "[INFO] SQL_INJ_Score = ", sqlInjectionScore        
        
        # Attempt XSS and get the score
        xssResponse = getXssResponse(params, action, url, cookies)
        responseFile.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
        xssScore = getXssScore(xssResponse, cookies)
        print "[INFO] XSS_Score = ", xssScore
        
        # Add scores to the report
        reportFile.write("[Params]:: " + str(params) + "\n")
        reportFile.write("[Action]:: " + action + "\n")
        reportFile.write("[SQL_Inj_Score]:: " + str(sqlInjectionScore) + "\n")
        reportFile.write("[XSS_Inj_Score]:: " + str(xssScore) + "\n\n")
        
        print "\n\n"
		
    # Close the report
    reportFile.close()     
    responseFile.close()                          
              
if __name__ == '__main__':
    main()
