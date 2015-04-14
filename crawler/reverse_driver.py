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
import json
import urllib2
from lxml import html
from os import system
import re

# This is a global set that contains all the URL's crawled from the website.
urls = set()

#####################################################################################################################
# This method gets all the urls present on the website by recursively crawling the pages
# Input:
#     startURL (String): the url to be crawled
#     baseURL (String): This is the base url that will be appended if relative paths are used
#     opener : used for the GET/POST request
# Output:
#     No output as it recursively crawls the pages and fills in the global Set       
#
#####################################################################################################################

def getAllURLs(startURL, baseURL, opener):
    try: 
        global urls      
        tree = html.fromstring(opener.open(startURL).read())   
        for url in tree.xpath('//a/@href'):
            if startURL not in str(url) and startURL in baseURL:
                ext_url = baseURL + url
	    else:
                start_URL = startURL.rsplit('/', 1)
	        ext_url = start_URL[0] + '/' + url
            ext_url = str(ext_url)
            if ext_url not in urls:
            	urls.add(ext_url)
            	getAllURLs(ext_url, baseURL, opener)
    except Exception,e:
        pass
            

#####################################################################################################################
# This method returns the form parameters and if the form exists on the page
# Use Scrapy here to extract the form and then parse the output and return as specified below
# Input:
#     domain (String): the domain 
#     url (String): url to be crawled
#     cookies (dictionary): the cookie dictionary used for logging in  
# Outputs: 
#     params[] (List[String]):  list of parameters along with the types in the following format. (name::type::value)
#                               ex: ["username::text::", "password::password::", button::myButton::submit]
#     action (String): The action the form should take when submitted  
#####################################################################################################################

def getFormForURl(domain, url, cookies):

    system("scrapy crawl crawler -a domain="+domain+" -a start_urls="+url+" -a cookies=\""+cookies+"\" -o items.json")
    data = open('items.json').read()
    system("rm items.json")        
    action = ""
    params = []
    
    if 'url' in data:
        jsonData = json.loads(data[1:-1])                        
        for element in jsonData['form']:            
            if 'action' in element:
                action = element.rsplit('::',1)[1]
           
            name = ""
            type = ""
            value = ""            
            for inputPart in element.rsplit(' '):                
                if 'name' in inputPart:
                    name = re.sub(">", "", re.sub("\"", "", inputPart.rsplit('=',1)[1]))                                        
                if 'type' in inputPart:
                    type = re.sub(">", "", re.sub("\"", "", inputPart.rsplit('=',1)[1]))                  
                if 'value' in inputPart:
                    value = re.sub(">", "", re.sub("\"", "", inputPart.rsplit('=',1)[1]))                            
            params.append(str(name+"::"+type+"::"+value))                                                
            
    return (params, action)

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

def getValidResponse(params, action, url):
    # do stuff here
    return validResponse

#####################################################################################################################
# This method takes in a form to be filled and the url and inserts <scripts> into the fields.
# Inputs:
#       params[] (List[String]): list of parameters along with the types in the following format. 
#                               ex: ["username::text", "password::password"]
#       action (String): The action the form should take when submitted 
# Output:
#       xssResponse (String): returns the HTML response
#####################################################################################################################

def getXssResponse(params, action):
    # do stuff here
    return xssResponse

#####################################################################################################################
# This method takes in a form to be filled and the url and tries SQL injection in the fields
# Inputs:
#       params[] (List[String]): list of parameters along with the types in the following format. 
#                               ex: ["username::text", "password::password"]
#       action (String): The action the form should take when submitted 
# Output:
#       xssResponse (String): returns the HTML response
#####################################################################################################################

def getSqlInjResponse(params, action):
    # do stuff here
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
    # do stuff here
    return score


#####################################################################################################################
# This is the main method that gets called and submits the report on possible vulnerabilities
#####################################################################################################################

def main():   
    
    # add the required headers, most likely its just the login cookie for the page.
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'cse591=kP047iYtubEZ6ZnMKmxO'))
    cookies = "{'cse591':'kP047iYtubEZ6ZnMKmxO'}"   
    domain = "129.219.253.30:80" 
    
    # get all the urls from the webApplication
    getAllURLs("https://129.219.253.30:80/", "https://129.219.253.30:80/", opener)
    print("urls-extracted: ", urls)
    
    # Open report file
    reportFile= open('reverse_report.txt','w')
        
    # for each url crawl the page for     
    for url in urls:
        reportFile.write("url:: " + str(url) + "\n")
        (params, action) = getFormForURl(domain, url, cookies)
        reportFile.write("params:: " + str(params) + "\n")
        reportFile.write("action::" + str(action) + "\n")

        # Get responses for valid and invalid inputs
        #validResponse = getValidResponse(params, action, url)        
        #xssResponse = getXssResponse(params, action) 
        #sqlInjResponse = getSqlInjResponse(params, action)
        # Get xss and SqlInjection score 
        #xssScore = getSimilarityScore(validResponse, xssResponse)
        #sqlInjScore = getSimilarityScore(validResponse, sqlInjResponse)
        
        # Print the scores to see if there exists a vulnerability
        
        #print("xssScore: ", xssScore)
        #print("sqlInjScore", sqlInjScore)

    # Close the report
    reportFile.close()              
              
if __name__ == '__main__':
    main()
