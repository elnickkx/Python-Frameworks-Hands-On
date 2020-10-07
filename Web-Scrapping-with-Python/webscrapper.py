import requests
import pprint
from bs4 import BeautifulSoup as bs4
import re
import os

if os.path.exists('summary.txt'):
    os.remove('summary.txt')
fetchingAddress = "http://aytm.com"
pagescrapped = requests.get(fetchingAddress)
#print(pagescrapped.content)
subscriptionExists = ['PRICING']
pageSoup = bs4(pagescrapped.content, "html.parser")
#print(pageSoup.prettify)
routeAddress = [a.get("href") for a in pageSoup.find_all("a")]
#print(routeAddress)

for i in routeAddress:
    val = re.match("^https:.*?\/careers$", i)
    if val:
        careerRoute = val.group(0)

# supporting email address
pageSupport = bs4((requests.get(careerRoute)).content, "html.parser")
metaDescription = (pageSoup.find("meta", property="og:description"))["content"]
companyName = (re.findall(".*?\)\s+", metaDescription))[0] # if company name exists
#print(companyName)
pageTitle = (pageSoup.find(id="main-content-text")).get_text() #if title exists
#print(pageTitle.strip())
shortDescription = metaDescription
#print(shortDescription)
contactEmail = (pageSupport.find_all("div", class_="icon envelope-icon"))[0].get_text()
contactEmail = contactEmail.strip()
print(contactEmail)
# summarization algorithm pending
summaryData = ""
for i in routeAddress:
    if not i is None:
        infoSupport = fetchingAddress + i
        pageSupport = bs4((requests.get(infoSupport)).content, "html.parser")
        pageData = pageSupport.find_all("div", class_="pages")
        if len(pageData):
            summaryData = " ".join(pageData[0].get_text())
            print(summaryData)
        #with open("summary.txt", "a+") as file:
        #    file.write(summaryData)
#print(summaryData)
headerMenu = (pageSoup.find_all("div", id="header-menu"))[0].get_text()
checkPaidService = ["Paid" for i in subscriptionExists if i in headerMenu]
print(checkPaidService)




