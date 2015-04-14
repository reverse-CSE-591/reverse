#!/usr/bin/python -tt
################################################################################################################
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
################################################################################################################

# Python Imports
import json
import urllib2
from lxml import html
from os import system

# This is a global set that contains all the URL's crawled from the website.
urls = set()

################################################################################################################
# This method gets all the urls present on the website by recursively crawling the pages
# Input:
#     startURL (String): the url to be crawled
#     baseURL (String): This is the base url that will be appended if relative paths are used
# Output:
#     No output as it recursively crawls the pages and fills in the global Set       
#
################################################################################################################
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
            

################################################################################################################
# This method returns the form parameters and if the form exists on the page
# Use Scrapy here to extract the form and then parse the output and return as specified below
# Input: 
#     url (String): url to be crawled
# Outputs: 
#     params[] (List[String]):  list of parameters along with the types in the following format. 
#                               ex: ["username::text", "password::password"]
#     action (String): The action the form should take when submitted  
################################################################################################################
def getFormForURl(url, cookies):
    system("scrapy crawl crawler -a domain=129.219.253.30:80 -a start_urls="+url+" -a cookies=\""+cookies+"\" -o items.json")
    txt = open('items.json').read()
    system("rm items.json")
    #txt = dict(txt[1:-1])
    if 'url' in txt:
    	txt1 = json.loads(txt[1:-1])
	print txt1['url']
	print txt1['form']
    print "Done"
    #return (params, action)

################################################################################################################
# This method takes in a form to be filled and the url and tries to guess valid inputs that would result in a
# successful response from the server
# Inputs:
#       params[] (List[String]): list of parameters along with the types in the following format. 
#                               ex: ["username::text", "password::password"]
#       action (String): The action the form should take when submitted 
# Output:
#       validResponse (String): returns the HTML string of the valid response
################################################################################################################
def getValidResponse(params, action, url):
    # do stuff here
    return validResponse

################################################################################################################
# This method takes in a form to be filled and the url and inserts <scripts> into the fields.
# Inputs:
#       params[] (List[String]): list of parameters along with the types in the following format. 
#                               ex: ["username::text", "password::password"]
#       action (String): The action the form should take when submitted 
# Output:
#       xssResponse (String): returns the HTML response
################################################################################################################
def getXssResponse(params, action):
    # do stuff here
    return xssResponse

################################################################################################################
# This method takes in a form to be filled and the url and tries SQL injection in the fields
# Inputs:
#       params[] (List[String]): list of parameters along with the types in the following format. 
#                               ex: ["username::text", "password::password"]
#       action (String): The action the form should take when submitted 
# Output:
#       xssResponse (String): returns the HTML response
################################################################################################################
def getSqlInjResponse(params, action):
    # do stuff here
    return sqlInjResponse

################################################################################################################
# This method takes in two HTML strings, compares them and assigns a similarity score. The idea is to use this 
# score to see how similar pages with valid and invalid outputs are.
# Inputs:
#       html_1 (String): The first HTML page
#       html_2 (String): The second HTML page
# Output:
#       score (double): similarity between pages 
################################################################################################################
def getSimilarityScore(html_1, html_2):
    # do stuff here
    return score


################################################################################################################
# This is the main method that gets called and submits the report on possible vulnerabilities
################################################################################################################
def main():   
    
    # add the required headers, most likely its just the login cookie for the page.
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'cse591=kP047iYtubEZ6ZnMKmxO'))
    cookies = "{'cse591':'kP047iYtubEZ6ZnMKmxO'}"   
    
    # get all the urls from the webApplication
    getAllURLs("https://129.219.253.30:80/", "https://129.219.253.30:80/", opener)
    print("urls-extracted: ", urls)
        
    # for each url crawl the page for     
    for url in urls:
        getFormForURl(url, cookies)

        # Get responses for valid and invalid inputs
        #validResponse = getValidResponse(params, action, url)        
        #xssResponse = getXssResponse(params, action) 
        #sqlInjResponse = getSqlInjResponse(params, action)
        # Get xss and SqlInjection score 
        #xssScore = getSimilarityScore(validResponse, xssResponse)
        #sqlInjScore = getSimilarityScore(validResponse, sqlInjResponse)
        
        # Print the scores to see if there exists a vulnerability
        print("url: ", url)
        #print("xssScore: ", xssScore)
        #print("sqlInjScore", sqlInjScore)
              
              
if __name__ == '__main__':
    main()
