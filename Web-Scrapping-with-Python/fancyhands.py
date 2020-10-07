import requests
import pprint
from bs4 import BeautifulSoup as bs4
import re
import os
import descriptionAlgo
import argparse
import pandas as pd
from fileformatter import fileFormatter


def Extract_data(websiteURL):
    responsiveData = list()
    dirpath = os.path.dirname(os.path.realpath(__file__))
    
    # check summarisation file if exists
    if os.path.exists(dirpath + '/summary2.txt'):
        os.remove(dirpath + '/summary2.txt')

    # setting websiteURL for condition checks and evaluate responsive data
    fetchingAddress = websiteURL
    pagescrapped = requests.get(fetchingAddress)
    
    # pricing parameters
    subscriptionExists = ['PRICING', 'SUBSCRIPTION', 'Pricing', 'Subscription']
    pageSoup = bs4(pagescrapped.content, "html.parser")
    
    # router switch list for entire website
    routeAddress = [a.get("href") for a in pageSoup.find_all("a")]
    
    # Scrapping content with file  
    for i in routeAddress:
       if not i is None:
           infoSupport = fetchingAddress + i
           pageSupport = bs4((requests.get(infoSupport)).content, "html.parser")
           pageData = pageSupport.find_all("p")
           if len(pageData):
               summaryData = pageData[0].get_text()

       with open(dirpath + "/summary2.txt", "a+") as file:
           file.write(summaryData)
    
    # if loop condition
    companyName = pageSoup.find("meta", property="og:title")["content"]
    responsiveData.append(companyName)
    pageTitle = pageSoup.find("h1").get_text().strip()
    responsiveData.append(pageTitle)
    shortDescription = pageSoup.find("meta", property="og:description")["content"]
    responsiveData.append(shortDescription)
    contactEmail = ""
    if pageSoup.find_all("meta", property="og:email"):
        contactEmail = (pageSoup.find_all("meta", property="og:email")[0])["content"]
    responsiveData.append(contactEmail)
    if pageSoup.find_all("a", {'href': '/pricing.*?'}):
        headerMenu = pageSoup.find_all("a", {'href': '/pricing.*?'})[-1].get_text()
    else:
        headerMenu = pageSoup.find_all("a", {'href': '/pricing/'})[-1].get_text()
    metaString = fileFormatter(dirpath + "/summary2.txt", dirpath + "/newSummary.txt")
    # number of top fetched sentences set to 7 (by default)
    exit()
    summarization = descriptionAlgo.generate_summary(metaString)
    responsiveData.append(summarization)
    checkPaidService = ""
    for i in subscriptionExists:
        if i in headerMenu:
            checkPaidService = "Paid"
            break
        else:
            checkPaidService = "Unknown"
    responsiveData.append(checkPaidService)
    
    # remove meta supportive datastrings
    os.remove(metaString)
    os.remove(dirpath + "/summary2.txt")
    
    return responsiveData

def Add_information(dataList):
    # dataList Structure -> ['comapanyName', 'pageTitle', 'screenShot', 'shortDescription', 'contactEmail'
    #                        'summarisation', 'checkPaidService']
    dirpath = os.path.dirname(os.path.realpath(__file__))
    
    formattedResponse = pd.DataFrame({
        "Company_Name": [dataList[0]],
        "Title": [dataList[1]],
        "Image/Screeenshot": [""],
        "Short_Description": [dataList[2]],
        "contact_email": [dataList[3]],
        "Summarize the website content": [dataList[4]],
        "Is the website has paid service?": [dataList[5]]
    })
    
    formattedResponse.to_csv(dirpath + "/new.csv", sep="\t", na_rep="Unknown", index=False)
    
    return formattedResponse
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument('--URL', '-U', nargs="*", type=str, default=0, required=True)
    args = parser.parse_args()    
    websiteURL = args.URL[0]
    valuableData = Extract_data(websiteURL)
    response = Add_information(valuableData)
    print(response)
    exit(0)


